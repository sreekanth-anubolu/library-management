
from util.db import DBConnection
from util.utils import add_delta
from util.queries import GET_ASSIGNED_BOOKS, INSERT_INTO_BORROWED_BOOKS
class BorrowedBooksModel:

    def __init__(self, student_id, student_name, book_id, book_name, due_date, return_date):
        self.book_id = book_id
        self.book_name = book_name
        self.student_id = student_id
        self.student_name = student_name
        self.due_date = due_date
        self.returned_date = return_date

    @staticmethod
    def assign_book_to_student(student_id, book_id, current_user_id):
        try:
            due_date = add_delta(3)
            conn = DBConnection.get_conn()
            curr = conn.cursor()
            curr.execute(INSERT_INTO_BORROWED_BOOKS, (student_id, book_id, due_date, current_user_id))
            conn.commit()
            curr.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Exception in assign_book_to_student {e}")
            return False

    @classmethod
    def get_assigned_books(cls):
        conn = DBConnection.get_conn()
        curr = conn.cursor()
        curr.execute(GET_ASSIGNED_BOOKS)
        data = curr.fetchall()
        curr.close()
        conn.close()
        result = []
        for d in data:
            #student_id, student_name, book_id, book_name, due_date, return_date
            result.append(cls(d[0], d[1], d[2], d[3], d[4], d[5]))
        return result