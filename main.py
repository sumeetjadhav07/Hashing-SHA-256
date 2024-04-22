from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import mysql.connector

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bdsm6969",
    database="pizzahouse"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        cursor.execute("INSERT INTO employees (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        db.commit()

        return "Registration successful!"

    return render_template('register.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = hash_password(password)
        cursor.execute("SELECT password_hash FROM employees WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            result_str = str(result)
            input_string = result_str
            characters_to_remove = "',()"

            # Remove specified characters
            output_string = input_string
            for char in characters_to_remove:
                output_string = output_string.replace(char, '')

            if output_string == password:
                return render_template('index.html')
            else:
                msg = "Invalid username or password. Please try again."

    return render_template('login.html', msg=msg)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
