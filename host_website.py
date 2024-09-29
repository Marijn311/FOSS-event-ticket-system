from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import pandas as pd
from utils import generate_code, send_emails
from werkzeug.security import check_password_hash
import mysql.connector 


#todo ensure a safe https connection
#todo add in readme a guide to https safe connection
app = Flask(__name__)


""" 
The secret_key in a Flask application is used for securely signing the session cookie 
and other security-related needs.
This ensures that the data stored in the session cookie cannot be tampered with by the client. 
If someone tries to modify the session data, Flask will detect it because
the signature will no longer match.
""" 
app.secret_key = 'placeholder'


# Connect to the database (I use a free dev package from clever cloud)
app.config['MYSQL_USER'] ="placeholder"
app.config['MYSQL_PASSWORD'] = "placeholder"
app.config['MYSQL_HOST'] = "placeholder-mysql.services.clever-cloud.com"
app.config['MYSQL_DB'] = "placeholder"
app.config['MYSQL_PORT'] = placeholder
app.config['MYSQL_CURSORCLASS'] = 'placeholder'
mysql = MySQL(app)


# Logic for the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    errormsg=""
    username=""
    password=""
    
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

        # Check if the username and password combination is valid in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.close()

        # If the account exists and the password is correct, the login is valid and the session variables are set
        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

        # Redirect to home page if login was valid (if the session variables exist)
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
        given_code=' '
        status = ' '
        color = 'white' 
        if request.method == "POST":
            # Extract the entered code
            info = request.form
            given_code = info['fcode']
            mycursor = mysql.connection.cursor()
            # Extract the row in the database that corresponds to the given code
            query="SELECT EXISTS(SELECT * FROM Tickets WHERE (code='" + given_code + "' AND valid=1));"
            mycursor.execute(query)
            mysql.connection.commit()
            result = str(mycursor.fetchall())
            # 'result' is one long string with the query and the result in it.
            # The fourth-from-last character is the actual boolean status of the ticket validity.
            if result[-4] == '1':    
                # If the given code is valid
                # Update the validity of the code in the database
                query="UPDATE Tickets SET valid=0 WHERE code='" + given_code + "';"
                mycursor.execute(query)
                mysql.connection.commit()
                # Color and status are active variables which are passed to the hmtl file
                # to dynamically update how the page looks. 
                color='green' 
                status='valid!'
            else:
                color='red'
                status='wrong (or has already been used).'
            mycursor.close()
        return render_template('scan_tickets.html', given_code=given_code, status=status, color=color)
    return redirect(url_for('login'))

# Logic for page that shows all the tickets in the database
@app.route('/login/home/show_tickets', methods=['GET', 'POST'])
def show_tickets():
    if 'loggedin' in session:
        # Print all the tickets that are in the database.
        query = "SELECT * FROM Tickets ORDER BY name ASC"
        mycursor = mysql.connection.cursor()
        mycursor.execute(query)
        mysql.connection.commit()
        result = mycursor.fetchall() # Result is a tuple filled with dictionaries
        # The following loop restructers only relevant info into a list of lists.
        # This list of lists is used to display the data in the html file. 
        data = []
        for row in result:
            data_row = []
            name = row.get('name')
            code = row.get('code')
            validity = row.get('valid')
            data_row.append(name)
            data_row.append(code)
            data_row.append(validity)
            data.append(data_row)     
        return render_template('show_tickets.html', data=data)
    return redirect(url_for('login'))


# Logic for the page that sends tickets to the database
@app.route('/login/home/send_tickets', methods=['GET', 'POST'])
def send_tickets():
    if 'loggedin' in session:
        if request.method == 'POST':
        # Extract the info which is submitted by the user in the form 
            info = request.form
            sender_email = info['sender_email']
            excel_file = info['excel_file']
            subject = info['subject']
            message = info['message']
            password = info['password']
 
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

