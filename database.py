import sqlite3
import datetime

database_conn = sqlite3.connect('database.sqlite3', check_same_thread=False)
database_cursor = database_conn.cursor()


def add_hostel(**kwargs):
    try:
        query = 'INSERT INTO hostel (Hostel_Name, Hostel_Phone, Hostel_Email, Hostel_Address, Postcode) VALUES (?, ?, ?, ?, ?)'
        database_cursor.execute(query, (
            kwargs.get('name'), int(kwargs.get('phone')), kwargs.get('email'), kwargs.get('address'),
            str(kwargs.get('postal_code'))))
        database_conn.commit()
        msg = 'Successfully inserted hostel'
    except Exception as ex:
        database_conn.rollback()
        msg = 'Error raises while inserting hostel'
    return msg


def add_room(**kwargs):
    try:
        query = 'INSERT INTO room (Hostel_ID, Room_Type_ID) VALUES (?, ?)'
        database_cursor.execute(query, (
            int(kwargs.get('hostel_id')), kwargs.get('room_type_id')))
        database_conn.commit()
        msg = 'Successfully inserted room'
    except Exception as ex:
        database_conn.rollback()
        msg = 'Error raises while inserting room'
    return msg


def add_room_category(**kwargs):
    try:
        query = 'INSERT INTO room_category (Room_category_Name, Room_Rent_per_month, Number_Of_Seats, Description) VALUES (?, ?, ?, ?)'
        database_cursor.execute(query, (
            kwargs.get('category_name'), int(kwargs.get('rent')), int(kwargs.get('seat')), kwargs.get('description')))
        database_conn.commit()
        msg = 'Successfully inserted room category'
    except Exception as ex:
        database_conn.rollback()
        msg = 'Error raises while inserting room category'
    return msg


def add_student(**kwargs):
    try:
        query = 'INSERT INTO student (Student_Name, Student_Father_Name, Date_of_Birth, Student_Gender, Mobile, Student_Email, Permanent_Address, Username, Password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        database_cursor.execute(query, (
            kwargs.get('name'), kwargs.get('father_name'),
            datetime.datetime.strptime(kwargs.get('dob'), '%Y-%m-%d'), kwargs.get('gender'),
            kwargs.get('mobile'), kwargs.get('email'), kwargs.get('address'), kwargs.get('username'),
            kwargs.get('password')))
        database_conn.commit()
        msg = 'Successfully inserted student'
    except Exception as ex:
        database_conn.rollback()
        msg = 'Error raises while inserting student'
    return msg


def add_reservation(**kwargs):
    try:
        query = 'INSERT INTO reservation (Student_ID, Room_ID, Room_Category,  Reservation_Date, Total_Month, Status) VALUES (?, ?,?, ?, ?, ?)'
        database_cursor.execute(query, (
            int(kwargs.get('student_id')), int(kwargs.get('room_id')), kwargs.get('room_cat'),
            datetime.datetime.strptime(kwargs.get('date'), '%Y-%m-%d'), int(kwargs.get('month')), 'Pending'))
        database_conn.commit()
        msg = 'Successfully inserted reservation'
    except Exception as ex:
        database_conn.rollback()
        msg = 'Error raises while inserting reservation'
    return msg


def check_student(**kwargs):
    try:
        query = 'SELECT Student_ID, Username, Student_Email FROM student WHERE Username=? and password=?'
        database_cursor.execute(query, (kwargs.get('user_name'), kwargs.get('password')))
        result = database_cursor.fetchall()
        if len(result) > 0:
            return result[0]
        return result
    except Exception as ex:
        result = []
    return result


def change_status(id, status):
    try:
        query = f"UPDATE reservation SET Status = '{status}' WHERE Reservation_ID = {int(id)}"
        database_cursor.execute(query)
        database_conn.commit()
    except Exception as ex:
        database_conn.rollback()
        raise ex


def get_all_reservation():
    try:
        query = 'SELECT * FROM reservation'
        database_cursor.execute(query)
        result = database_cursor.fetchall()
        return result
    except Exception as ex:
        result = []
    return result


def get_student_reservation(id):
    try:
        query = f'SELECT * FROM reservation WHERE Student_ID = {int(id)}'
        database_cursor.execute(query)
        result = database_cursor.fetchall()
        return result
    except Exception as ex:
        result = []
    return result


def get_all_rooms():
    try:
        query = 'SELECT Room_ID FROM room'
        database_cursor.execute(query)
        result = database_cursor.fetchall()
        output = []
        for res in result:
            output.append(res[0])
    except Exception as ex:
        output = []
    return output


def get_all_rooms_cat():
    try:
        query = 'SELECT Room_category_Name FROM room_category'
        database_cursor.execute(query)
        result = database_cursor.fetchall()
        output = []
        for res in result:
            output.append(res[0])
    except Exception as ex:
        output = []
    return output


def get_id(name):
    try:
        query = f"SELECT Room_category_id FROM room_category where Room_category_Name='{name}'"
        database_cursor.execute(query)
        result = database_cursor.fetchone()
        return int(result[0])
    except Exception as ex:
        output = []
    return output


def update_reservation_details(**kwargs):
    try:
        query = 'UPDATE reservation SET Student_ID = ? , Room_ID = ? , Room_Category = ? ,  Reservation_Date = ?, Total_Month = ? , Status = ? where Reservation_ID = ?'
        database_cursor.execute(query, (
            int(kwargs.get('student_id')), int(kwargs.get('room_id')), kwargs.get('room_cat'),
            datetime.datetime.strptime(kwargs.get('date'), '%Y-%m-%d'), int(kwargs.get('month')), 'Pending',
            int(kwargs.get('id'))))
        database_conn.commit()
    except Exception as ex:
        database_conn.rollback()
