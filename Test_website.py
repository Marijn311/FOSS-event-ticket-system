# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:54:31 2022

@author: 20192010
"""

from flask import Flask, request, render_template
from flask_mysqldb import MySQL



app = Flask(__name__)

app.config['MYSQL_USER'] ="u0rzyyrzeczuua0e"
app.config['MYSQL_PASSWORD'] = "0gAOcli6gNMMMn3zzz31"
app.config['MYSQL_HOST'] = "balbwuq2vgphmafftda4-mysql.services.clever-cloud.com"
app.config['MYSQL_DB'] = "balbwuq2vgphmafftda4"
app.config['MYSQL_PORT'] = '3306'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'






mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        mycursor = mysql.connection.cursor()
        query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
        val = (firstName, lastName, 'save_code', True)
        mycursor.execute(query, val)
        mysql.connection.commit()
        mycursor.close()
        print('gelukt bitches')
    return render_template('homepage.html')



    
if __name__ == "__main__":
    app.run(debug=True, port=8181)

    