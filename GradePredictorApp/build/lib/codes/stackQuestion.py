from flask import render_template
from app import app

import sqlite3, json

@app.route('/')
@app.route('/index')
def index():
    table_names = nav_bar()
    return render_template('index.html',title='Homepage',table_names = table_name)
def nav_bar():
    connection = sqlite3.connect('C:\\SQLite\\Databases\\testPython.db')
    cursor = connection.cursor()

    cursor.execute('SELECT NAME FROM sqlite_master WHERE TYPE = \'table\';')
        #ORDER BY NAME ASC
        #tableNames = cursor.fetchall()

    connection.close()

    table_names = json.dumps(cursor.fetchall()).replace("\"], [\"", " ").replace("[[\"","").replace("\"]]","").replace("access_","").split()

    return table_names

@app.route('/', methods=['GET','POST'])
def home():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":
            data = c.execute("SELECT * FROM users WHERE username=(%s)", thwart(request.form["username"]))
            data = c.fetchone()[2]
            if sha256_crypt.veryify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash("You are now logged in")
                return redirect(url_for("home"))
            else:
                error = "Invalid try again"
        gc.collect()
        return render_template("index.html", error=error)
    except Exception as e:
        flash(e)
        return render_template("index.html", error=error)
