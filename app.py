from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML/JavaScript frontend - Ab yeh bina click kiye auto-load hoga
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Automatic GPS Tracker</title>
</head>
<body style="text-align: center; font-family: Arial; margin-top: 50px;">

    <h2>Exact GPS Location Tracker (Automatic)</h2>
    <p id="status">Kripya browser mein location permission ko <b>Allow</b> karein...</p>

    <script>
    // Page load hote hi yeh function khud chal jayega (Bina click kiye)
    window.onload = function() {
        getLocation();
    };

    function getLocation() {
        const status = document.getElementById('status');

        if (!navigator.geolocation) {
            status.textContent = 'Aapka browser GPS support nahi karta.';
            return;
        }

        // Exact High-Accuracy GPS data nikalna
        navigator.geolocation.getCurrentPosition(success, error, {
            enableHighAccuracy: true,
            timeout: 7000, // Timeout thoda badha diya taaki phone sahi se GPS lock kar sake
            maximumAge: 0
        });
    }

    function success(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        document.getElementById('status').innerHTML = `<b>Success!</b><br>Lat: ${lat}<br>Lon: ${lon}<br><br>Sending data to Python Backend...`;

        // JavaScript comment sahi kiya (// use kiya, # nahi)
        fetch('/receive-location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lon })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').innerHTML += "<br><br><span style='color:green;'><b>[Done] Python Server par data save ho gaya!</b></span>";
        });
    }

    function error(err) {
        const status = document.getElementById('status');
        if (err.code == 1) {
            status.innerHTML = "<span style='color:red;'><b>Error:</b> Aapne Permission Deny (Block) kar di hai. Kripya site settings se location ON karein.</span>";
        } else {
            status.innerHTML = "<span style='color:red;'><b>Error:</b> GPS signal kamzor hai ya timeout ho gaya.</span>";
        }
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/receive-location', methods=['POST'])
def receive_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Google Maps ka link format sahi kiya taaki click karte hi sahi jagah khule
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    print("\n" + "="*50)
    print(f"🔥 AUTOMATIC GPS LOCATION RECEIVED! 🔥")
    print(f"Latitude : {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Google Maps Link: {google_maps_link}")
    print("="*50 + "\n")
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Local Network par mobile se test karne ke liye host='0.0.0.0' rakha hai
    app.run(debug=True, host='0.0.0.0', port=5000)
