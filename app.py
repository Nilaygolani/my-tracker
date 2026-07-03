from flask import Flask, request, render_template_string
import os

app = Flask(__name__)


@app.route('/')
def home():
    # 1. User ka IP address nikalna
    if request.headers.getlist("X-Forwarded-For"):
        user_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        user_ip = request.remote_addr  # Local testing ke liye

    # 2. Terminal/Render logs mein IP print karna
    print(f"\n⚡ [TRACKED] Ek user website par aaya! IP Address: {user_ip}\n")

    # 3. Responsive aur Centered HTML Page (Sky Blue Background)
    html_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome</title>
        <style>
            /* Pure page ko full screen banana aur background color sky blue karna */
            body {
                margin: 0;
                padding: 0;
                background-color: #87CEEB; /* Sky Blue Color */
                font-family: 'Arial', sans-serif;

                /* Content ko horizontal aur vertical dono taraf se center karne ke liye flexbox */
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh; /* Viewport Height (Puri screen cover karega) */
                text-align: center;
                box-sizing: border-box;
            }

            /* Container jo mobile par text ko secure aur readable rakhega */
            .content-box {
                padding: 20px;
                max-width: 90%; /* Mobile screens par corners se touch nahi hoga */
            }

            h1 {
                font-size: 2.5rem;
                color: #ffffff;
                margin-bottom: 10px;
                text-shadow: 1px 1px 4px rgba(0,0,0,0.2); /* Sunder text effect */
            }

            p {
                font-size: 1.2rem;
                color: #f0f8ff;
            }

            /* Choti mobile screens ke liye font size adjust karna */
            @media (max-width: 480px) {
                h1 { font-size: 1.8rem; }
                p { font-size: 1rem; }
            }
        </style>
    </head>
    <body>

        <div class="content-box">
            <h1>BSDK AA GYA MADARCHOD.</h1>
          
        </div>

    </body>
    </html>
    """
    return render_template_string(html_page)


if __name__ == '__main__':
    # Render deployment ke liye port configuration secure rakha hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
