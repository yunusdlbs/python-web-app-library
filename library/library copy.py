from crypt import methods
from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)


app.secret_key = 'mysecret'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'library'
app.config['MYSQL_PORT'] = 9906
app.config["MYSQL_UNIX_SOCKET"] = None
app.config["MYSQL_CONNECT_TIMEOUT"] = 10
app.config["MYSQL_READ_DEFAULT_FILE"] = None
app.config["MYSQL_USE_UNICODE"] = True
app.config["MYSQL_CHARSET"] = "utf8"
app.config["MYSQL_SQL_MODE"] = None
app.config["MYSQL_CURSORCLASS"] = None
app.config["MYSQL_AUTOCOMMIT"] = False
app.config["MYSQL_CUSTOM_OPTIONS"] = None


mysql = MySQL()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('login.html')
    
@app.route('/index')
def index():
    topic = request.args.get('topic')
    if topic:
        cur = mysql.connection.cursor()
        cur.execute(f"select book_name, book_photo, book_topic, book_writer, book_summary from books where book_topic='{topic}'")
        books = cur.fetchall()
        cur.close()
        return render_template('index.html', kitaplar=books, username=session['username'])

    else: 
        cur = mysql.connection.cursor()
        cur.execute(f"select book_name, book_photo, book_topic, book_writer, book_summary from books")
        books = cur.fetchall()
        cur.close()
        return render_template('index.html', kitaplar=books, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        # user = db.get("user",{"username":username,"password":pwd})
        # if user :
        #     session['username'] = user[0]
        #     return redirect(url_for('home'))
        # else:
        #     return render_template('login.html', error='Invalid username or password')
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from users where username ='{username}'")
        user = cur.fetchone()
        cur.close()
        if user and pwd == user[1]:
            session['username'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='!!! Kullanıcı Adı veya Şifre Hatalı, Tekrar Deneyiniz...')
    else:
        session.clear()
        return render_template('login.html')

@app.route('/registry', methods=['GET','POST'])
def registry():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f"insert into users (username, email, password) values('{username}', '{email}', '{pwd}')")
        mysql.connection.commit()
        cur.close()
        return render_template('registry.html', valid='Tebrikler ! Kaydınız başarı ile yapıldı.')
    return render_template('registry.html')

@app.route('/kitapdetay')
def kitapdetay():
    book_name = request.args.get('book_name')
    cur = mysql.connection.cursor()
    cur.execute(f"select * from books where book_name='{book_name}'")
    book = cur.fetchone()
    cur.close()
    return render_template('kitapdetay.html', kitap_detay=book, username=session['username'])

@app.route('/oduncal', methods=['GET','POST'])
def oduncal():from crypt import methods
from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import functions

app = Flask(__name__)


app.secret_key = 'mysecret'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'library'
app.config['MYSQL_PORT'] = 9906
app.config["MYSQL_UNIX_SOCKET"] = None
app.config["MYSQL_CONNECT_TIMEOUT"] = 10
app.config["MYSQL_READ_DEFAULT_FILE"] = None
app.config["MYSQL_USE_UNICODE"] = True
app.config["MYSQL_CHARSET"] = "utf8"
app.config["MYSQL_SQL_MODE"] = None
app.config["MYSQL_CURSORCLASS"] = None
app.config["MYSQL_AUTOCOMMIT"] = False
app.config["MYSQL_CUSTOM_OPTIONS"] = None


mysql = MySQL()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('login.html')
    
@app.route('/index')
def index():
    topic = request.args.get('topic')
    if topic:
        cur = mysql.connection.cursor()
        cur.execute(f"select book_name, book_photo, book_topic, book_writer, book_summary from books where book_topic='{topic}'")
        books = cur.fetchall()
        cur.close()
        return render_template('index.html', kitaplar=books, username=session['username'])

    else: 
        cur = mysql.connection.cursor()
        cur.execute(f"select book_name, book_photo, book_topic, book_writer, book_summary from books")
        books = cur.fetchall()
        cur.close()
        return render_template('index.html', kitaplar=books, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        # user = db.get("user",{"username":username,"password":pwd})
        # if user :
        #     session['username'] = user[0]
        #     return redirect(url_for('home'))
        # else:
        #     return render_template('login.html', error='Invalid username or password')
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from users where username ='{username}'")
        user = cur.fetchone()
        cur.close()
        if user and pwd == user[1]:
            session['username'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='!!! Kullanıcı Adı veya Şifre Hatalı, Tekrar Deneyiniz...')
    else:
        session.clear()
        return render_template('login.html')

@app.route('/registry', methods=['GET','POST'])
def registry():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f"insert into users (username, email, password) values('{username}', '{email}', '{pwd}')")
        mysql.connection.commit()
        cur.close()
        return render_template('registry.html', valid='Tebrikler ! Kaydınız başarı ile yapıldı.')
    return render_template('registry.html')

@app.route('/kitapdetay')
def kitapdetay():
    book_name = request.args.get('book_name')
    cur = mysql.connection.cursor()
    cur.execute(f"select * from books where book_name='{book_name}'")
    book = cur.fetchone()
    cur.close()
    return render_template('kitapdetay.html', kitap_detay=book, username=session['username'])

@app.route('/oduncal', methods=['GET','POST'])
def oduncal():
    book_name = request.form['book_name']
    cur = mysql.connection.cursor()
    cur.execute(f"select * from books where book_name='{book_name}'")
    book = cur.fetchone()
    cur.execute(f"select book_writer from books where book_name='{book_name}'")
    book_writer = cur.fetchone()
    username=session['username']
    cur.execute(f"select email from users where username='{username}'")
    user_mail = cur.fetchone()
    borrowed_date = datetime.now().date()
    due_date = borrowed_date + timedelta(days=10)
    cur.execute(f"INSERT INTO borrowed (book_name, book_writer, who_borrowed, email, when_borrowed, due_time) VALUES (%s, %s, %s, %s, %s, %s)", (book_name, book_writer, username, user_mail, borrowed_date, due_date))
    mysql.connection.commit()
    cur.close()
    #functions.borrow_mail(book_name)
    return render_template('oduncal.html', kitap_detay=book, username=session['username'])

@app.route('/odunckitaplist')
def odunckitaplist():
    cur = mysql.connection.cursor()
    username=session['username']
    cur.execute(f"select * from borrowed where who_borrowed='{username}'")
    book = cur.fetchall()
    cur.close()
    return render_template('odunckitaplist.html',borrowed_books=book, username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ =='__main__':
    app.run(debug=True)
    #book_name = request.args.get('book_name')
    book_name = request.form['book_name']
    cur = mysql.connection.cursor()
    cur.execute(f"select * from books where book_name='{book_name}'")
    book = cur.fetchone()
    cur.close()
    return render_template('oduncal.html', kitap_detay=book, username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ =='__main__':
    app.run(debug=True)