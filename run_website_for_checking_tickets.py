"""
Ticket system 
Created by Marijn Borghouts
Heavy inspiration was taken form: https://codeshack.io/login-system-python-flask-mysql/
"""

from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL

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

@app.route('/login/', methods=['GET', 'POST'])
def login():
    errormsg=''
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
    if username == 'Marijn Borghouts' and password == 'PilsIsLekker35!': # Hardcoded valid account credentials
            session['loggedin'] = True
            session['id'] = 1
            session['username'] = 'Marijn Borghouts'
            # Redirect to home page if login was valid (if the session variables exist)
            return redirect(url_for('home'))
    else:
            errormsg = 'Incorrect username/password!'
    return render_template('loginpage.html', msg=errormsg)


# This is just a placeholder page to always redirect a user to the login page. 
@app.route('/')
def reroute():
   return redirect(url_for('login'))

# This is the code for the actual main page where the tickets can be checked.
@app.route('/login/home', methods=['GET', 'POST'])
def home():
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
        return render_template('homepage.html', given_code=given_code, status=status, color=color)
    # if not logged in you get send to login page.
    return redirect(url_for('login'))

# Logout page where session variables are cleared
# and immediatly after you are redirected to the login page. 
@app.route('/login/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

# Page which shows all tickets and validity
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
        return render_template('show_tickets_page.html', data=data)
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