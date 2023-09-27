
from util.db import DBConnection
from util.queries import INSERT_STUDENT, GET_STUDENTS

class StudentModel:

    def __init__(self, id, name, email, reg_number, active=None, created_by=None, created_on=None):
        self.id = id
        self.name = name
        self.email = email
        self.reg_number = reg_number
        self.active = active
        self.created_by = created_by
        self.created_on = created_on

    @staticmethod
    def create_student(name, email, reg_number, current_user_id):
        try:
            conn = DBConnection.get_conn()
            curr = conn.cursor()
            curr.execute(INSERT_STUDENT, (name, email, reg_number, current_user_id))
            conn.commit()
            curr.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Exception in create_student {e}")
            return False


    @classmethod
    def get_students(cls):
        try:
            conn = DBConnection.get_conn()
            curr = conn.cursor()
            curr.execute(GET_STUDENTS)
            data = curr.fetchall()
            curr.close()
            conn.close()
            students = []
            for student in data:
                b = StudentModel(student[0], student[1], student[2], student[3], student[4])
                students.append(b)
            return students
        except Exception as e:
            print(f"Exception in get_student {e}")
            return False













