restfull-server
===============

Demo RESTfull server with a Redis persistant store

Introduction
------------

The project goal is to create a simple RESTfull web service with a Redis
(backend) persistent store.  This code is based on Miguel Grinbergs Flask
Restful tools and his RESTfull tutorial code.  You'll notice I made no 
attempt to disguise the fact that I'm re-using this code.


What does it do
---------------

This service provides a very simply ToDo list with the following data fields:

'id':           the integer task ID 
'title':        the title of the ToDo task
'description':  a description of the ToDo task
'done':         a boolean to indicated if this task is complete

The data is inserted and retrieved in JSON format.
All ToDo tasks are referenced by their task ID

How can I test it
-----------------

The simplist way to test this service, assuming you can run the curl
tool (easily installed on any Linux server), is to issue the RESTfull
calls using curl as described in the following sample commands:


* to add add a task: 
    curl -u miguel:python  -i -X POST -H "Content-Type: application/json" -d '{ "title": "Buy computer hardware", "description": "CPUs, Disks, RAM"  }' http://127.0.0.1:5000/todo/api/v1.0/tasks

* to list all current tasks:
    '''
    curl -u miguel:python -i  http://127.0.0.1:5000/todo/api/v1.0/tasks
    '''

* to list a specific task (in this example - task #1):
    '''
    curl -u miguel:python -i  http://127.0.0.1:5000/todo/api/v1.0/tasks/1
    '''

* to delete a specific task (in this example - task #3):
    '''
    curl -u miguel:python  -i -X DELETE http://127.0.0.1:5000/todo/api/v1.0/tasks/3
    '''

* to modify a task (in this example - task #1):
    '''
    curl -u miguel:python  -i -X PUT -H "Content-Type: application/json" -d '{ "title": "Buy computer hardware", "description": "don't do it!" }' http://127.0.0.1:5000/todo/api/v1.0/tasks/1
    '''



