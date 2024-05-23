from crypt import methods
from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
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

        page = request.args.get('sayfa', 1, type=int)
        per_page = 3
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(books) + per_page -1) // per_page
        books_on_page = books[start:end]

        return render_template('index.html', kitaplar=books_on_page, toplam_sayfa=total_pages, sayfa=page, username=session['username'])
        #return render_template('index.html', kitaplar=books, username=session['username'])

    else: 
        cur = mysql.connection.cursor()
        cur.execute(f"select book_name, book_photo, book_topic, book_writer, book_summary from books")
        books = cur.fetchall()
        cur.close()

        page = request.args.get('sayfa', 1, type=int)
        per_page = 3
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(books) + per_page -1) // per_page
        books_on_page = books[start:end]

        return render_template('index.html', kitaplar=books_on_page, toplam_sayfa=total_pages, sayfa=page, username=session['username'])
        #return render_template('index.html', kitaplar=books, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
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
        #pwd = generate_password_hash(request.form['password'])
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
    cur.execute(f"select borrowed from books where book_name='{book_name}'")
    quantity = int((cur.fetchone())[0]) +1
    cur.execute(f"select present from books where book_name='{book_name}'")
    p_quantity = int((cur.fetchone())[0]) -1

    cur.execute(f"select id from books where book_name='{book_name}'")
    book_id = cur.fetchone()
    username=session['username']
    cur.execute(f"select email from users where username='{username}'")
    user_mail = cur.fetchone()
    borrowed_date = datetime.now().date()
    due_date = borrowed_date + timedelta(days=10)
    cur.execute("update books set borrowed=%s where id=%s", (quantity, book_id) )
    cur.execute("update books set present=%s where id=%s", (p_quantity, book_id) )
    cur.execute(f"INSERT INTO borrowed (book_name, book_writer, who_borrowed, email, when_borrowed, due_time) VALUES (%s, %s, %s, %s, %s, %s)", (book_name, book_writer, username, user_mail, borrowed_date, due_date))
    mysql.connection.commit()
    cur.execute(f"select * from books where book_name='{book_name}'")
    book = cur.fetchone()
    cur.close()
    #functions.borrow_mail(book_name)
    return render_template('oduncal.html', kitap_detay=book, username=session['username'])

@app.route('/odunckitaplist')
def odunckitaplist():
    book = request.args.get('book')
    writer = request.args.get('writer')
    who = request.args.get('who')

    if (book and writer and who):
        cur = mysql.connection.cursor()
        username=session['username']
        cur.execute(f"select id from books where book_name='{book}'")
        book_id = cur.fetchone()
        cur.execute(f"select borrowed from books where book_name='{book}' AND book_writer='{writer}'")
        b_quantity = int((cur.fetchone())[0]) -1
        cur.execute(f"select present from books where book_name='{book}' AND book_writer='{writer}'")
        p_quantity = int((cur.fetchone())[0]) +1
        cur.execute("update books set present=%s where id=%s", (p_quantity, book_id) )
        cur.execute("update books set borrowed=%s where id=%s", (b_quantity, book_id) )
        cur.execute("delete from borrowed where book_name=%s AND book_writer=%s AND who_borrowed=%s",(book, writer, who))
        mysql.connection.commit()
        cur.close()
    cur = mysql.connection.cursor()
    username=session['username']
    cur.execute(f"select * from borrowed where who_borrowed='{username}'")
    book = cur.fetchall()
    cur.close()
    return render_template('odunckitaplist.html',borrowed_books=book, username=session['username'])

@app.route('/kitapekle', methods=['GET','POST'])
def kitapekle():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        book = request.form['book_name']
        writer = request.form['book_writer']
        cur.execute(f"select book_name from books where book_name='{book}'")
        book_in = cur.fetchone()
        cur.execute(f"select book_writer from books where book_name='{book}'")
        writer_in = cur.fetchone()

        if (book==book_in and writer==writer_in):
            cur.execute(f"select book_quantity from books where book_name='{book}'")
            amount = int((cur.fetchone())[0]) +1
            cur.execute("update books set book_quantity=%s where book_name=%s", (amount, book) )
            cur.execute(f"select present from books where book_name='{book}'")
            present = int((cur.fetchone())[0]) +1
            cur.execute("update books set present=%s where book_name=%s", (present, book) )
        else: 
            #book = request.form['book_name']
            photo = request.form['book_photo']
            topic = request.form['book_topic']
            #writer = request.form['book_writer']
            summary = request.form['book_summary']
            page = request.form['book_page']
            quantity = request.form['book_quantity']
            cur = mysql.connection.cursor()
            cur.execute(f"insert into books (book_name, book_photo, book_topic, book_writer, book_summary, book_page, book_quantity, borrowed, present) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (book, photo, topic, writer, summary, page, quantity, "0", quantity))
            mysql.connection.commit()
            cur.close()
            return render_template('kitapekle.html', username=session['username'], value='Kitap başarı ile kaydedildi !')
    return render_template('kitapekle.html', username=session['username'])

@app.route('/forgetpass', methods=['GET','POST'])
def forgetpass():
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f"select username, email from users")
        info = cur.fetchall()
        cur.close()
        print(info)
        if (user, email) in info:
            new_pass = functions.generate_pass()
            #functions.change_pass(user, email, new_pass)
            cur = mysql.connection.cursor()
            cur.execute(f"UPDATE users SET password = '{new_pass}' WHERE username='{user}';")
            mysql.connection.commit()
            cur.close()
            return render_template('forgetpass.html', valid='Tebrikler ! Şifreniz başarı ile değiştirildi Lutfen mail adresinizi kontrol ediniz.')
        else: 
            return render_template('forgetpass.html', error='Üzgünüz! Belirtilen mail veya kullanıcı adına rastlanılamadı.')
    else:
        return render_template('forgetpass.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ =='__main__':
    app.run(debug=True)