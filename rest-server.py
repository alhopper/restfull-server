#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
import redis
import sys

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
print "pool called"
sys.stdout.flush()
global r 
r = redis.Redis(connection_pool=pool)


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def get_all_tasks():
    tasks = []
    k = r.keys()
    if k is not None:
        for key in k:
            d = retrieve_by_id(key)
            tasks.append(d)
    print "tasks", tasks
    sys.stdout.flush()
    return tasks


def retrieve_by_id(rec):
    d = {}
    keys = ['id', 'title', 'description', 'done']
    vals = r.hmget(rec, keys)
    if vals[0] is not None:
        d = dict(zip(keys, vals))
        d['id'] = int(d['id'])
    return d
    
def store_by_id(rec, d):
    keys = ['id', 'title', 'description', 'done']
    r.hmset(rec, d)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task
    
@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
    tasks = get_all_tasks()
    return jsonify( { 'tasks': map(make_public_task, tasks) } )

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
@auth.login_required
def get_task(task_id):
    task = []
    d = retrieve_by_id(task_id)
    task.append(d)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': make_public_task(task[0]) } )

@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    keys = r.keys()
    if len(keys) > 0:
        kint = map(int, keys)
        kint.sort()
        id = kint[-1] + 1
    else:
        id = 1
    task = {
        'id': id,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    store_by_id(id, task)
    return jsonify( { 'task': make_public_task(task) } ), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    d = retrieve_by_id(task_id)
    print 'retrieved:', d
    sys.stdout.flush()
    if not d:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    dnew = {}
    dnew['title'] = request.json.get('title', d['title'])
    dnew['description'] = request.json.get('description', d['description'])
    dnew['done'] = request.json.get('done', d['done'])
    dnew['id'] = task_id
    task = []
    task.append(dnew)
    store_by_id(task_id, dnew)
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    d = retrieve_by_id(task_id)
    if not d:
        abort(404)
    r.hdel(task_id, 'id', 'title', 'description', 'done')
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)
