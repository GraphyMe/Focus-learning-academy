import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


teacher_credentials = {"username": "Shimaa Robaa", "password": "controlpanel"}


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == teacher_credentials[
            'username'] and password == teacher_credentials['password']:
        return redirect(url_for('control_panel'))
    else:
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE username = ?',
                               (username, )).fetchone()
        conn.close()

        if student and student['password'] == password:
            return redirect(url_for('student_dashboard', student=username))
        else:
            return "Invalid credentials, please try again."


@app.route('/controlpanel')
def control_panel():
    return render_template('controlpanel.html')


@app.route('/dashboard/<student>', methods=['GET'])
def student_dashboard(student):
    conn = get_db_connection()
    student_data = conn.execute('SELECT * FROM students WHERE username = ?',
                                (student, )).fetchone()
    conn.close()

    if student_data:
        directories = {
            "Evaluations": student_data['evaluations'].split('\n') if student_data['evaluations'] else []
        }
        return render_template('dashboard.html',
                               student=student,
                               directories=directories)
    else:
        return "Student not found."

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_name = request.form['name']
        student_password = 'Focus2024'
        student_age = request.form['age']
        student_grade = request.form['grade']

        conn = get_db_connection()

        # Check if the username already exists
        existing_student = conn.execute('SELECT * FROM students WHERE username = ?',
                                       (student_name, )).fetchone()

        if existing_student:
            conn.close()
            return f"Student with username '{student_name}' already exists!"

        # Insert the new student if username is unique
        conn.execute(
            'INSERT INTO students (username, password, age, grade) VALUES (?, ?, ?, ?)',
            (student_name, student_password, student_age, student_grade))
        conn.commit()
        conn.close()

        return f"Student {student_name} added successfully!"
    return render_template('add_student.html')


@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if request.method == 'POST':
        student_name = request.form['name']

        conn = get_db_connection()
        conn.execute('DELETE FROM students WHERE username = ?',
                     (student_name, ))
        conn.commit()
        conn.close()

        return f"Student {student_name} deleted successfully!"
    return render_template('delete_student.html')


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    if request.method == 'POST':
        student_name = request.form['name']
        student_age = request.form.get('age')
        student_grade = request.form.get('grade')

        conn = get_db_connection()
        if student_age:
            conn.execute('UPDATE students SET age = ? WHERE username = ?',
                         (student_age, student_name))
        if student_grade:
            conn.execute('UPDATE students SET grade = ? WHERE username = ?',
                         (student_grade, student_name))
        conn.commit()
        conn.close()

        return f"Student {student_name} updated successfully!"
    return render_template('edit_student.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        student_name = request.form['name']
        student_feedback = request.form['feedback']

        conn = get_db_connection()
        conn.execute('UPDATE students SET feedback = ? WHERE username = ?',
                     (student_feedback, student_name))
        conn.commit()
        conn.close()

        return f"Feedback for {student_name} submitted successfully!"
    return render_template('feedback.html')


@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    if request.method == 'POST':
        student_name = request.form['name']
        assignment = request.form['assignment']

        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE username = ?',
                               (student_name, )).fetchone()
        if student:
            assignments = student['assignments'] or ''
            assignments += f"{assignment}\n"
            conn.execute(
                'UPDATE students SET assignments = ? WHERE username = ?',
                (assignments, student_name))
            conn.commit()
            conn.close()

            return f"Assignment added for {student_name}!"
        else:
            conn.close()
            return f"Student {student_name} not found!"
    return render_template('add_assignment.html')


@app.route('/add_evaluation', methods=['GET', 'POST'])
def add_evaluation():
    if request.method == 'POST':
        student_name = request.form['name']
        evaluation = request.form['evaluation']

        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE username = ?',
                               (student_name, )).fetchone()
        if student:
            existing_evaluations = student['evaluations'] or ''
            updated_evaluations = f"{existing_evaluations}\n{evaluation}".strip()
            conn.execute('UPDATE students SET evaluations = ? WHERE username = ?',
                         (updated_evaluations, student_name))
            conn.commit()
            conn.close()

            return f"Evaluation added for {student_name}!"
        else:
            conn.close()
            return f"Student {student_name} not found!"
    # For GET requests, you may want to show a form or a message
    return render_template('add_evaluation.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
