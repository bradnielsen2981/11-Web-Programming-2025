print("\33c") # Clear the console
from flask import * # Importing Flask
import databaseinterface

app = Flask(__name__) # Initializing Flask app
app.secret_key = "Yo Peace man!" # Setting the secret key for session management

DATABASE = databaseinterface.Database("test.db", app.logger) # Initializing the database interface with the database file

@app.route("/") # Defining the home url route
def home():
    if 'userid' in session:
        saying = "Welcome back, user!"
    else:
        return redirect("/login")
    return render_template("home.html", message=saying)

@app.route("/login", methods=["GET", "POST"]) # Defining the login url route
def login():
    if 'userid' in session:
        return redirect("./")
    message = "Please enter your login details."
    if request.method == "POST": # If the method is POST
        print("POST request received")
        email = request.form["email"]
        password = request.form["password"]
        results = DATABASE.ViewQuery("SELECT * FROM users WHERE email = ?", (email,))
        if results:
            user = results[0]
            user_password = user['password']
            if user_password == password:
                print("Login successful")
                session['userid'] = user['userid']
                session['permission'] = user['permission']
                message = "Login successful! Welcome back."
                return redirect("./") #. stops redirecting form data
            else:
                message = "Incorrect password. Please try again."
        else:
            message = "Email not found. Please register or try again."
    return render_template("login.html", message=message)

@app.route("/logout") # Defining the logout url route
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register") # Register
def register():
    return "Register"

@app.route("/admin") # Admin
def admin():
    results = DATABASE.ViewQuery("SELECT * FROM users")
    return jsonify(results)

if __name__ == "__main__": # Running the app
    app.run(debug=True, port=5000)