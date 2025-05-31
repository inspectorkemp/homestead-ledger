# Homestead Tracking Web App

A minimalist Python Flask web app for tracking your homestead's gardens, crops, chickens, pets, and equipment using a MySQL database.

## Features

- **Garden Beds**: Add, edit, and delete garden bed records.
- **Crops**: Track crop types, varieties, planting/harvest dates, and yields.
- **Chickens**: Manage chickens, egg/meat/dual-purpose, and status.
- **Pets**: Register pets, manage health and status.
- **Equipment**: Track equipment, purchase, maintenance, and status.
- **General Notes**: Add and review notes for any category.
- **Simple CRUD**: All data can be created, viewed, updated, or deleted via the web interface.

## Requirements

- Python 3.13+
- [MySQL server](https://dev.mysql.com/downloads/)
- Pip packages: `Flask`, `mysql-connector-python`  
  *(see [requirements.txt](requirements.txt) for exact versions)*

## Setup

1. **Install MySQL** and create the database and tables:
    - Use your provided SQL schema to create the `homestead` database and tables.
    - Run initialdbsetup.sql against your newly installed instance for the table creation

2. **Clone this repository** and install dependencies:
    ```bash
    git clone <your_repo_url>
    cd <this_project_directory>
    pip install -r requirements.txt
    ```

3. **Configure database connection:**
    - By default, the app uses environment variables for DB connection:
      - `DB_HOST` (default: `localhost`)
      - `DB_USER` (default: `root`)
      - `DB_PASSWORD` (default: `""`)
      - `DB_NAME` (default: `"homestead"`)
    - Set these in your environment or modify `get_db_connection()` in `app.py`.

4. **Run the web app:**
    ```bash
    python app.py
    ```
    - Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Directory Structure

```
.
├── app.py
├── requirements.txt
└── templates/
    ├── home.html
    ├── beds_list.html
    ├── bed_form.html
    ├── crops_list.html
    ├── crop_form.html
    ├── chickens_list.html
    ├── chicken_form.html
    ├── pets_list.html
    ├── pet_form.html
    ├── equipment_list.html
    ├── equipment_form.html
    └── notes_list.html
```

## Usage

- Use the navigation links on the homepage to manage each category.
- Add, edit, and delete entries as needed.
- All changes are stored in your MySQL database.

## Notes

- This project is intentionally simple—no authentication, no JavaScript, no frontend frameworks.
- You can extend it to add features like login, search, or reporting.
- For production, consider running with a WSGI server (e.g., gunicorn) and behind a reverse proxy.

## License

MIT License

---

*Happy homesteading!*
