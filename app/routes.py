from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# In-memory task store
tasks = []
_id_counter = 1


def get_next_id():
    global _id_counter
    tid = _id_counter
    _id_counter += 1
    return tid


def reset_store():
    global tasks, _id_counter
    tasks = []
    _id_counter = 1


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200


@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title', '').strip():
        return jsonify({'error': 'Title is required'}), 400
    task = {
        'id': get_next_id(),
        'title': data['title'].strip(),
        'done': False,
        'created_at': datetime.utcnow().isoformat()
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def toggle_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    task['done'] = not task['done']
    return jsonify(task), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'deleted': task_id}), 200


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'tasks_count': len(tasks)}), 200
