from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
BOOKED_DATES_FILE = "petsitting_schedule.csv"

def load_booked_dates():
    booked = set()
    if os.path.exists(BOOKED_DATES_FILE):
        with open(BOOKED_DATES_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    booked.add(row[0])
    return booked

@app.route("/", methods=["GET", "POST"])
def index():
    booked_dates = load_booked_dates()

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        pet = request.form.get("pet")
        notes = request.form.get("notes")
        dates = request.form.getlist("dates")  # list of selected dates

        if not name or not phone or not pet or not dates:
            return render_template("index.html", booked_dates=booked_dates,
                                   error="All fields and at least one date are required.")

        # check for conflicts
        for d in dates:
            if d in booked_dates:
                return render_template("index.html", booked_dates=booked_dates,
                                       error=f"Date {d} is already booked.")

        with open(BOOKED_DATES_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            for d in dates:
                writer.writerow([d, name, phone, pet, notes])

        return redirect(url_for("index"))

    return render_template("index.html", booked_dates=booked_dates)

if __name__ == "__main__":
    app.run(debug=True)
