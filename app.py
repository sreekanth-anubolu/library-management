
from flask import Flask, render_template, request, redirect

from flask_login import LoginManager, login_required, login_user, current_user, logout_user

import bcrypt

from models.UserModel import UserModel

BCRYPT_SALT = b'$2b$12$91.eXPD2irVqBkzL/NLvc.'

app = Flask("library-management")
app.config["SECRET_KEY"] = "2323%$#Secret75%$&#"


login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    return UserModel.get_user_by_id(id)


@app.route("/employee/register", methods=["GET", "POST"])
def employee_registration():
    if request.method == "GET":
        return render_template("registration.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), BCRYPT_SALT)
        pw_hash = pw_hash.decode("utf-8")

        try:
            UserModel.register_employee(name, email, pw_hash)
        except Exception as e:
            print(f"Exception Handled in employee_registration POST block- {e}")

        return redirect("/employee/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        password = password.encode("utf-8")
        password_hash = bcrypt.hashpw(password, salt=BCRYPT_SALT).decode("utf-8")
        auth_message = UserModel.authenticate_user(email, password_hash)
        if auth_message["success"]:
            login_user(auth_message["user"])
            return redirect("/")
        else:
            return redirect("/login?login=failed")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
@login_required
def home():
    return render_template("home.html", current_user=current_user)


@app.route("/add/book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")
    else:
        pass












if __name__ == "__main__":
    app.run(debug=True)
