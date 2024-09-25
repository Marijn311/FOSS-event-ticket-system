from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import pandas as pd
import time

"""
Ticket system 
Created by Marijn Borghouts
Heavy inspiration was taken form: https://codeshack.io/login-system-python-flask-mysql/
"""

app = Flask(__name__)

# Secret key for extra protection. (I forgot how this worked though)
app.secret_key = '33PilsIsLekker35'

# Connect to the database
app.config['MYSQL_USER'] ="u0rzyyrzeczuua0e"
app.config['MYSQL_PASSWORD'] = "0gAOcli6gNMMMn3zzz31"
app.config['MYSQL_HOST'] = "balbwuq2vgphmafftda4-mysql.services.clever-cloud.com"
app.config['MYSQL_DB'] = "balbwuq2vgphmafftda4"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# Logic for the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    errormsg=""
    username=""
    password=""
    # If fields are filled in, create local variables
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']    
        """ 
        Create session data if credentials are valid
        Session variables basically act like browser cookies. They are stored on the webserver as opposed to the user's browser.
        So the session data can be passed to the home page to validate if the persons has logged in or not.
        This prevents "hackers" from just navigating to http/IP/login/home and skipping the login step.
        """
    if username == 'Marijn' and password == 'Pils': # Hardcoded valid account credentials
            
            
            session['loggedin'] = True
            session['id'] = 1
            session['username'] = 'Marijn Borghouts'
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
            if 'scan_tickets' in request.form:
                return redirect(url_for('scan_tickets'))
            elif 'show_tickets' in request.form:
                return redirect(url_for('show_tickets'))
            elif 'send_tickets' in request.form:
                return redirect(url_for('send_tickets'))
        return render_template('home.html')
    # if not logged in you get sent to login page
    return redirect(url_for('login'))



# Logic for ticket scanning page
@app.route('/login/home/scan_tickets', methods=['GET', 'POST'])
def scan_tickets():
    # Check if user is logged in then show main page
    if 'loggedin' in session:
        given_code=' '
        status = ' '
        color = 'grey'
        if request.method == "POST":
            # Fetch the info associated with the given code
            info = request.form
            given_code = info['fcode']
            mycursor = mysql.connection.cursor()
            query="SELECT EXISTS(SELECT * FROM Tickets WHERE (code='" + given_code + "' AND valid=1));"
            mycursor.execute(query)
            mysql.connection.commit()
            result = str(mycursor.fetchall())
            # 'result' is one long string with the query and the result in it.
            # The fourth-from-last character is the actual boolean status of the ticket validity.
            if result[-4] == '1':    
                # If the given code is valid then a guest has been admitted.
                # Now we need to update the validity of the code in the database, 
                # else everyone could use the same ticket.
                query="UPDATE Tickets SET valid=0 WHERE code='" + given_code + "';"
                mycursor.execute(query)
                mysql.connection.commit()
                color='green' 
                status='valid!'
                # Color and status are active variables which are passed to the hmtl file
                # to dynamically update how the page looks. 
            else:
                color='red'
                status='wrong (or has already been used).'
            mycursor.close()
        return render_template('scan_tickets.html', given_code=given_code, status=status, color=color)
    # if not logged in you get send to login page.
    return redirect(url_for('login'))

# Logic for page that shows all the tickets in the database
@app.route('/login/home/show_tickets', methods=['GET', 'POST'])
def show_tickets():
    # Check if user is logged in 
    if 'loggedin' in session:
        # Print all the tickets that are in the database.
        query = "SELECT * FROM Tickets ORDER BY name ASC"
        mycursor = mysql.connection.cursor()
        mycursor.execute(query)
        mysql.connection.commit()
        result = mycursor.fetchall() # Result is a tuple filled with dictionaries,
        # the following loop restructers only relevant info into a list of lists. 
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
            # If not logged in you get send to login page
    return redirect(url_for('login'))


# Logic for the page that sends tickets to the database
@app.route('/login/home/send_tickets', methods=['GET', 'POST'])
def send_tickets():
    # Check if user is logged in
    if 'loggedin' in session:
        # If the user has filled in the form then the info is stored in the database.
        # assert 4 == 5, "This is an assertion error" # This works

        if request.method == 'POST':
            assert 4 == 5, "This is an assertion error" #
            info = request.form
            sender_email = info['sender_email']
            excel_file = info['excel_file']
            message = info['message']

            assert message == "xxx", "The message is not xxx"
            
            
            print("form was sumbitted at", time.time())
            #load the uploaded file from the user
            file = request.files['file']
            # Read the xlsx file into a dataframe
            df = pd.read_excel(file)
             
            # Process the dataframe as needed
            # For example, you can iterate over the rows and insert them into the database
            for index, row in df.iterrows():
                name = row['name']
                code = row['code']
                valid = row['valid']
                query = "INSERT INTO Tickets (name, code, valid) VALUES (%s, %s, %s)"
                mycursor = mysql.connection.cursor()
                mycursor.execute(query, (name, code, valid))
                mysql.connection.commit()
            mycursor.close()
        return render_template('send_tickets.html')
    # If not logged in you get send to login page
    return redirect(url_for('login'))




# Actually host the website on the specified IP adress and propper port.
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8181)



""" 
###EIGEN AANTEKENINGEN###

-Als je 'ipconfig' in je terminal typt dan kun je, je IP adressen zien. 
IPv4 is je eigen laptops "interne" IP adress wat je apparaten van je modem krijgen als ze op de wifi zitten.
De default gateway is het "externe" IP adress (het adress van je modem zelf).
Als je iemand van buiten af (buiten de wifi waarop deze website runt) op de website wil laten,
heb je het externe IP adress nodig (om naar de modem te komen) en het goede port nummer (om naar het goede apparaat te komen). 
LET OP dat deze adressen kunnen veranderen, zelfs binnnen je eigen netwerk, dit is onhandig.
Als je deze in je browser je "default gateway" gooit ga je naar de website van je provider.
Hier kan je de 'port forward' en IP adress instellen en vastzetten zodat hij niet meer veranderd.
Het probleem is dat je deze website wss niet op de uni kan runnen. Want wij kunnen niet bij de modem instellingen van de TU/e.
En een intern Ip gebruiken werkt misschien ook niet omdat die wss door de firewall geblokkeerd wordt.
En dan werkt de site alleen als je op de uni bent, en dus niet bij de Villa.


"""