from flask import Flask, render_template, request, redirect, url_for
from models import db, RoomOccupant
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    status = request.args.get('status')
    if status:
        all_rooms = RoomOccupant.query.filter_by(status=status).all()
    else:
        all_rooms = RoomOccupant.query.all()
    return render_template('rooms.html', rooms=all_rooms)

@app.route('/checkin', methods=['POST'])
def checkin():
    data = request.form
    new_guest = RoomOccupant(
        guest_name=data['guest_name'],
        room_number=data['room_number']
    )
    db.session.add(new_guest)
    db.session.commit()
    return redirect(url_for('rooms'))

@app.route('/checkout/<int:occupant_id>')
def checkout_screen(occupant_id):
    guest = RoomOccupant.query.get_or_404(occupant_id)
    return render_template('checkout.html', guest=guest)

@app.route('/checkout/<int:occupant_id>', methods=['POST'])
def checkout(occupant_id):
    guest = RoomOccupant.query.get_or_404(occupant_id)
    guest.check_out = datetime.utcnow()
    guest.status = "vacant"
    db.session.commit()
    return redirect(url_for('rooms'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
