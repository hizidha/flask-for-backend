from flask import Flask, request
from data import todo, generated_id

app = Flask(__name__)

@app.post('/todo/')
def todoHandle():
    data = request.json
        
    if all(key in data for key in ['title', 'tags', 'body']):
        if all(data[key] for key in ['title', 'tags', 'body']):
            new_id = generated_id
            todo_items = {
                'id': new_id,
                'title': data['title'],
                'tags': data['tags'],
                'body': data['body']
            }
            todo.append(todo_items)
                
            response = {
                'message': 'Todo item created successfully',
                'status': 'success', 
                'data': {'id': todo_items['id']},
            }
            return response, 200

    response = {
        'message': 'Title, tags, and body must be provided',
        'status': 'error',
    }
    return response, 400


@app.get('/todo/')
def getAlltodoHandle():
    title = request.args.get('title')
    
    if title:
        title_lower = title.lower()
        filtered_todo = [item for item in todo if title_lower in item['title'].lower()]
        response = {
            'data': filtered_todo,
        }
        return response, 200
    
    response = {
        'data': todo,
    }    
    return response, 200


@app.get('/todo/<todoId>/')
def showitemTodo(todoId):
    for item in todo:
        if item['id'] == todoId:
            response = {
                'data': item,
                'status': 'success',
            }
            return response, 200
    
    response = {
        'message': 'Todo item not found',
        'status': 'error',
    }
    return response, 404


@app.put('/todo/<todoId>/')
def editTodo():
    
    return

@app.delete('/todo/<todoId>/')
def deleteTodo(todoId):
    for index, item in enumerate(todo):
        if item['id'] == todoId:
            titles = item['title']
            del todo[index]
            response = {
                'message': f'Todo with title: {titles}, deleted successfully',
                'status': 'success',
            }
            return response, 200
    
    response = {
        'message': 'Todo item are not found and cant be deleted',
        'status': 'error',
    }
    return response, 404