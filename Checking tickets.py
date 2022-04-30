# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:54:31 2022
@author: 20192010
"""

from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors 
#These two methods to access the database both work and are both used 
#but it can be rewritten to only use one method (to make the code more compact and more uniform)
import re

app = Flask(__name__)

# Secret key (it's for extra protection)
app.secret_key = '33PilsIsLekker35'

app.config['MYSQL_USER'] ="u0rzyyrzeczuua0e"
app.config['MYSQL_PASSWORD'] = "0gAOcli6gNMMMn3zzz31"
app.config['MYSQL_HOST'] = "balbwuq2vgphmafftda4-mysql.services.clever-cloud.com"
app.config['MYSQL_DB'] = "balbwuq2vgphmafftda4"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# This is the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # If fields are filled in, create local variables
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Check if the account exists 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        # Create session data if the account exists in the database
        # Session variables basically act like browser cookies. They are stored on the server as opposed to the user's browser.
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page if login was valid
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')


#This is to clear the session variables and then return to login screen 
@app.route('/login/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/login/home', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin then show main page
    if 'loggedin' in session:
        given_code=' '
        status = ' '
        color = 'grey'

        if request.method == "POST":
            info = request.form
            given_code = info['fcode']
            mycursor = mysql.connection.cursor()
            query="SELECT EXISTS(SELECT * FROM Tickets WHERE (code='" + given_code + "' AND valid=1));"
            mycursor.execute(query)
            mysql.connection.commit()
            result = str(mycursor.fetchall())
            #result is one long string with the query and the result and the fourth from last character is the actual boolean status
            if result[-4] == '1':
                #If the code is was valid then it has been used, so we need to update the validity of the code in the database
                query="UPDATE Tickets SET valid=0 WHERE code='" + given_code + "';"
                mycursor.execute(query)
                mysql.connection.commit()
                color='green'
                status='VALID'
            else:
                color='red'
                status='WRONG (or has already been used)'
            mycursor.close()

        return render_template('homepage.html', given_code=given_code, status=status, color=color) #result is one long string with the query and the result and the fourth from last character is the actual boolean status


    # if not logged in you get send to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8181)


# Waarom linked de CSS niet? Eigenlijk moet ik kijken of er mobile html opmaakt packages of tutorials zijn.
# Het is misschien ook nog leuk om te kijken of we van http naar https kunnen gaan. 
# Volgens TechNiek hebben we daar een gratis certificaat voor nodig    

###EIGEN AANTEKENINGEN###
# In cmd typ je 'ipconfig'. IPv4 is je eigen laptops interne ipadress.
# de default gateway is het adress van je modem.
# Als je deze in je browser gooit ga je naar de website van je provider
# Hier kan je de 'port forward' bepalen naar je laptop zodat je vanaf een ander network ook op de website kan.
# Het probleem is dat je deze website wss niet op de uni kan runnen. Want wij kunnen niet bij de modem instellingen van de tu.
# En een intern Ip gebruiken werkt misschien ook niet omdat die wss door de firewall geblokkeerd wordt.