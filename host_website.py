from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import pandas as pd
from utils import generate_code, send_emails
from werkzeug.security import check_password_hash
import mysql.connector 
import os
import MySQLdb
import re  
from flask import flash  
import ssl


app = Flask(__name__)

""" 
The secret_key in a Flask application is used for securely signing the session cookie 
and other security-related needs.
This ensures that the data stored in the session cookie cannot be tampered with by the client. 
If someone tries to modify the session data, Flask will detect it because
the signature will no longer match.
""" 
app.secret_key = os.environ.get('SECRET_KEY')

# Replace the MySQL configuration block with this:
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))

# Now, let's create a dictionary of our connection parameters
db_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DB'),
    'port': int(os.environ.get('MYSQL_PORT', 3306))
}

# Try to establish a connection
try:
    connection = MySQLdb.connect(**db_config)
    print("Successfully connected to the database")
    connection.close()
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL Platform: {e}")
    print(f"Error: {e.args[0]}, {e.args[1]}")

# Initialize MySQL
mysql = MySQL(app)



# Logic for the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    errormsg = ""
    username = ""
    password = ""
    
    """ 
    Create session data if credentials are valid
    Session variables basically act like browser cookies. They are stored on the webserver as opposed to the user's browser.
    So the session data can be passed to the home page to validate if the persons has logged in or not.
    This prevents "hackers" from just navigating to http/IP/login/home and skipping the login step.
    """

    # If a username and password are submitted: 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']    

        # Input validation (to protect against sql injection)
        if not re.match(r'^[A-Za-z0-9_]+$', username):
            errormsg = 'Username must contain only letters, numbers, and underscores!'
        else:
            # get the account info from the database
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM Accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            cursor.close()

            # check if the password is correct, if so set the session variables
            if account and check_password_hash(account[2], password):
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                return redirect(url_for('home'))
            else:
                errormsg = 'Incorrect username/password!'

    return render_template('loginpage.html', msg=errormsg)


# If the user tries to go to a subpage that does not exist, they get redirected to the login page
@app.route('/')
def reroute():
   return redirect(url_for('login'))

# Logic for the home page (3 buttons: choose to scan tickets, show tickets, send tickets)
@app.route('/login/home', methods=['GET', 'POST'])
def home():
    # Check if user is logged in
    if 'loggedin' in session:
        if request.method == 'POST':
            # Based on the button pressed, redirect to the corresponding page
            if 'scan_tickets' in request.form:
                return redirect(url_for('scan_tickets'))
            elif 'show_tickets' in request.form:
                return redirect(url_for('show_tickets'))
            elif 'send_tickets' in request.form:
                return redirect(url_for('send_tickets'))
        return render_template('home.html')
    return redirect(url_for('login'))

# Logic for ticket scanning page
@app.route('/login/home/scan_tickets', methods=['GET', 'POST'])
def scan_tickets():
    if 'loggedin' in session:
        reset_color = False
        color = 'white'
        given_code = ''
        if request.method == "POST":
            given_code = request.form['fcode']
            
            if not re.match(r'^[A-Za-z]+$', given_code):
                flash('Invalid code format. Only letters are allowed.', 'error')
                color = 'red'
                reset_color = True
            else:
                mycursor = mysql.connection.cursor()
                query = "SELECT EXISTS(SELECT * FROM Tickets WHERE code = %s AND valid = 1)"
                mycursor.execute(query, (given_code,))
                result = mycursor.fetchone()
                
                if result[0] == 1:
                    query = "UPDATE Tickets SET valid = 0 WHERE code = %s"
                    mycursor.execute(query, (given_code,))
                    mysql.connection.commit()
                    flash(f'The code "{given_code}" is valid!', 'success')
                    color = 'green'
                    reset_color = True
                else:
                    flash(f'The code "{given_code}" is wrong (or has already been used).', 'error')
                    color = 'red'
                    reset_color = True
                mycursor.close()
        return render_template('scan_tickets.html', reset_color=reset_color, color=color, given_code=given_code)
    return redirect(url_for('login'))

# Logic for page that shows all the tickets in the database
@app.route('/login/home/show_tickets', methods=['GET', 'POST'])
def show_tickets():
    if 'loggedin' in session:
        # Print all the tickets that are in the database.
        query = "SELECT name, code, valid FROM Tickets ORDER BY name ASC"
        mycursor = mysql.connection.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()  # Result is a tuple of tuples
        mycursor.close()

        # Convert the result directly to the desired format
        data = [[name, code, validity] for name, code, validity in result]
        
        return render_template('show_tickets.html', data=data)
    return redirect(url_for('login'))


# Logic for the page that sends tickets to the database
@app.route('/login/home/send_tickets', methods=['GET', 'POST'])
def send_tickets():
    if 'loggedin' in session:
        if request.method == 'POST':
            # If the user submits the form, extract the data
            sender_email = request.form['sender_email']
            excel_file = request.form['excel_file']
            subject = request.form['subject']
            message = request.form['message']
            password = request.form['password']
 
            # Input validation (to protect against sql injection)
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', sender_email):
                flash('Invalid email format!', 'error')
                return render_template('send_tickets.html')
            
            # Check if the file is an excel file
            if not excel_file.lower().endswith('.xlsx'):
                flash('Invalid file format. Please use .xlsx files.', 'error')
                return render_template('send_tickets.html')

            # Clear out the Tickets table before filling it again 
            mycursor = mysql.connection.cursor()
            query = "DELETE FROM Tickets WHERE valid!=5"
            mycursor.execute(query)
            mysql.connection.commit()
            mycursor.close()

            # Read the xlsx file into a dataframe
            df = pd.read_excel(excel_file)
            
            #Add a column to the dataframe that will contain the generated codes
            df['Code'] = ''
            
            # Loop through the dataframe and generate a code for each person
            used_codes = []
            for i in range(len(df)):
                df['Code'][i] = generate_code()
                # Keep regenerating a random code until it is unique
                while df['Code'][i] in used_codes:
                    df['Code'][i] = generate_code()
                used_codes.append(df['Code'][i]) # To keep track of the codes that have been given out

            # Add the created tickets to the database
            for _, row in df.iterrows():
                name = row['Name']
                email = row['Email']
                code = row['Code']
                valid = 1 
                query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
                mycursor = mysql.connection.cursor()
                mycursor.execute(query, (name, email, code, valid))
                mysql.connection.commit()

            # Send the emails with the tickets
            send_emails(sender_email, password, subject, message, df)

            mycursor.close()
        return render_template('send_tickets.html')
    return redirect(url_for('login'))


# This allows you to host the website your own pc (local hosts). 
# So that you can test the website when you make changes or are developing it.
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8181)