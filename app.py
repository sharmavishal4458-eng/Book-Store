from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
app = Flask(__name__)
app.secret_key = 'secret123'   # required for login session

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

books = [
    {"id": 1, "title": "Python Basics", "price": 299, "image": "/static/images/python.jpg"},
    {"id": 2, "title": "Flask Web Development", "price": 399, "image": "/static/images/flask.jpg"},
    { "id": 3, "title": "Data Science with Python", "price": 499, "image": "/static/images/data.jpg"},
    { "id": 4, "title": "Machine Learning", "price": 599, "image": "/static/images/java.jpg"},
    { "id": 5, "title": "Deep Learning", "price": 699, "image": "/static/images/javascript.jpg"},
    { "id": 6, "title": "Python for Data Analysis", "price": 399, "image": "/static/images/python programming.jpg"}
]

cart = []

# Home
@app.route('/')
def home():
    return render_template('index.html', books=books)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return "User already exists ❌"
        
        users[username] = password
        return redirect('/index.html')

    return render_template('signup.html')
# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":
            session['admin'] = True
            return redirect('/admin')   # 👈 direct admin page
        else:
            return "Invalid Credentials ❌"

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

# Admin Panel (Protected)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        file = request.files['image']

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            new_book = {
                "id": len(books) + 1,
                "title": title,
                "price": int(price),
                "image": f"/static/images/{file.filename}"
            }

            books.append(new_book)

        return redirect(url_for('home'))

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)