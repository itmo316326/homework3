import secrets
from flask import Flask, request, render_template, redirect, session, url_for
from pymongo import MongoClient

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret

client = MongoClient('localhost', 27017)
db = client.wad


@app.route("/")
def index():
    all_post = db.users.find({"post": "post"})
    return render_template("index.html", all_post=all_post)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_user_online = db.users.find_one({"username": username, "password": password})
        if is_user_online:
            session['username'] = username
            return redirect(url_for("profile"))
        else:
            message = "Failed Login"
            return render_template("login.html", message=message)
    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_is_online = db.users.insert_many([{"username": username, "password": password} for _ in range(1)])
        if user_is_online:
            session['username'] = username
            return redirect(url_for("profile"))
        else:
            message = 'User not registered'
            return render_template("register.html", message=message)
    return render_template("register.html")


@app.route("/profile")
def profile():
    if session.get("username"):
        post_list = refresh_information()
        return render_template("profile.html", post_list=post_list)
    else:
        return render_template("login.html")


@app.route("/logout")
def log_out():
    session.clear()
    return redirect(url_for("login"))


@app.route("/new", methods=['GET', 'POST'])
def creat_new_post():
    if request.method == 'POST':
        post_title = request.form["p_title"]
        post_content = request.form["p_content"]
        post_type = request.form["p_type"]
        is_post_success = db.users.insert_many([{"post": "post", "title": post_title, "content": post_content, "type": post_type,"username": session.get("username")} for _ in range(1)])
        if is_post_success:
            return redirect(url_for("profile"))
    return render_template("new.html")


def refresh_information():
    post_list = db.users.find({"post": "post", "username": session.get("username")})
    return post_list


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
