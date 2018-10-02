
from forms import AddTaskForm, RegisterForm, LoginForm

from datetime import datetime
from functools import wraps
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for

import db

app = Flask(__name__)
app.config.from_pyfile('_config.py')

db.init(app.config['SQLALCHEMY_DATABASE_URI'])

from models import User, Task

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %field -%s" % (
                getattr(form, field).label.text, error), 'error')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            newUser = User(form.name.data, form.email.data, form.password.data, 'user')            
            if db.addNewUser(newUser) == True:
                flash('Thanks for registering. Please login.')
                return redirect(url_for('login'))
            else:
                error = 'Sorry. Unable to register you at this time. There is a duplicate e-mail \
                         or user matching your credentials.'
        else:
            error = 'Please enter a valid e-mail address and a username and password of at least 6 characters.'
    return render_template('register.html', form=form, error=error)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            candidate_user = request.form['name']
            candidate_pwd = request.form['password']
            user = db.getUserCredentials(candidate_user, candidate_pwd)
            if user == None or candidate_pwd != user['password']:
                error = 'Invalid credentials. Please log in.'                
            else:
                session['logged_in'] = True
                session['user_id'] = user['user_id']
                session['role'] = user['role']
                flash('Welcome {}'.format(candidate_user))
                #return render_template('tasks.html')
                return redirect(url_for('tasks'))
                
    return render_template('login.html', form=form, error=error)

@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Goodbye!')
    return redirect(url_for('login'))

# Task-related operations

@app.route('/tasks/', methods = ['GET', 'POST'])
@login_required
def tasks():
    now = datetime.now()
    formatted_now = now.strftime("%-m/%d/%Y")
    form=AddTaskForm(request.form)
    userid = session['user_id']
    open_tasks = db.getOpenTasks(userid)
    closed_tasks = db.getClosedTasks(userid)    
    return render_template('tasks.html', form=form, default_date=formatted_now, 
                            open_tasks=open_tasks, closed_tasks=closed_tasks)

# Add new tasks
@app.route('/add/', methods = ['POST'])
@login_required
def new_task():    
    name = request.form['name']
    date = request.form['due_date']
    priority = request.form['priority']
    userid = session['user_id']
    if not name or not date or not priority:
        flash("All fields are required. Please try again.")
        return redirect(url_for('tasks'))
    else:
        db.add_task(userid, name, date, priority, 1)
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('tasks'))

@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    db.update_task_complete(task_id, True)
    flash('The task was marked as completed.')
    return redirect(url_for('tasks'))

@app.route('/incomplete/<int:task_id>/')
@login_required
def incomplete(task_id):
    db.update_task_complete(task_id, False)
    flash('The task was marked as completed.')
    return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    db.delete_task(task_id)
    flash('The task was marked as deleted.')
    return redirect(url_for('tasks'))


#TODO: I'm getting task values from the db, can I get them from the form's table row?
@app.route('/edit/<int:task_id>/')
@login_required
def edit_entry(task_id):
    task = db.getTaskInfo(task_id)

    task_id = task['task_id']
    name = task['task_name']
    due_date = task['due_date']
    priority = task['priority']

    #name = request.args.get('name', None)
    #due_date =  request.args.get('due_date', None)
    #priority = request.args.get('priority', None)

    return render_template('edit.html', taskToEdit=task)

@app.route('/save_edited_task/<int:task_id>/', methods=['POST'])
@login_required
def save_edited_task(task_id):
    #task_id = request.form.get('task_id', None)

    task_name = request.form.get('name', None)
    task_due_date = request.form.get('due_date', None)
    task_priority = request.form.get('priority', None)

    #db.update_task("taskId", "taskName", "dueDate", "priority")
    db.update_task(task_id, task_name, task_due_date, task_priority)
    return redirect(url_for('tasks'))

