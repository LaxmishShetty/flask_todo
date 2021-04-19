from flask import Flask, render_template,flash,redirect,request,url_for
import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_task(task_id):
    conn = sqlite3.connect('database.db')
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    if not task:
        abort(404)
    return task


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Duringthesecondffworldwar'


@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)


@app.route('/<int:task_id>')
def task(task_id):
    task = get_task(task_id)
    return render_template('task.html', task=task)

@app.route('/create',methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash("Title enter bhayya")

        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO tasks (title,content) VALUES (?,?)',(title,content))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:task_id>/edit', methods=('GET', 'POST'))
def edit(task_id):
    task = get_task(task_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash("Title enter bhayya")

        else:
            conn = get_db_connection()
            conn.execute('UPDATE tasks SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, task_id))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
    return render_template('edit.html',task=task)

@app.route('/<int:id>/delete',methods=('POST',))
def delete(id):
    task = get_task(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(task[2]))
    return redirect(url_for('index'))

