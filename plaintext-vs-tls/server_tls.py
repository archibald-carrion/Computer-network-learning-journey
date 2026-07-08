from flask import Flask, request, render_template_string
import ssl

app = Flask(__name__)

# Simple HTML form for login
LOGIN_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>TLS Login Demo</title>
</head>
<body>
    <h1>Login (HTTPS with TLS)</h1>
    <form action="/login" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Login">
    </form>
    <p><strong>Note:</strong> This form submits data encrypted with TLS. Try capturing the traffic with Wireshark!</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(LOGIN_FORM)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return f"<h1>TLS Submission Received</h1>" \
           f"<p>Username: {username}</p>" \
           f"<p>Password: {password}</p>" \
           f"<p><strong>Note:</strong> This data was encrypted with TLS and cannot be read by eavesdroppers.</p>"

if __name__ == '__main__':
    # Use a self-signed certificate for demo purposes
    # Generate one with: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=8443, ssl_context=context, debug=False)
