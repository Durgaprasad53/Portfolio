from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# Create DB table if it doesn't exist
def init_db():
    conn = sqlite3.connect('contact_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Call init_db on import so it runs in Render too
init_db()

@app.route('/')
def home():
    return render_template('index.html')  # HTML must be in 'templates' folder

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('contact_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/messages')
def messages():
    conn = sqlite3.connect('contact_data.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, message FROM contacts")
    messages = c.fetchall()
    conn.close()
    return render_template('messages.html', messages=messages)

@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    conn = sqlite3.connect('contact_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()
    return redirect('/messages')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
