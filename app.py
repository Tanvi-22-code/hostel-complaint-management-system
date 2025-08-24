from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pandas as pd
import os

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Root@1234',  
        database='hostel_complaints',
        cursorclass=pymysql.cursors.DictCursor
    )

def update_excel_from_db(excel_path: str = "complaints.xlsx"):
    """
    Mirror the MySQL complaints table into an Excel file.
    Overwrites the file so Excel always matches DB after add/edit/delete.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM complaints')
            complaints = cursor.fetchall()  # list[dict]
    finally:
        conn.close()

    # Convert to DataFrame (keeps columns in a consistent order)
    if complaints:
        # Ensure predictable column order
        preferred_cols = ["id", "username", "room_number", "category", "description", "date", "priority"]
        # Create DataFrame and reorder/ensure all columns exist
        df = pd.DataFrame(complaints)
        for col in preferred_cols:
            if col not in df.columns:
                df[col] = None
        df = df[preferred_cols]
    else:
        # Empty table: create an empty DataFrame with headers
        df = pd.DataFrame(columns=["id", "username", "room_number", "category", "description", "date", "priority"])

    # Write to Excel
    try:
        df.to_excel(excel_path, index=False, engine="openpyxl")
        print(f"[Excel Sync] Wrote {len(df)} rows to {excel_path}")
    except Exception as e:
        # Do not crash the request if Excel is locked; just log
        print(f"[Excel Sync] Failed to write Excel: {e}")

@app.route('/')
def index():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM complaints')
            complaints = cursor.fetchall()
    finally:
        conn.close()
    return render_template('index.html', complaints=complaints)

@app.route('/add_complaint', methods=['POST'])
def add_complaint():
    username = request.form['username']
    room_number = request.form['room_number']
    category = request.form['category']
    description = request.form['description']
    priority = request.form['priority']

    # 1) Save to MySQL 
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO complaints (username, room_number, category, description, priority) VALUES (%s, %s, %s, %s, %s)',
                (username, room_number, category, description, priority)
            )
        conn.commit()
    finally:
        conn.close()

    # 2) Mirror to Excel from DB
    update_excel_from_db()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM complaints WHERE id = %s', (id,))
            complaint = cursor.fetchone()
    finally:
        conn.close()

    if request.method == 'POST':
        username = request.form['username']
        room_number = request.form['room_number']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']
        priority = request.form['priority']

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE complaints SET username = %s, room_number = %s, category = %s, description = %s, date = %s, priority = %s WHERE id = %s',
                    (username, room_number, category, description, date, priority, id)
                )
            conn.commit()
        finally:
            conn.close()

        # Mirror to Excel
        update_excel_from_db()
        return redirect(url_for('index'))

    return render_template('edit.html', complaint=complaint)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM complaints WHERE id = %s', (id,))
            # Re-sequence IDs after deletion (per your earlier requirement)
            cursor.execute('SET @count = 0;')
            cursor.execute('UPDATE complaints SET id = @count:=@count+1;')
            cursor.execute('ALTER TABLE complaints AUTO_INCREMENT = 1;')
        conn.commit()
    finally:
        conn.close()

    # Mirror to Excel
    update_excel_from_db()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initial Excel sync on server start (optional)
    try:
        update_excel_from_db()
    except Exception as e:
        print(f"[Startup] Excel sync skipped: {e}")
    app.run(debug=True)
