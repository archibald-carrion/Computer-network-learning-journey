from flask import Flask, request, render_template_string

app = Flask(__name__)

# Simple HTML form for login
LOGIN_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Plaintext Login Demo</title>
</head>
<body>
    <h1>Login (Plaintext HTTP)</h1>
    <form action="/login" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Login">
    </form>
    <p><strong>Warning:</strong> This form submits data in plaintext. Use Wireshark/tcpdump to capture the traffic!</p>
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
    return f"<h1>Plaintext Submission Received</h1>" \
           f"<p>Username: {username}</p>" \
           f"<p>Password: {password}</p>" \
           f"<p><strong>Note:</strong> This data was sent in plaintext and can be intercepted!</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
