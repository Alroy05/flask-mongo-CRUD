from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
import os
from dotenv import load_dotenv

app = Flask(__name__, static_url_path='/static')
conn_str = os.getenv('mongo')
client = MongoClient(conn_str, tlsCAFile=certifi.where())
db = client['List']
collection = db['task']

# Index page - Show all todos
@app.route('/')
def index():
    todos = list(collection.find())
    return render_template('index.html', todos=todos)

# Create a new todo
@app.route('/create', methods=['POST'])
def create_todo():
    todo = request.form['todo']
    if todo.strip():
        collection.insert_one({'todo': todo})
    return redirect(url_for('index'))

# Update a todo
@app.route('/update/<todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo = request.form['todo']
    if todo.strip():
        collection.update_one({'_id': ObjectId(todo_id)}, {'$set': {'todo': todo}})
    return redirect(url_for('index'))

# Delete a todo
@app.route('/delete/<todo_id>', methods=['POST'])
def delete_todo(todo_id):
    collection.delete_one({'_id': ObjectId(todo_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
