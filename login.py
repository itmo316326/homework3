from flask import Flask, request, render_template, redirect, session, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.wad


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_user_online = db.users.find_one({"username": username, "password": password})
        if is_user_online:
            session['username'] = username
            return redirect(url_for("http://localhost:5000/profile"))
        else:
            message = "Failed Login"
            return render_template('login.html', message=message)
    return render_template('login.html')


@app.route("/registered/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_is_online = db.insert_one({"username": username, "password": password})
        if user_is_online:
            session['username'] = username
            return redirect(url_for("http://localhost:5000/profile"))
        else:
            message = 'User not registered'
            return render_template('register.html', message=message)
    return render_template('register.html')


@app.route("/profile")
def profile():
    if session.get("username"):
        return redirect(url_for("http://localhost:5000/profile/"))
    else:
        return render_template('login.html')
    return render_template('profile.html')


def log_out():
    session.clear()
    return redirect('login.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
