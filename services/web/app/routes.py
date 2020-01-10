from flask import render_template
from app import app
from flask import jsonify

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'MonetDB'}
    return render_template('index.html', title='Home', user=user)

@app.route('/api/get_benchmarks')
def get_benchmarks():
    data = {"results": ["TPCH-1","TPCH-10","TPCH-100","TPCH-10000"]}
    return jsonify(data)

@app.route('/about')
def about():
    return render_template('about.html', document='Lalalala lalalalla')


@app.route('/api/get_workers')
def get_workers():
    data =  [
    {
        "name": "Tiger Nixon",
        "position": "System Architect",
        "salary": "$320,800",
        "start_date": "2011/04/25",
        "office": "Edinburgh",
        "extn": "5421"
    },
    {
        "name": "Timmy Intern",
        "position": "Intern",
        "salary": "$40,800",
        "start_date": "2018/04/25",
        "office": "Edinburgh",
        "extn": "5421"
    },
    {
        "name": "Hardcore Henry",
        "position": "Junior Developer",
        "salary": "$120,800",
        "start_date": "2016/04/25",
        "office": "Edinburgh",
        "extn": "5421"
    },
    {
        "name": "Jimmy Yang",
        "position": "Senior Developer",
        "salary": "$220,800",
        "start_date": "2015/04/25",
        "office": "Edinburgh",
        "extn": "5421"
    }
    ]
    return jsonify(data)



