from flask import Flask, jsonify, request, redirect, render_template
import json
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Atlas setup - replace with your connection string
MONGO_URI = "your_mongo_uri_here"
client = MongoClient(MONGO_URI)
db = client['flaskdb']
collection = db['entries']

DATA_FILE = 'data.json'

@app.route('/api', methods=['GET'])
def get_data():
    if not os.path.exists(DATA_FILE):
        return jsonify([])  # Return empty list if file doesn't exist

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')

            # Insert into MongoDB Atlas
            collection.insert_one({'name': name, 'email': email})

            return redirect('/success')
        except Exception as e:
            return render_template('form.html', error=str(e))
    return render_template('form.html')

@app.route('/success')
def success():
    return "Data submitted successfully"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
