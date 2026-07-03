
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Yeh HTML/JavaScript frontend hai jo user ko screen par dikhega
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Exact GPS Tracker</title>
</head>
<body style="text-align: center; font-family: Arial; margin-top: 50px;">

    <h2>Exact GPS Location Tracker</h2>
    <p>Neeche diye gaye button par click karke exact location share karein:</p>
    <button onclick="getLocation()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">Share Live GPS Location</button>

    <p id="status"></p>

    <script>
    function getLocation() {
        const status = document.getElementById('status');

        // Check karna ki browser GPS support karta hai ya nahi
        if (!navigator.geolocation) {
            status.textContent = 'Aapka browser GPS support nahi karta.';
            return;
        }

        status.textContent = 'Locating... Kripya permission Allow karein.';

        // Exact High-Accuracy GPS data nikalna
        navigator.geolocation.getCurrentPosition(success, error, {
            enableHighAccuracy: true, // Isse exact GPS use hoga, IP nahi
            timeout: 5000,
            maximumAge: 0
        });
    }

    function success(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        document.getElementById('status').innerHTML = `<b>Success!</b><br>Lat: ${lat}<br>Lon: ${lon}<br><br>Sending to Python Backend...`;

        # Data ko Python server par bhejna
        fetch('/receive-location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lon })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').innerHTML += "<br><b>Python Server Saved it!</b>";
        });
    }

    function error() {
        document.getElementById('status').textContent = 'Location access nahi mila ya timeout ho gaya.';
    }
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


# Yeh route JavaScript se exact location coordinates receive karega
@app.route('/receive-location', methods = ['POST'])

def receive_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    print("\n" + "=" * 40)
    print(f"🔥 EXACT GPS LOCATION RECEIVED IN PYTHON! 🔥")
    print(f"Latitude : {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Google Maps Link: https://www.google.com/maps?q={latitude},{longitude}")
    print("=" * 40 + "\n")

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
