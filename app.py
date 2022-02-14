from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)


db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():

    if "username" in request.form:

        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO py_user(user_name, password, email) VALUES (%s, %s, %s)",(username,password,email))
        mysql.connection.commit()

    if "link" in request.form:
        cur = mysql.connection.cursor()
        result_value = cur.execute("SELECT * FROM py_user")

        users = cur.fetchall()
        return render_template('recount.html', users = users)

    return render_template ('index.html')



@app.route('/recount', methods = ['GET', 'POST'])
def recount():

    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM py_user")

    users = cur.fetchall()
    return render_template('recount.html', user = users)

@app.route('/port', methods=['GET','POST'])
def port():

    return render_template ('portfolio.html')

if __name__ == '__main__':
    app.run(debug = True)
