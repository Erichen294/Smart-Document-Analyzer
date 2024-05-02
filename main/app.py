from flask import Flask, render_template, request, redirect, url_for, session
import requests
import database

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form['action'] == 'register':
        return redirect(url_for('register'))
    elif request.method == 'POST' and request.form['action'] == 'login':
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success = database.register_user(username, password)
        
        if success:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', message="User already exists. Please try again.")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form('username')
        password = request.form('password')

        

if __name__ == '__main__':
    app.run(debug=True, port=5002)
