from flask import Flask, render_template, url_for, redirect, session, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'qwer2345'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'datareg'
mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/proses_login', methods=['GET', 'POST'])
def proses_login():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       username = request.form['username']
       password = request.form['password']
       cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cur.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
       acc = cur.fetchone()

       if acc:
           session['loggedin'] = True
           session['id'] = acc['id_user']
           session['username'] = acc['username']
           mesage = 'Logged in successfully !'
           return render_template('index.html', mesage = mesage, username = username)
       else:
           mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/data_show', methods=['GET', 'POST'])
def data_show():
    x = []
    y = []
    x2 = []
    y2 = []
    xy = []
    ape = []

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dataset")
    query = cur.fetchall()

    def sum_x():
        xs = 0
    
        for i in x:
            xs = xs + int(i)
        return (xs)
    
    def sum_y():
        ys = 0
    
        for i in y:
            ys = ys + int(i)
        return (ys)
    
    def sum_x2():
        x2s = 0
    
        for i in x2:
            x2s = x2s + int(i)
        return (x2s)    

    def sum_y2():
        y2s = 0
    
        for i in y2:
            y2s = y2s + int(i)
        return (y2s)    
    
    def sum_xy():
        xys = 0
    
        for i in xy:
           xys = xys + int(i)
        return (xys)            

    def sum_const_a(y_sum, x2_sum, x_sum, xy_sum, x_data):
        a = y_sum * x2_sum
        b = x_sum * xy_sum
        c = x_data * x2_sum
        d = x_sum ** 2
    
        e = a - b
        f = c - d
    
        g = e / f
        return g
    
    def sum_const_b(x_data, xy_sum, x_sum, y_sum, x2_sum):
        a = x_data * xy_sum
        b = x_sum * y_sum
        c = x_data * x2_sum
        d = x_sum ** 2
    
        e = a - b
        f = c - d
    
        g = e / f
        return g

    for n in query:
        x.append(n[1])
        y.append(n[2])

    for q in range(20):
        w = int(x[q]) ** 2
        x2.append(w)

    for w in range(20):
        m = int(y[w]) ** 2
        y2.append(m)    

    for e in range(20):
        m = int(y[e]) * int(x[e])
        xy.append(m)    

    for i in range(20):
        p = (int(x[i]) - int(y[i])) / int(x[i])
        p = abs(p)
        ape.append(p)

    x_sum = sum_x()
    y_sum = sum_y()
    x2_sum = sum_x2()
    y2_sum = sum_y2()
    xy_sum = sum_xy()
    x_data = len(x)
    const_a = sum_const_a(y_sum, x2_sum, x_sum, xy_sum, x_data)
    const_b = sum_const_b(x_data, xy_sum, x_sum, y_sum, x2_sum)
    mape = sum(ape) / len(ape)
    o = round(mape * 100, 2)
    sub = ''

    if request.method == 'POST' and 'val_prediksi' in request.form:
       sub = request.form['val_prediksi']
       q = const_b * int(sub)
       w = const_a + q
       e = w

    return render_template('data_show.html', x=x, y=y, x2=x2, y2=y2, xy=xy, ape=ape, x_sum=x_sum, y_sum=y_sum, x2_sum=x2_sum, y2_sum=y2_sum, xy_sum=xy_sum, sub=sub, w=w, o=o)

@app.route('/predict_form')
def predict_form():
    return render_template('predict.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()