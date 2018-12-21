import json
import dbconnection
from flask import Flask, request, Response, render_template, redirect, url_for,session,flash
from functools import wraps
import bcrypt
app = Flask(__name__)

users = []

def init_list():
    
    users[:] = []
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    cursor.execute('''SELECT * FROM Users''')
    for row in cursor:
        user = {"id":row[0], "username":row[1], "password":row[2], "firstname":row[3], "lastname":row[4]}
        users.append(user)
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('signin'))
    return wrap

# index
@app.route('/users/all')
def get_users():
    init_list()
    return render_template('users.html', result = users)

@app.route('/dashboard')
@is_logged_in
def dashboard():
    init_list()
    return render_template('users.html', result = users)


# find user by id
@app.route('/users/<id>')
def edit_user(id):
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    cursor.execute('''SELECT * FROM Users WHERE Id = ? ''', (id,))
    row = cursor.fetchone()
    user = {"id":row[0], "username":row[1], "password":row[2], "firstname":row[3], "lastname":row[4]}
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return render_template('user.html', user = user)

# new user form
@app.route('/users/newuser')
def new_user():
    return render_template('newuser.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
    
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()


    if request.method == 'POST':
        #Get Form Fields
        username = request.form['username']
        password = request.form['password']
        
        cursor.execute("SELECT username,password FROM Users WHERE username = ?", [username])
        result = cursor.fetchone()
        print(result)
        if cursor.rowcount==0:
            error = 'Invalid Username/Passowrd'
            return render_template('signin.html',error=error)
        
        else:
            passwd = result[1]
            #if bcrypt.hashpw(password.encode('utf-8'), passwd) == passwd:
            if passwd==password:
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))

            else:
                error = 'Invalid Username/Passowrd'
                return render_template('signin.html',error=error)

    return render_template('signin.html')

# Check if user logged in

# add user to database
@app.route('/users/newuser/add', methods = ['POST'])
def add_new_user():
    user = request.form
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    
    #If you want to encrypt password uncomment below 2 lines
    #salt = bcrypt.gensalt()
    #pword=bcrypt.hashpw(pword.encode('utf-8'),salt)

    cursor.execute('''INSERT INTO Users(Username, Password, Firstname, Lastname) VALUES(?, ?, ?, ?)''', (uname, pword, fname, lname))    
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return redirect(url_for('get_users'))

# update user information
@app.route('/users/update', methods = ['PUT', 'POST'])
def update_user():
    user = request.form
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    cursor.execute('''UPDATE Users SET Username = ?, Password = ?, Firstname = ?, Lastname = ? WHERE Id = ? ''', (uname, pword, fname, lname, user['id']))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return redirect(url_for('get_users'))

@app.route('/users/delete', methods = ['DELETE', 'POST'])
def delete_user():
    user = request.form
    dbconnection.db_conn.init_app(app)
    dbconnection.db_conn.connection.execute('''DELETE FROM Users WHERE Id = ? ''', (user['id'],))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return redirect(url_for('get_users'))

# for easy routing
@app.route('/')
def index_site():
    return redirect(url_for('get_users'))

@app.route('/users')
def user_index():
    return redirect(url_for('get_users'))

# JSON, CRUD functions for postman testing

@app.route('/users/json/all')
def get_users_json():
    init_list()
    u = json.dumps(users, indent=True)
    resp = Response(u, status=200, mimetype='application/json')
    return resp

@app.route('/users/json/<username>')
def get_user_json(username):
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    cursor.execute('''SELECT * FROM Users WHERE Username = ? ''', (username,))
    dbconnection.db_conn.commit()
    row = cursor.fetchone()
    return json.dumps({"id":row[0], "username":row[1], "password":row[2], "firstname":row[3], "lastname":row[4]}, indent=True)

@app.route('/users/json/add', methods = ['POST'])
def add_new_user_json():
    user = request.get_json(force=True)
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    cursor.execute('''INSERT INTO Users(Username, Password, Firstname, Lastname) VALUES(?, ?, ?, ?)''', (uname, pword, fname, lname))    
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return json.dumps(user, indent=True)

@app.route('/users/json/update', methods = ['PUT', 'POST'])
def update_user_json():
    user = request.get_json(force=True)
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    uname = str(user['username'])
    pword = str(user['password'])
    fname = str(user['firstname'])
    lname = str(user['lastname'])
    cursor.execute('''UPDATE Users SET Username = ?, Password = ?, Firstname = ?, Lastname = ? WHERE Id = ? ''', (uname, pword, fname, lname, user['id']))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return json.dumps(user, indent=True)

@app.route('/users/json/delete', methods = ['DELETE','POST'])
def delete_user_json():
    user = request.get_json(force = True)
    dbconnection.db_conn.init_app(app)
    dbconnection.db_conn.connection.execute('''DELETE FROM Users WHERE Id = ? ''', (user['id'],))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return "Success!"

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('signin'))

if __name__ == '__main__':
    app.secret_key='test'
    app.run(debug = True)