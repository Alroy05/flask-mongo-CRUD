from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
import os
from dotenv import load_dotenv

app = Flask(__name__, static_url_path='/static')
load_dotenv()  # Load environment variables

conn_str = os.getenv('mongo')
client = MongoClient(conn_str, tlsCAFile=certifi.where())
db = client['Users']
collection = db['information']

# Index page - Show all users
@app.route('/')
def index():
    users = list(collection.find())
    return render_template('users.html', users=users)

# Create a new user
@app.route('/create', methods=['POST'])
def create_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if username.strip() and email.strip() and password.strip():
        collection.insert_one({'username': username, 'email': email, 'password': password})
    return redirect(url_for('index'))

# Update a user
@app.route('/update/<user_id>', methods=['POST'])
def update_user(user_id):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if username.strip() and email.strip() and password.strip():
        collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'username': username, 'email': email, 'password': password}})
    return redirect(url_for('index'))

# Delete a user
@app.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    collection.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
