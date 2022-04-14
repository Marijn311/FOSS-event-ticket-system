# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:54:31 2022

@author: 20192010
"""

from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL




app = Flask(__name__)

app.config['MYSQL_USER'] ="u0rzyyrzeczuua0e"
app.config['MYSQL_PASSWORD'] = "0gAOcli6gNMMMn3zzz31"
app.config['MYSQL_HOST'] = "balbwuq2vgphmafftda4-mysql.services.clever-cloud.com"
app.config['MYSQL_DB'] = "balbwuq2vgphmafftda4"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
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



    
if __name__ == "__main__":
    app.run(debug=True, port=8181)

