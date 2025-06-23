from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import os
from datetime import datetime
from functools import lru_cache

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TD_temp.csv')

# 确保文件初始化
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['时间', '内容'])

@lru_cache(maxsize=1)
def _get_cached_todos():
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            return [row for row in csv.reader(f)][1:]
    except FileNotFoundError:
        return []

@app.route('/todos')
def get_todos():
    return jsonify([{'time': t, 'content': c} for t, c in _get_cached_todos()])

@app.route('/add', methods=['POST'])
def add_todo():
    content = request.get_json()['content']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([timestamp, content])
    
    _get_cached_todos.cache_clear()
    return jsonify({'time': timestamp, 'content': content}), 201

@app.route('/delete', methods=['POST'])
def delete_todo():
    target_time = request.get_json()['time']
    
    rows = _get_cached_todos()
    filtered = [row for row in rows if row[0] != target_time]
    
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['时间', '内容'])
        writer.writerows(filtered)
    
    _get_cached_todos.cache_clear()
    return jsonify({'status': 'success'})

@app.route('/')
@app.errorhandler(404)
def serve_index(e=None):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
