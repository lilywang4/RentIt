import json

from flask import Flask, render_template, request
from flask import abort
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypassword'
app.config['MYSQL_DATABASE_DB'] = 'cs6400_sfa17_team033'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_HOST'] = 'mysql'  # mysql is the name of the docker container
mysql.init_app(app)

json_content = {'ContentType': 'application/json'}


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/old")
def old_hello():
    return render_template('index_old.html')

@app.route("/addtool")
def add_tool():
    # code here
    # grab data from request
    # request data to database
    # DB gives results
    # result to json
    return json.dumps(
        {'success': True}),\
           200, json_content

@app.route("/customer/login", methods=['POST'])
def login():
    login_info = request.json

    if login_info['type'] == 'customer':
        sql_statement = "SELECT password from Customer as c where c.user_name = '{}';".format(login_info['username'])
    elif login_info['type'] == 'clerk':
        sql_statement = "SELECT password from Clerk as c where c.user_name = '{}';".format(login_info['username'])

    cursor = mysql.connect().cursor()
    try:
        cursor.execute(sql_statement)
        result = cursor.fetchall()
    finally:
        cursor.close()

    if cursor.rownumber != 1:
        return json.dumps(
            {'success': False,
             'type': login_info['type'],
             'message': 'There is no {} with username {}'.format(login_info['type'], login_info['username'])
             }), \
               400, json_content

    pw = result[0][0]

    if login_info["password"] == pw:
        return json.dumps({'success': True,
                           'type': login_info['type'],
                           'username': login_info['username']
                           }), 200, json_content
    else:
        return json.dumps(
            {'success': False,
             'type': login_info['type'],
             'message': 'Password is incorrect for {}'.format(login_info['username'])
             }), \
               400, json_content


@app.route("/myindex")
def myindex():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from Persons")
    data = cursor.fetchall()

    return render_template('index_old.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
