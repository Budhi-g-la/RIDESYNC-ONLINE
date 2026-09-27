from flask import Flask, render_template, jsonify, request
import os

app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates"
    )
)


# =====================================
# BUS DATA
# =====================================

buses = {

    "bus1": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "current_stop": "College Gate",
        "next_stop": "Main Road",
        "eta": 3
    },

    "bus2": {
        "latitude": 12.9750,
        "longitude": 77.5990,
        "current_stop": "Main Road",
        "next_stop": "Bus Stop 1",
        "eta": 4
    },

    "bus3": {
        "latitude": 12.9785,
        "longitude": 77.6030,
        "current_stop": "Bus Stop 1",
        "next_stop": "Bus Stop 2",
        "eta": 5
    }
}


# =====================================
# HOME
# =====================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================
# STUDENT TRACK PAGE
# =====================================

@app.route("/track")
def track():
    return render_template("track.html")


# =====================================
# DRIVER PAGE
# =====================================

@app.route("/driver")
def driver():
    return render_template("driver.html")


# =====================================
# GET BUS LOCATION
# =====================================

@app.route("/api/bus-location")
def bus_location():

    bus_id = request.args.get("bus", "bus1")

    if bus_id not in buses:
        bus_id = "bus1"

    return jsonify(buses[bus_id])


# =====================================
# UPDATE BUS LOCATION FROM DRIVER
# =====================================

@app.route("/api/update-location", methods=["POST"])
def update_location():

    data = request.get_json()

    bus_id = data.get("bus_id")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if bus_id not in buses:
        return jsonify({
            "success": False,
            "message": "Invalid bus"
        }), 400

    buses[bus_id]["latitude"] = latitude
    buses[bus_id]["longitude"] = longitude

    return jsonify({
        "success": True,
        "message": "Location updated"
    })


# =====================================
# START SERVER
# =====================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )