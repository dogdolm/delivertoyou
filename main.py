import flask
import sqlite3

sqlite_connection = sqlite3.connect('cart.db', check_same_thread=False)
cursor = sqlite_connection.cursor()
print("Подключен к SQLite")

app = flask.Flask(__name__)


@app.route('/')
def index():
    if flask.request.cookies.get('user') is not None:
        user = {'nickname': flask.request.cookies.get('user')}
        return flask.render_template("order.html", user=user)
    else:
        return flask.render_template("order.html", noentry='True')


@app.route('/cart/')
def cart():
    cursor.execute("SELECT cart FROM cart WHERE nickname = ?;", (flask.request.cookies.get("user"),))
    cur = cursor.fetchone()
    print(cur)
    lent = str(cur).count("1")
    cartitem = list()
    for i in range(lent):
        cartitem.append(str(cur)[str(cur).index("1"):str(cur).index("1") + 3])
        print(cartitem)
    return flask.render_template("cart.html", len=lent, cartitem=cartitem)


@app.route('/about/')
def order():
    return flask.render_template("index.html")


@app.route('/exit/')
def reset():
    res = flask.make_response(flask.redirect('/'))
    res.set_cookie('user', 'no', max_age=0)
    return res


@app.route('/kfc/')
def kfc():
    return flask.render_template("kfc.html")


@app.route('/delete/<int:db_id>')
def delete(db_id):
    com = """UPDATE cart
             SET cart = ?
             WHERE nickname = ?;"""
    cursor.execute(com, (str(db_id) + " ", str(flask.request.cookies.get('user'))))
    sqlite_connection.commit()
    return flask.redirect('/')


@app.route('/add/<int:db_id>')
def add(db_id):
    user = flask.request.cookies.get('user')
    com = """UPDATE cart
             SET cart = ?
             WHERE nickname = ?;"""
    cursor.execute("SELECT cart FROM cart WHERE nickname = ?;", (flask.request.cookies.get("user"),))
    cursor.execute(com, (str(cursor.fetchone()) + " " + str(db_id) + " ", str(flask.request.cookies.get('user')),))
    sqlite_connection.commit()
    return flask.redirect('/')


@app.route('/login/', methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        res = flask.make_response(flask.redirect("/"))
        cursor.execute("SELECT nickname FROM cart;")
        if flask.request.form['user'] in str(cursor.fetchone()):
            cursor.execute("SELECT nickname FROM cart;")
            nick = list(cursor.fetchone())
            cursor.execute("SELECT passwd FROM cart;")
            pas = list(cursor.fetchone())
            print(nick)
            sqlite_connection.commit()
            if flask.request.form['password'] in pas and pas.index(flask.request.form['password']) == nick.index(flask.request.form['user']):
                res.set_cookie('user', flask.request.form['user'], max_age=60 * 60 * 24 * 365)
                res.set_cookie('passwd', flask.request.form['password'], max_age=60 * 60 * 24 * 365)
            else:
                return flask.render_template("login.html")
        else:
            passw = str(flask.request.form['password'])
            us = str(flask.request.form['user'])
            sqlite_insert_query = """INSERT INTO cart
                                      (nickname, cart, passwd)
                                      VALUES (?, '', ?);"""
            cursor.execute(sqlite_insert_query, (us, passw))
            res.set_cookie('user', us, max_age=60 * 60 * 24 * 365)
            sqlite_connection.commit()
        return res
    return flask.render_template("login.html")


app.run()
