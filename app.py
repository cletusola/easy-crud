from flask import Flask, render_template, url_for, request, redirect 

from  models import db, Todo


app = Flask(__name__)

#configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

#create the database tables
with app.app_context():
    db.create_all()


# home page and add task 
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Unable to add task" 
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# edit/update task 
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_task(id):
    task = Todo.query.get(id)
    if request.method == 'POST':
        try:
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            return "unable to update task"
    return render_template('update.html', task=task)


# delete task 
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "Thers was a problem deleting your task"    


if __name__ == "__main__":
    app.run(debug=True)