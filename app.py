from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)


db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'super secret key'
mysql = MySQL(app)



@app.route('/', methods = ['GET','POST'])
def index():
    menu_display = 'disabled'

    if request.method == 'POST':

        user_name = request.form.get('user_name', False)
        user_pass = request.form.get('user_pass', False)


        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM py_user")
        user = cur.fetchall()

        for user_fetched in user:

            if user_fetched["user_name"] == user_name and user_fetched["user_pass"] == user_pass:
                sign_in_value = "pass"
                session["sign_in_value"] = sign_in_value
                return menu()

            else:
                sign_in_value = "nopass"
                session["sign_in_value"] = sign_in_value


    return render_template('sign-in.html', menu_display = menu_display)



@app.route('/menu', methods = ['GET','POST'])
def menu():

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        return render_template('menu.html', sign_in_value = sign_in_value)
    else:
        return index()

@app.route('/recount', methods = ['GET','POST'])
def recount():
    selected_view = []

    if request.method == 'POST':
        selected = request.form.getlist('form-check')
        for i in selected:
            print (i)
            selected_view.append(i)
            print(selected_view)
        session['selected'] = selected_view
        return redirect(url_for('selected'))

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM py_db_main ORDER BY created_at")
        recount_data = cur.fetchall()

        # return render_template('db.test.html', view = recount_data)
        return render_template('recount2.html', sign_in_value = sign_in_value, recount_data = recount_data)

    else:
        return index()






@app.route('/selected', methods = ['GET','POST'])
def selected():



    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        selected_view = session['selected'] 

        return render_template('selected.html', sing_in_value = sign_in_value, selected_view = selected_view)

    else:
        return index()





@app.route('/form', methods = ['GET','POST'])
def form():

    statement = "Enter the required data please"
    form_condition = True

    if request.method == "POST":

        name = request.form.get('name', False)
        email = request.form.get('email', False)
        subject = request.form.get('subject', False)
        message = request.form.get('message',False)


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO py_db_main (name, email, subject, message ) VALUES (%s, %s, %s, %s)",(name, email, subject, message))
        mysql.connection.commit()
        statement = "Your Message has been recorded"
        form_condition = False

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        return render_template('form.html', sign_in_value = sign_in_value, statement = statement, form_condition = form_condition)
    else:
        return index()



if __name__ == '__main__':
    app.run(debug = True)
