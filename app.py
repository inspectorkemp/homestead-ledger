from flask import Flask, render_template, request, redirect
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

@app.route('/garden_beds', methods=['GET', 'POST'])
def garden_beds():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO garden_beds (name, soil_type, area_sqft, notes) VALUES (%s, %s, %s, %s)",
            (
                request.form['name'],
                request.form.get('soil_type', ''),
                request.form.get('area_sqft', 0),
                request.form.get('notes', '')
            )
        )
        conn.commit()

    cursor.execute("SELECT * FROM garden_beds")
    beds = cursor.fetchall()
    conn.close()
    return render_template('garden_beds.html', beds=beds)

if __name__ == '__main__':
    app.run(debug=True)
