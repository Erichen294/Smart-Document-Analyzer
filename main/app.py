from flask import Flask, render_template, request, redirect, url_for, session
import requests
import database
import summarizer
import ingester
import summarize_webpage
from urllib.error import HTTPError

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
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post(f"http://127.0.0.1:5000/api/login", json={'username': username, 'password': password})
        if response.status_code == 200:
            access_token = response.json()['access_token']
            session['access_token'] = access_token
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            message = "Incorrect username or password. Please try again."
    return render_template('login.html', message=message)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'access_token' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'upload_document':
            return redirect(url_for('upload_document'))
        elif action == 'analyze_document':
            return redirect(url_for('analyze_document'))
        elif action == 'analyze_webpage':
            return redirect(url_for('analyze_webpage'))
        elif action == 'logout':
            session.pop('access_token', None) 
            return redirect(url_for('index'))

    return render_template('dashboard.html')

@app.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if 'access_token' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        document_file = request.files['document']
        if document_file:
            access_token = session['access_token']
            headers = {'Authorization': f'Bearer {access_token}'}
            files = {'document': (document_file.filename, document_file.stream, document_file.mimetype)}
            response = requests.post("http://127.0.0.1:5001/api/upload", headers=headers, files=files)

            if response.status_code == 200:
                message = "File uploaded successfully."
            else:
                message = "Error uploading file. Please try again."

            return render_template('upload_document.html', message=message)
        else:
            message = "No file uploaded. Please select a file to upload."
            return render_template('upload_document.html', message=message)

    return render_template('upload_document.html')

@app.route('/analyze_document', methods=['GET', 'POST'])
def analyze_document():
    if 'access_token' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        file_name = request.form.get('file_name')
        username = session.get('username')

        # Placeholder values for summary, keywords, urls, and tone
        summary, return_val, keywords = summarizer.summarize_document(file_name, username)
        urls = ingester.search_articles(keywords)
        tone = summarizer.analyze_tone(summary)

        return render_template('analyze_document.html', 
                               summary=summary, 
                               keywords=keywords, 
                               urls=urls, 
                               tone=tone)

    return render_template('analyze_document.html')

@app.route('/analyze_webpage', methods=['GET', 'POST'])
def analyze_webpage():
    if request.method == 'POST':
        webpage_url = request.form.get('webpage_url')
        
        summary, return_val = summarize_webpage.summarize_webpage(webpage_url)
        keywords = summarizer.extract_keywords(summary)
        urls = ingester.search_articles(keywords)
        tone = summarizer.analyze_tone(summary)

        return render_template('analyze_webpage.html', 
                               summary=summary,
                               keywords=keywords,
                               urls=urls, 
                               tone=tone)
    # Render the initial form
    return render_template('analyze_webpage.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
