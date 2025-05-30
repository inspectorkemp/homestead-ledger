from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# 🔧 Update these values to match your MySQL setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Hello123',
    'database': 'homestead'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

# Generic route to show table data
def render_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return render_template('table.html', table=table_name, rows=rows)

@app.route('/garden_beds')
def garden_beds():
    return render_table('garden_beds')

@app.route('/crops')
def crops():
    return render_table('crops')

@app.route('/crop_harvests')
def crop_harvests():
    return render_table('crop_harvests')

@app.route('/crop_treatments')
def crop_treatments():
    return render_table('crop_treatments')

@app.route('/crop_notes')
def crop_notes():
    return render_table('crop_notes')

@app.route('/chickens')
def chickens():
    return render_table('chickens')

@app.route('/egg_production')
def egg_production():
    return render_table('egg_production')

@app.route('/chicken_weights')
def chicken_weights():
    return render_table('chicken_weights')

@app.route('/pets')
def pets():
    return render_table('pets')

@app.route('/pet_health_records')
def pet_health_records():
    return render_table('pet_health_records')

@app.route('/equipment')
def equipment():
    return render_table('equipment')

@app.route('/equipment_maintenance')
def equipment_maintenance():
    return render_table('equipment_maintenance')

@app.route('/general_notes')
def general_notes():
    return render_table('general_notes')

if __name__ == '__main__':
    app.run(debug=True)
