
from flask import Flask, render_template, request, redirect

from flask_login import LoginManager, login_required, login_user, current_user, logout_user

import bcrypt

from models.UserModel import UserModel
from models.BookModel import BookModel
from models.studentModel import StudentModel
from models.BorrowedBooks import BorrowedBooksModel

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
    books = BookModel.get_books()
    students = StudentModel.get_students()
    return render_template("home.html", current_user=current_user, books=books, students=students)


@app.route("/add/book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")
    else:
        title = request.form["title"].title()
        author = request.form["author"].title()
        copies = int(request.form.get("copies", 0))
        created = BookModel.create_book(title, author, copies, current_user.id)
        if created:
            return redirect("/")
        else:
            return render_template("add_book.html", error=True)


@app.route("/book/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(id):
    if request.method == "GET":
        books = BookModel.get_book_by_id(id)
        return render_template("edit_book.html", book=books)
    else:
        title = request.form["title"].title()
        author = request.form["author"].title()
        copies = int(request.form.get("copies", 0))
        available_copies = int(request.form.get("available_copies", 0))
        updated = BookModel.update_book(id, title, author, copies, available_copies)
        if updated:
            return redirect("/")
        else:
            return redirect(f"/book/{id}/edit")


@app.route("/add/student", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "GET":
        return render_template("add_student.html")
    else:
        name = request.form["name"].title()
        email = request.form["email"]
        reg_number = request.form.get("registration_number")
        print("====================")
        print(name, email, reg_number)
        created = StudentModel.create_student(name, email, reg_number, current_user.id)
        if created:
            return redirect("/")
        else:
            return render_template("add_student.html", error=True)



@app.route("/assign-books", methods=["GET"])
@login_required
def render_assign_books():
    students = StudentModel.get_students()
    books = BookModel.get_books()

    assigned_books = BorrowedBooksModel.get_assigned_books()
    return render_template("assign_books_to_students.html", books=books, students=students, assigned_books=assigned_books)


@app.route("/assign/book/<int:book_id>/student/<int:student_id>")
@login_required
def assign_book(book_id, student_id):
    print(book_id)
    print(student_id)
    BorrowedBooksModel.assign_book_to_student(student_id, book_id, current_user.id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
