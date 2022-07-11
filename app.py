from flask import Flask, render_template, request, redirect, url_for, session, abort
from database import *
from functools import wraps

app = Flask(__name__)

app.secret_key = 'hostel'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user_name = request.form['username']
        password = request.form['password']
        result = check_student(user_name=user_name, password=password)
        if result:
            session['is_login'] = True
            session['id'] = result[0]
            session['username'] = result[1]
            session['email'] = result[2]
            if result[1] == 'admin':
                session['is_admin'] = True
            else:
                session['is_admin'] = False
            return redirect(url_for('reservation'))
        else:
            msg = 'Incorrect username / password !'
    else:
        msg = 'Fill the details'
    return render_template('login.html', msg=msg, session=session)


def is_login(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if session.get('id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return dec


def admin_check(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if session.get('id') is not None and session.get('is_admin') == True:
            return f(*args, **kwargs)
        else:
            return abort(404, 'Admin can not open the url')

    return dec


@app.route('/hostel', methods=['GET', 'POST'])
@admin_check
def hostel():
    msg = 'Fill the details'
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        postal_code = request.form['postal_code']
        msg = add_hostel(name=name, postal_code=postal_code, phone=phone, email=email, address=address)
    return render_template('hostel.html', msg=msg, session=session)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'Fill the details'
    if request.method == 'POST':
        name = request.form['name']
        father_name = request.form['father_name']
        gender = request.form['gender']
        dob = request.form['dob']
        mobile = request.form['mobile']
        address = request.form['address']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        msg = add_student(name=name, gender=gender, username=username, password=password,
                          father_name=father_name,
                          dob=dob, mobile=mobile, address=address, email=email)
        return redirect(url_for('reservation'))
    return render_template('student.html', msg=msg, session=session)


@app.route('/rooms', methods=['GET', 'POST'])
@admin_check
def rooms():
    msg = 'Fill the details'
    if request.method == 'POST':
        hostel_id = request.form['hostel_id']
        room_type_id = request.form['room_type_id']
        msg = add_room(hostel_id=hostel_id, room_type_id=room_type_id)
    return render_template('rooms.html', msg=msg, session=session)


@app.route('/rooms_category', methods=['GET', 'POST'])
@admin_check
def rooms_category():
    msg = 'Fill the details'
    if request.method == 'POST':
        category_name = request.form['category_name']
        rent = request.form['rent']
        description = request.form['description']
        seat = request.form['seat']

        msg = add_room_category(category_name=category_name, rent=rent, seat=seat, description=description)
    return render_template('rooms_category.html', msg=msg, session=session)


@app.route('/reservation', methods=['GET', 'POST'])
@is_login
def reservation():
    all_rooms = get_all_rooms()
    all_rooms_cat = get_all_rooms_cat()
    msg = 'Fill the details'
    header = f"Hi Your Student id is {session['id']}"
    if request.method == 'POST':
        student_id = request.form['student_id']
        room_id = request.form['room_id']
        room_cat = get_id(request.form['room_cat'])
        date = request.form['date']
        month = request.form['month']
        msg = add_reservation(student_id=student_id, room_id=room_id, date=date, month=month, room_cat=room_cat)
    return render_template('Reservation.html', header=header, msg=msg, session=session, all_rooms=all_rooms,
                           all_rooms_cat=all_rooms_cat, len_all_rooms=len(all_rooms),
                           len_all_rooms_cat=len(all_rooms_cat))


@app.route('/past_reservation', methods=['GET', 'POST'])
@is_login
def past_reservation():
    if request.form.get("accept"):
        change_status(int(request.form.get("accept")), 'Booked')
    if request.form.get('reject'):
        change_status(int(request.form.get("reject")), 'Rejected')
    header = f"Hi {session['username']}, Below is your previous booking"
    if session['username'] == 'admin':
        items = get_all_reservation()
    else:
        items = get_student_reservation(session['id'])
    for i in range(len(items)):
        items[i] = list(items[i])
        items[i][3] = str(items[i][3])
    table_header = ['Index', "Reservation_ID", "Student_ID", "Room_ID", "Reservation_Date", "Total_Month", "Status"]
    return render_template('reservation_history.html', header=header,
                           table_header=table_header, table_header_len_=len(table_header),
                           items_len_=len(items), items=items, session=session)


@app.route('/logout')
@is_login
def logout():
    session.pop('is_login', None)
    session.pop('username', None)
    session['is_admin'] = False
    session['id'] = None
    return redirect(url_for('login'))


@app.route('/update_reservation',  methods=['GET', 'POST'])
@is_login
def update_reservation():
    all_rooms = get_all_rooms()
    all_rooms_cat = get_all_rooms_cat()
    header = f"Hi Your Student id is {session['id']}"
    msg = 'Fill the details'
    if 'edit' in request.form:
        session['reservation_edit'] = request.form['edit']
    if request.method == 'POST' and 'student_id' in request.form:
        reservation_id = session['reservation_edit']
        student_id = request.form['student_id']
        room_id = request.form['room_id']
        room_cat = get_id(request.form['room_cat'])
        date = request.form['date']
        month = request.form['month']
        update_reservation_details(id = reservation_id, student_id=student_id, room_id=room_id, date=date, month=month, room_cat=room_cat)
        return redirect(url_for('past_reservation'))
    else:
        return render_template('update_reservation.html', header=header, msg=msg, session=session, all_rooms=all_rooms,
                           all_rooms_cat=all_rooms_cat, len_all_rooms=len(all_rooms),
                           len_all_rooms_cat=len(all_rooms_cat))


if __name__ == '__main__':
    app.run(debug=True)
