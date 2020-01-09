from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'MonetDB'}
    return render_template('index.html', title='Home', user=user)

@app.route('/table')
def table():
    data = [['1','column', 'size', 'type'], ['2','saylors', '8192', 'int'], ['3','ships', '8192', 'int']]
    return render_template('tables.html', title='Table', data=data)

@app.route('/about')
def about():
    return render_template('about.html', document='Lalalala lalalalla')


