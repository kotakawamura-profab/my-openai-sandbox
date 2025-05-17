from flask import Flask, jsonify, request, render_template
from task_manager import TaskManager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    manager = TaskManager.load()
    tasks = [{'description': t.description, 'completed': t.completed} for t in manager.list_tasks()]
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'error': 'Description required'}), 400
    manager = TaskManager.load()
    manager.add_task(data['description'])
    return jsonify({'status': 'ok'})

@app.route('/api/tasks/<int:index>/complete', methods=['POST'])
def complete_task(index):
    manager = TaskManager.load()
    manager.complete_task(index)
    return jsonify({'status': 'ok'})

@app.route('/api/tasks/<int:index>', methods=['DELETE'])
def delete_task(index):
    manager = TaskManager.load()
    manager.delete_task(index)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
