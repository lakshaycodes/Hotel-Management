from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Room, Booking
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    types = [r[0] for r in Room.query.with_entities(Room.room_type).distinct()]
    if request.method == 'POST':
        data = request.form
        b = Booking(
            guest_name=data['guest_name'],
            room_id=data['room_id'],
            check_in_date=datetime.strptime(data['check_in'], '%Y-%m-%d').date(),
            check_out_date=datetime.strptime(data['check_out'], '%Y-%m-%d').date(),
            status='booked'
        )
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('rooms'))
    rooms = Room.query.all()
    return render_template('book.html', rooms=rooms)

@app.route('/checkin/<int:booking_id>')
def checkin(booking_id):
    b = Booking.query.get_or_404(booking_id)
    b.status = 'occupied'
    db.session.commit()
    return redirect(url_for('rooms'))

@app.route('/checkout/<int:booking_id>', methods=['GET', 'POST'])
def checkout(booking_id):
    b = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        b.status = 'completed'
        db.session.commit()
        return redirect(url_for('rooms'))
    return render_template('checkout.html', booking=b)

@app.route('/rooms')
def rooms():
    # Filters
    fdate = request.args.get('date')
    if fdate:
        fdate = datetime.strptime(fdate, '%Y-%m-%d').date()
    else:
        fdate = date.today()
    room_type = request.args.get('room_type')
    status_filter = request.args.get('status')

    query = Room.query
    if room_type:
        query = query.filter_by(room_type=room_type)
    rooms_list = query.all()

    room_status = []
    for r in rooms_list:
        booking = Booking.query.filter(
            Booking.room_id == r.id,
            Booking.check_in_date <= fdate,
            Booking.check_out_date >= fdate,
            Booking.status.in_(['booked', 'occupied'])
        ).first()
        status = booking.status if booking else 'vacant'
        bid = booking.id if booking else None
        room_status.append({'room': r, 'status': status, 'booking_id': bid})

    types = [r[0] for r in Room.query.with_entities(Room.room_type).distinct()]
    return render_template(
        'rooms.html',
        room_status=room_status,
        types=types,
        selected_type=room_type,
        selected_status=status_filter,
        filter_date=fdate
    )
@app.route('/bookings')
def view_bookings():
    selected_date = request.args.get('date')
    if selected_date:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        date_obj = date.today()

    bookings = Booking.query.filter(
        Booking.check_in_date <= date_obj,
        Booking.check_out_date >= date_obj
    ).all()

    return render_template('bookings.html', bookings=bookings, selected_date=date_obj)

@app.route('/rooms/manage')
def manage_rooms():
    rooms = Room.query.all()
    return render_template('manage_rooms.html', rooms=rooms)

@app.route('/rooms/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_number = request.form['room_number']
        room_type = request.form['room_type']
        room = Room(room_number=room_number, room_type=room_type)
        db.session.add(room)
        db.session.commit()
        flash('Room created successfully.')
        return redirect(url_for('manage_rooms'))
    return render_template('create_room.html')

@app.route('/rooms/edit/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        room.room_number = request.form['room_number']
        room.room_type = request.form['room_type']
        db.session.commit()
        flash('Room updated successfully.')
        return redirect(url_for('manage_rooms'))
    return render_template('edit_room.html', room=room)

@app.route('/rooms/delete/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully.')
    return redirect(url_for('manage_rooms'))

# DATABASE INIT & SERVER START
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # seed sample rooms if not exists
        if not Room.query.first():
            sample = [
                ('101', 'Single'), ('102', 'Single'),
                ('201', 'Double'), ('202', 'Double'),
                ('301', 'Suite')
            ]
            for num, rtype in sample:
                db.session.add(Room(room_number=num, room_type=rtype))
            db.session.commit()
    app.run(debug=True)