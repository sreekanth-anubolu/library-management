

GET_USER_BY_ID = "SELECT * from EMPLOYEE WHERE id=%s;"

GET_USER_BY_EMAIL = "SELECT * from EMPLOYEE WHERE email=%s;"

INSERT_EMPLOYEE = "INSERT INTO EMPLOYEE(name, email, password) VALUES(%s, %s, %s);"

INSERT_BOOK = "INSERT INTO BOOKS(title, author, total_copies, available_copies, created_by) VALUES(%s, %s, %s,  %s , %s);"

GET_BOOKS = "select b.id, title, author, total_copies, available_copies, bought_on, e.name from books as b inner join employee as e on e.id = b.created_by;"

GET_BOOK_BY_ID = "select title, author, total_copies, available_copies from books where id=%s;"

UPDATE_BOOK = "UPDATE BOOKS SET title=%s, author=%s, total_copies=%s, available_copies=%s where id=%s;"

INSERT_STUDENT = "INSERT INTO STUDENT(name, email, reg_no, created_by) VALUES(%s, %s, %s, %s);"

GET_STUDENTS = "SELECT id, name, email, reg_no, active FROM STUDENT;"

INSERT_INTO_BORROWED_BOOKS = "INSERT INTO BORROWEDBOOKS(student_id, book_id, due_date, emp_id) VALUES(%s, %s, %s, %s);"

GET_ASSIGNED_BOOKS = "SELECT s.id as student_id, s.name as student_name, b.id as book_id, b.title as book_title, bb.due_date, bb.return_date FROM " \
                     "student s INNER JOIN borrowedbooks bb ON s.id = bb.student_id INNER JOIN books b ON bb.book_id = b.id;"