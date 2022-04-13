# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:54:31 2022

@author: 20192010
"""

from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from termcolor import colored



app = Flask(__name__)

app.config['MYSQL_USER'] ="u0rzyyrzeczuua0e"
app.config['MYSQL_PASSWORD'] = "0gAOcli6gNMMMn3zzz31"
app.config['MYSQL_HOST'] = "balbwuq2vgphmafftda4-mysql.services.clever-cloud.com"
app.config['MYSQL_DB'] = "balbwuq2vgphmafftda4"
app.config['MYSQL_PORT'] = '3306'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

given_code = 'FUK'


mycursor = mysql.connection.cursor()
query="SELECT EXISTS(SELECT * FROM Tickets WHERE (code='" + given_code + "' AND valid=1));"
mycursor.execute(query)
mysql.connection.commit()
result = mycursor.fetchone()

if result[0] == 1:
    message=colored("This code is VALID", 'green')
    #If the code is was valid then it has been used, so we need to update the validity of the code in the database
    query="UPDATE Tickets SET valid=0 WHERE code='" + given_code + "';"
    mycursor.execute(query)
    mysql.connection.commit() 
else:
    message=colored("This code is WRONG (or has been used)", 'bright red' )


print(message)
mycursor.close()



    