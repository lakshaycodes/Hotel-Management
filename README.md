# 🏨 Hotel Management System — Flask App

A lightweight hotel management system built using **Flask** (Python), with a simple HTML frontend and SQLite database. This project lets you manage hotel rooms, bookings, check-ins/check-outs, and more with clean UI screens.

---

## 🚀 Features

- ✅ Check-in & Check-out Guests
- ✅ View all bookings by day
- ✅ Manage (Create/Edit/Delete) Rooms
- ✅ Grid view of rooms with filters
- ✅ Book rooms in advance
- ✅ Filter rooms by date, type, and status
- ✅ Daily booking report
- ✅ Simple responsive UI with consistent navbar

---

## 🧠 Code Structure

```
hotel-management/
│
├── app.py                  # Flask app with all routes
├── models.py               # SQLAlchemy models (Room, Booking)
├── static/
│   └── style.css           # Basic styling for the frontend
├── templates/
│   ├── base.html           # Shared layout with navbar
│   ├── index.html          # Landing page
│   ├── rooms.html          # Room grid + filters
│   ├── book.html           # Book room form
│   ├── checkout.html       # Checkout page
│   ├── bookings.html       # Daily bookings with date filter
│   ├── manage_rooms.html   # Admin CRUD for rooms
│   ├── create_room.html    # Create new room form
│   └── edit_room.html      # Edit existing room
└── README.md               # This file
```

---

## 🧑‍💻 Tech Stack

- **Backend**: Flask + SQLAlchemy (ORM)
- **Frontend**: HTML, CSS
- **Database**: SQLite

---

## 💪 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/hotel-management.git
cd hotel-management
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install Flask Flask-SQLAlchemy
```

### 4. Run the app
```bash
python app.py
```

Go to [http://localhost:5000](http://localhost:5000) to view the app.

---

## 💾 Database Models

### `Room`
| Field         | Type     | Description              |
|---------------|----------|--------------------------|
| id            | Integer  | Primary Key              |
| room_number   | String   | Unique Room Number       |
| room_type     | String   | Type (AC, Deluxe, etc.)  |
| is_occupied   | Boolean  | True if someone is in    |

### `Booking`
| Field          | Type     | Description              |
|----------------|----------|--------------------------|
| id             | Integer  | Primary Key              |
| guest_name     | String   | Guest's name             |
| room_id        | Foreign  | FK to Room               |
| check_in_date  | Date     | Check-in date            |
| check_out_date | Date     | Check-out date           |
| status         | String   | `booked`, `occupied`, `completed` |

---

## 🔁 Key Routes

| Route               | Purpose                            |
|---------------------|-------------------------------------|
| `/`                 | Landing Page                        |
| `/rooms`            | Room grid with filters              |
| `/book`             | Book a room                         |
| `/checkout`         | Checkout a guest                    |
| `/bookings`         | See bookings per day                |
| `/rooms/manage`     | View & manage rooms (CRUD)          |
| `/rooms/create`     | Create a new room                   |
| `/rooms/edit/<id>`  | Edit a room                         |
| `/rooms/delete/<id>`| Delete a room                       |

---

## 📸 Screenshots

> _(Add screenshots here showing room grid, bookings page, and manage rooms page)_

---

## 📌 Future Improvements

- Login system for admin/staff
- Assign room based on type availability
- Booking reports export (PDF/Excel)
- Email confirmation on booking
- Responsive UI with Tailwind or Bootstrap

---

## 🧑 Author

Made with 💻 by [Your Name](https://github.com/your-username)

---

## 📜 License

MIT License - free to use and modify.

