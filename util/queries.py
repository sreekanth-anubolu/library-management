

GET_USER_BY_ID = "SELECT * from EMPLOYEE WHERE id=%s;"

GET_USER_BY_EMAIL = "SELECT * from EMPLOYEE WHERE email=%s;"

INSERT_EMPLOYEE = "INSERT INTO EMPLOYEE(name, email, password) VALUES(%s, %s, %s);"
