import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Database Connection Setup ---
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "homestead"),
        auth_plugin='mysql_native_password'
    )

# --- Home ---
@app.route("/")
def home():
    return render_template("home.html")

# ===============================
# Garden Beds CRUD
# ===============================
@app.route("/beds")
def beds_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM garden_beds")
    beds = cursor.fetchall()
    conn.close()
    return render_template("beds_list.html", beds=beds)

@app.route("/beds/new", methods=["GET", "POST"])
def bed_create():
    if request.method == "POST":
        name = request.form["name"]
        soil_type = request.form["soil_type"]
        area_sqft = request.form["area_sqft"]
        notes = request.form["notes"]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO garden_beds (name, soil_type, area_sqft, notes) VALUES (%s, %s, %s, %s)",
            (name, soil_type, area_sqft, notes)
        )
        conn.commit()
        conn.close()
        flash("Garden bed added!")
        return redirect(url_for("beds_list"))
    return render_template("bed_form.html", bed=None)

@app.route("/beds/<int:id>/edit", methods=["GET", "POST"])
def bed_edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM garden_beds WHERE id = %s", (id,))
    bed = cursor.fetchone()
    if request.method == "POST":
        bed["name"] = request.form["name"]
        bed["soil_type"] = request.form["soil_type"]
        bed["area_sqft"] = request.form["area_sqft"]
        bed["notes"] = request.form["notes"]
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE garden_beds SET name=%s, soil_type=%s, area_sqft=%s, notes=%s WHERE id=%s",
            (bed["name"], bed["soil_type"], bed["area_sqft"], bed["notes"], id)
        )
        conn.commit()
        conn.close()
        flash("Garden bed updated!")
        return redirect(url_for("beds_list"))
    conn.close()
    return render_template("bed_form.html", bed=bed)

@app.route("/beds/<int:id>/delete", methods=["POST"])
def bed_delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM garden_beds WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Garden bed deleted!")
    return redirect(url_for("beds_list"))

# ===============================
# Crops CRUD (barebones)
# ===============================
@app.route("/crops")
def crops_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT crops.*, garden_beds.name as bed_name FROM crops LEFT JOIN garden_beds ON crops.bed_id = garden_beds.id")
    crops = cursor.fetchall()
    conn.close()
    return render_template("crops_list.html", crops=crops)

