from flask import Flask, render_template, request, redirect, url_for
from models import db, Todo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

try:
    with app.app_context():
        db.create_all()
    print("Database tables created successfully.")
except Exception as e:
    print("An error occurred while creating the database tables:", str(e))

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

"""@app.route('/process_date', methods=['POST'])
def process_date():
    selected_date = request.form['date']
    return f'You selected the date: {selected_date}'"""

@app.route('/add', methods=['GET','POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    new_todo = Todo(content=content, title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')

#Updating Todo Records
@app.route('/update/<int:id>',  methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        title = request.form['title']
        content = request.form['content']
        todo =Todo.query.filter_by(id=id).first()
        todo.title=title
        todo.content=content
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo =Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)
    

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/search/<int:id>')
def search(id):
    query = request.args.get('query', '').strip()  # Get the search query from the form
    filtered_todos = [todo for todo in Todo if query.lower() in todo['content'].lower()]
    return render_template('index.html', todos=filtered_todos)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
