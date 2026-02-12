from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "secret_taxi_key"

POINTS = ['A', 'B', 'C', 'D', 'E', 'F']
DISTANCE_PER_POINT = 15
TIME_PER_POINT = 1


class Booking:
    def __init__(self, booking_id, customer_id, pickup, drop, pickup_time, drop_time, amount):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.pickup = pickup
        self.drop = drop
        self.pickup_time = pickup_time
        self.drop_time = drop_time
        self.amount = amount


class Taxi:
    def __init__(self, taxi_id):
        self.taxi_id = taxi_id
        self.current_point = 'A'
        self.available_time = 0
        self.total_earnings = 0
        self.bookings = []


class TaxiService:
    def __init__(self, n):
        self.taxis = [Taxi(i + 1) for i in range(n)]
        self.booking_id = 1

    def distance(self, a, b):
        return abs(POINTS.index(a) - POINTS.index(b)) * DISTANCE_PER_POINT

    def travel_time(self, a, b):
        return abs(POINTS.index(a) - POINTS.index(b)) * TIME_PER_POINT

    def fare(self, distance):
        return 100 if distance <= 5 else 100 + (distance - 5) * 10

    def book_taxi(self, customer_id, pickup, drop, pickup_time):
        free_taxis = [t for t in self.taxis if t.available_time <= pickup_time]
        if not free_taxis:
            return None

        same_point = [t for t in free_taxis if t.current_point == pickup]

        if same_point:
            taxi = min(same_point, key=lambda t: t.total_earnings)
        else:
            taxi = min(
                free_taxis,
                key=lambda t: (
                    abs(POINTS.index(t.current_point) - POINTS.index(pickup)),
                    t.total_earnings
                )
            )

        distance = self.distance(pickup, drop)
        drop_time = pickup_time + self.travel_time(pickup, drop)
        amount = self.fare(distance)

        booking = Booking(
            self.booking_id, customer_id, pickup, drop, pickup_time, drop_time, amount
        )
        self.booking_id += 1

        taxi.bookings.append(booking)
        taxi.total_earnings += amount
        taxi.current_point = drop
        taxi.available_time = drop_time

        return taxi

    def add_taxi(self):
        self.taxis.append(Taxi(len(self.taxis) + 1))

    def remove_taxi(self):
        if self.taxis:
            self.taxis.pop()


service = TaxiService(4)


@app.route('/')
def index():
    return render_template('index.html', taxis=service.taxis)


@app.route('/book', methods=['POST'])
def book():
    try:
        cid = int(request.form.get('customer_id'))
        p = request.form.get('pickup').upper()
        d = request.form.get('drop').upper()
        t = int(request.form.get('time'))

        if p not in POINTS or d not in POINTS:
            flash("Invalid points! Use A-F.", "danger")
            return redirect('/')

        taxi = service.book_taxi(cid, p, d, t)
        if taxi:
            flash(f"Taxi-{taxi.taxi_id} allotted.", "success")
        else:
            flash("No taxi available.", "warning")
    except:
        flash("Invalid input.", "danger")

    return redirect('/')


@app.route('/add_taxi', methods=['POST'])
def add_taxi():
    service.add_taxi()
    return redirect('/')


@app.route('/remove_taxi', methods=['POST'])
def remove_taxi():
    service.remove_taxi()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