@app.route("/crops/new", methods=["GET", "POST"])
def crop_create():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM garden_beds")
    beds = cursor.fetchall()
    if request.method == "POST":
        crop_type = request.form["crop_type"]
        variety = request.form["variety"]
        plant_date = request.form.get("plant_date") or None
        bed_id = request.form.get("bed_id") or None
        estimated_first_harvest = request.form.get("estimated_first_harvest") or None
        estimated_last_harvest = request.form.get("estimated_last_harvest") or None
        estimated_yield = request.form.get("estimated_yield") or None
        yield_unit = request.form.get("yield_unit")
        status = request.form.get("status")
        notes = request.form.get("notes")
        cursor2 = conn.cursor()
        cursor2.execute("""
            INSERT INTO crops 
            (crop_type, variety, plant_date, bed_id, estimated_first_harvest, estimated_last_harvest, estimated_yield, yield_unit, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (crop_type, variety, plant_date, bed_id, estimated_first_harvest, estimated_last_harvest, estimated_yield, yield_unit, status, notes))
        conn.commit()
        conn.close()
        flash("Crop added!")
        return redirect(url_for("crops_list"))
    conn.close()
    return render_template("crop_form.html", crop=None, beds=beds)

@app.route("/crops/<int:id>/edit", methods=["GET", "POST"])
def crop_edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM crops WHERE id = %s", (id,))
    crop = cursor.fetchone()
    cursor.execute("SELECT id, name FROM garden_beds")
    beds = cursor.fetchall()
    if request.method == "POST":
        crop["crop_type"] = request.form["crop_type"]
        crop["variety"] = request.form["variety"]
        crop["plant_date"] = request.form.get("plant_date") or None
        crop["bed_id"] = request.form.get("bed_id") or None
        crop["estimated_first_harvest"] = request.form.get("estimated_first_harvest") or None
        crop["estimated_last_harvest"] = request.form.get("estimated_last_harvest") or None
        crop["estimated_yield"] = request.form.get("estimated_yield") or None
        crop["yield_unit"] = request.form.get("yield_unit")
        crop["status"] = request.form.get("status")
        crop["notes"] = request.form.get("notes")
        cursor2 = conn.cursor()
        cursor2.execute("""
            UPDATE crops SET 
                crop_type=%s, variety=%s, plant_date=%s, bed_id=%s, estimated_first_harvest=%s, 
                estimated_last_harvest=%s, estimated_yield=%s, yield_unit=%s, status=%s, notes=%s
            WHERE id=%s
        """, (crop["crop_type"], crop["variety"], crop["plant_date"], crop["bed_id"],
              crop["estimated_first_harvest"], crop["estimated_last_harvest"], crop["estimated_yield"],
              crop["yield_unit"], crop["status"], crop["notes"], id))
        conn.commit()
        conn.close()
        flash("Crop updated!")
        return redirect(url_for("crops_list"))
    conn.close()
    return render_template("crop_form.html", crop=crop, beds=beds)

@app.route("/crops/<int:id>/delete", methods=["POST"])
def crop_delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM crops WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Crop deleted!")
    return redirect(url_for("crops_list"))

# ===============================
# Chickens CRUD (barebones)
# ===============================
@app.route("/chickens")
def chickens_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chickens")
    chickens = cursor.fetchall()
    conn.close()
    return render_template("chickens_list.html", chickens=chickens)

@app.route("/chickens/new", methods=["GET", "POST"])
def chicken_create():
    if request.method == "POST":
        name = request.form["name"]
        breed = request.form["breed"]
        purpose = request.form["purpose"]
        sex = request.form["sex"]
        hatch_date = request.form.get("hatch_date") or None
        acquired_date = request.form.get("acquired_date") or None
        status = request.form.get("status")
        notes = request.form.get("notes")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chickens (name, breed, purpose, sex, hatch_date, acquired_date, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, breed, purpose, sex, hatch_date, acquired_date, status, notes))
        conn.commit()
        conn.close()
        flash("Chicken added!")
        return redirect(url_for("chickens_list"))
    return render_template("chicken_form.html", chicken=None)

@app.route("/chickens/<int:id>/edit", methods=["GET", "POST"])
def chicken_edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chickens WHERE id = %s", (id,))
    chicken = cursor.fetchone()
    if request.method == "POST":
        chicken["name"] = request.form["name"]
        chicken["breed"] = request.form["breed"]
        chicken["purpose"] = request.form["purpose"]
        chicken["sex"] = request.form["sex"]
        chicken["hatch_date"] = request.form.get("hatch_date") or None
        chicken["acquired_date"] = request.form.get("acquired_date") or None
        chicken["status"] = request.form.get("status")
        chicken["notes"] = request.form.get("notes")
        cursor2 = conn.cursor()
        cursor2.execute("""
            UPDATE chickens SET name=%s, breed=%s, purpose=%s, sex=%s, hatch_date=%s, acquired_date=%s, status=%s, notes=%s
            WHERE id=%s
        """, (chicken["name"], chicken["breed"], chicken["purpose"], chicken["sex"], chicken["hatch_date"],
              chicken["acquired_date"], chicken["status"], chicken["notes"], id))
        conn.commit()
        conn.close()
        flash("Chicken updated!")
        return redirect(url_for("chickens_list"))
    conn.close()
    return render_template("chicken_form.html", chicken=chicken)

@app.route("/chickens/<int:id>/delete", methods=["POST"])
def chicken_delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chickens WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Chicken deleted!")
    return redirect(url_for("chickens_list"))

# ===============================
# Pets CRUD (barebones)
# ===============================
@app.route("/pets")
def pets_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    conn.close()
    return render_template("pets_list.html", pets=pets)

@app.route("/pets/new", methods=["GET", "POST"])
def pet_create():
    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        breed = request.form["breed"]
        sex = request.form["sex"]
        birth_date = request.form.get("birth_date") or None
        acquired_date = request.form.get("acquired_date") or None
        status = request.form.get("status")
        notes = request.form.get("notes")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pets (name, species, breed, sex, birth_date, acquired_date, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, species, breed, sex, birth_date, acquired_date, status, notes))
        conn.commit()
        conn.close()
        flash("Pet added!")
        return redirect(url_for("pets_list"))
    return render_template("pet_form.html", pet=None)

@app.route("/pets/<int:id>/edit", methods=["GET", "POST"])
def pet_edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pets WHERE id = %s", (id,))
    pet = cursor.fetchone()
    if request.method == "POST":
        pet["name"] = request.form["name"]
        pet["species"] = request.form["species"]
        pet["breed"] = request.form["breed"]
        pet["sex"] = request.form["sex"]
        pet["birth_date"] = request.form.get("birth_date") or None
        pet["acquired_date"] = request.form.get("acquired_date") or None
        pet["status"] = request.form.get("status")
        pet["notes"] = request.form.get("notes")
        cursor2 = conn.cursor()
        cursor2.execute("""
            UPDATE pets SET name=%s, species=%s, breed=%s, sex=%s, birth_date=%s, acquired_date=%s, status=%s, notes=%s
            WHERE id=%s
        """, (pet["name"], pet["species"], pet["breed"], pet["sex"], pet["birth_date"],
              pet["acquired_date"], pet["status"], pet["notes"], id))
        conn.commit()
        conn.close()
        flash("Pet updated!")
        return redirect(url_for("pets_list"))
    conn.close()
    return render_template("pet_form.html", pet=pet)

@app.route("/pets/<int:id>/delete", methods=["POST"])
def pet_delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pets WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Pet deleted!")
    return redirect(url_for("pets_list"))

# ===============================
# Equipment CRUD (barebones)
# ===============================
@app.route("/equipment")
def equipment_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipment")
    equipment = cursor.fetchall()
    conn.close()
    return render_template("equipment_list.html", equipment=equipment)

@app.route("/equipment/new", methods=["GET", "POST"])
def equipment_create():
    if request.method == "POST":
        name = request.form["name"]
        brand = request.form["brand"]
        model = request.form["model"]
        purchase_date = request.form.get("purchase_date") or None
        status = request.form.get("status")
        notes = request.form.get("notes")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO equipment (name, brand, model, purchase_date, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, brand, model, purchase_date, status, notes))
        conn.commit()
        conn.close()
        flash("Equipment added!")
        return redirect(url_for("equipment_list"))
    return render_template("equipment_form.html", equipment=None)

@app.route("/equipment/<int:id>/edit", methods=["GET", "POST"])
def equipment_edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipment WHERE id = %s", (id,))
    equipment = cursor.fetchone()
    if request.method == "POST":
        equipment["name"] = request.form["name"]
        equipment["brand"] = request.form["brand"]
        equipment["model"] = request.form["model"]
        equipment["purchase_date"] = request.form.get("purchase_date") or None
        equipment["status"] = request.form.get("status")
        equipment["notes"] = request.form.get("notes")
        cursor2 = conn.cursor()
        cursor2.execute("""
            UPDATE equipment SET name=%s, brand=%s, model=%s, purchase_date=%s, status=%s, notes=%s
            WHERE id=%s
        """, (equipment["name"], equipment["brand"], equipment["model"], equipment["purchase_date"],
              equipment["status"], equipment["notes"], id))
        conn.commit()
        conn.close()
        flash("Equipment updated!")
        return redirect(url_for("equipment_list"))
    conn.close()
    return render_template("equipment_form.html", equipment=equipment)

@app.route("/equipment/<int:id>/delete", methods=["POST"])
def equipment_delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipment WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Equipment deleted!")
    return redirect(url_for("equipment_list"))

# ===============================
# General Notes (Read/Add Only)
# ===============================
@app.route("/notes", methods=["GET", "POST"])
def notes_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == "POST":
        category = request.form["category"]
        reference_id = request.form.get("reference_id") or None
        note_date = request.form.get("note_date") or str(date.today())
        note = request.form["note"]
        cursor2 = conn.cursor()
        cursor2.execute("""
            INSERT INTO general_notes (category, reference_id, note_date, note)
            VALUES (%s, %s, %s, %s)
        """, (category, reference_id, note_date, note))
        conn.commit()
        flash("Note added!")
    cursor.execute("SELECT * FROM general_notes ORDER BY note_date DESC")
    notes = cursor.fetchall()
    conn.close()
    return render_template("notes_list.html", notes=notes)

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)