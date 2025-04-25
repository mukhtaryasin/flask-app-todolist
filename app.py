from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)
todos = []
trash = []

def cleanup_trash():
    now = datetime.utcnow()
    global trash
    trash = [item for item in trash if now - item['deleted_at'] < timedelta(days=7)]

@app.route('/')
def index():
    cleanup_trash()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        todos.append({
            'task': task,
            'created': datetime.utcnow(),
            'updated': None
        })
    return redirect('/')

@app.route('/edit/<int:index>')
def edit(index):
    if 0 <= index < len(todos):
        return render_template('edit.html', index=index, todo=todos[index])
    return redirect('/')

@app.route('/update/<int:index>', methods=['POST'])
def update(index):
    if 0 <= index < len(todos):
        updated_task = request.form.get('task')
        if updated_task:
            todos[index]['task'] = updated_task
            todos[index]['updated'] = datetime.utcnow()
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(todos):
        item = todos.pop(index)
        item['deleted_at'] = datetime.utcnow()
        trash.append(item)
    return redirect('/')

@app.route('/bin')
def bin():
    cleanup_trash()
    return render_template('bin.html', trash=trash)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) # Change to your desired port
