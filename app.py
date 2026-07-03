from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML/JavaScript frontend - Isme user ka IP detect karne ka logic add kiya hai
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Automatic GPS & IP Tracker</title>
</head>
<body style="text-align: center; font-family: Arial; margin-top: 50px;">

    <h2>Exact GPS & IP Location Tracker (Automatic)</h2>
    <p id="status">Kripya browser mein location permission ko <b>Allow</b> karein...</p>

    <script>
    window.onload = function() {
        getLocation();
    };

    function getLocation() {
        const status = document.getElementById('status');

        if (!navigator.geolocation) {
            status.textContent = 'Aapka browser GPS support nahi karta.';
            return;
        }

        navigator.geolocation.getCurrentPosition(success, error, {
            enableHighAccuracy: true,
            timeout: 7000,
            maximumAge: 0
        });
    }

    function success(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        document.getElementById('status').innerHTML = `<b>Success!</b><br>Lat: ${lat}<br>Lon: ${lon}<br><br>Sending data to Python Backend...`;

        // Backend par data bhejte waqt IP address fetch karne ki zaroorat nahi hai, 
        // Flask khud user ki IP request se nikaal lega.
        fetch('/receive-location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lon })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').innerHTML += "<br><br><span style='color:green;'><b>[Done] Data Flask server par save ho gaya!</b></span>";
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

    # request.remote_addr se Flask user ka exact IP Address nikaal leta hai
    user_ip = request.remote_addr

    # Agar user local network (localhost) par chala raha hai, toh IP '127.0.0.1' ya '::1' dikhayega
    if user_ip == "127.0.0.1" or user_ip == "::1":
        user_ip = "127.0.0.1 (Localhost / Same Device)"

    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    print("\n" + "="*50)
    print(f"🔥 AUTOMATIC DATA RECEIVED! 🔥")
    print(f"USER IP ADDRESS : {user_ip}")  # Aapki requirement ke mutabik IP print hoga
    print(f"Latitude        : {latitude}")
    print(f"Longitude       : {longitude}")
    print(f"Google Maps Link: {google_maps_link}")
    print("="*50 + "\n")
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
