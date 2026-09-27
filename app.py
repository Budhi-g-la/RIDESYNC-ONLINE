from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


# -----------------------------
# BUS DATA
# -----------------------------

bus_data = {

    "bus1": {
        "status": "On Route",
        "current_stop": "Doddaballapur",
        "eta": "25 minutes",
        "next_stop": "D-Cross",
        "latitude": None,
        "longitude": None
    },

    "bus2": {
        "status": "On Route",
        "current_stop": "Yelahanka",
        "eta": "30 minutes",
        "next_stop": "Puttenahalli",
        "latitude": None,
        "longitude": None
    }
}


# -----------------------------
# BUS ROUTES
# -----------------------------

bus_routes = {

    "bus1": [
        "Doddaballapur",
        "D-Cross",
        "Railway Station",
        "Bank Circle",
        "Marsandra",
        "Rajankunte",
        "Primus College"
    ],

    "bus2": [
        "Yelahanka",
        "Puttenahalli",
        "Anantpur Gate",
        "Nagenahalli",
        "Avalahalli",
        "Singanayakanahalli Gate",
        "Primus College"
    ]
}


# -----------------------------
# STUDENT PAGE
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# DRIVER PAGE
# -----------------------------

@app.route("/driver")
def driver():
    return render_template("driver.html")


# -----------------------------
# GET BUS STATUS
# -----------------------------

@app.route("/api/bus-status")
def bus_status():

    return jsonify(bus_data)


# -----------------------------
# UPDATE BUS STOP
# -----------------------------

@app.route("/api/update-location", methods=["POST"])
def update_location():

    data = request.get_json()

    bus = data.get("bus")
    stop = data.get("stop")

    if bus not in bus_data:

        return jsonify({
            "success": False,
            "message": "Invalid bus"
        })


    if stop not in bus_routes[bus]:

        return jsonify({
            "success": False,
            "message": "Invalid stop for this bus"
        })


    bus_data[bus]["current_stop"] = stop

    route = bus_routes[bus]

    current_index = route.index(stop)


    # -----------------------------
    # NEXT STOP
    # -----------------------------

    if current_index < len(route) - 1:

        bus_data[bus]["next_stop"] = \
            route[current_index + 1]

        bus_data[bus]["status"] = "On Route"

    else:

        bus_data[bus]["next_stop"] = \
            "Destination Reached"

        bus_data[bus]["status"] = "Reached"


    # -----------------------------
    # ETA
    # -----------------------------

    remaining_stops = \
        len(route) - current_index - 1


    if remaining_stops == 0:

        bus_data[bus]["eta"] = "Arrived"

    else:

        bus_data[bus]["eta"] = \
            str(remaining_stops * 5) + " minutes"


    return jsonify({

        "success": True,

        "message":
            f"{bus.upper()} location updated to {stop}"
    })


# -----------------------------
# UPDATE GPS LOCATION
# -----------------------------

@app.route("/api/update-gps", methods=["POST"])
def update_gps():

    data = request.get_json()

    bus = data.get("bus")
    latitude = data.get("latitude")
    longitude = data.get("longitude")


    # -----------------------------
    # CHECK BUS
    # -----------------------------

    if bus not in bus_data:

        return jsonify({

            "success": False,

            "message": "Invalid bus"
        })


    # -----------------------------
    # CHECK GPS DATA
    # -----------------------------

    if latitude is None or longitude is None:

        return jsonify({

            "success": False,

            "message": "GPS coordinates missing"
        })


    # -----------------------------
    # SAVE GPS
    # -----------------------------

    bus_data[bus]["latitude"] = latitude
    bus_data[bus]["longitude"] = longitude


    return jsonify({

        "success": True,

        "message": "GPS location received",

        "latitude": latitude,

        "longitude": longitude
    })


# -----------------------------
# START SERVER
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )