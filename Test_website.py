# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:54:31 2022

@author: 20192010
"""

<<<<<<< HEAD:Checking tickets website.py
from flask import Flask, request, render_template, redirect, url_for, session
=======
from flask import Flask, request, render_template, redirect, url_for
>>>>>>> parent of b0236e7 (opgeschoont):Test_website.py
from flask_mysqldb import MySQL
#from werkzeug.security import generate_password_hash, check_password_hash
#import re







app = Flask(__name__)

app.config['MYSQL_USER'] ="u0rzyyrzeczuua0e"
app.config['MYSQL_PASSWORD'] = "0gAOcli6gNMMMn3zzz31"
app.config['MYSQL_HOST'] = "balbwuq2vgphmafftda4-mysql.services.clever-cloud.com"
app.config['MYSQL_DB'] = "balbwuq2vgphmafftda4"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)


<<<<<<< HEAD:Checking tickets website.py
#ER MOET NOG EEN INLOG BEVEILIGING OPKOMEN
# 
#app.secret_key = 'VoVoorMarijn'
=======

>>>>>>> parent of b0236e7 (opgeschoont):Test_website.py

# @app.route('/pythonlogin/', methods=['GET', 'POST'])
# def login():
#     # Output message if something goes wrong...
#     msg = ''
#     return render_template('Index.html', msg='')



# @app.route('/pythonlogin/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
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



    
if __name__ == "__main__":
    app.run(debug=True, port=8181)

<<<<<<< HEAD:Checking tickets website.py
# Het is misschien ook nog leuk om te kijken of we van http naar https kunnen gaan. 
# Volgens TechNiek hebben we daar een gratis certificaat voor nodig    

###EIGEN AANTEKENINGEN###
# In cmd typ je 'ipconfig'. IPv4 is je eigen laptops interne ipadress.
# De 'default gateway' is het adress van je modem.
# Als je deze in je browser gooit ga je naar de website van je provider.
# Hier kan je de 'port forward' bepalen naar je laptop zodat je vanaf een ander network ook op de website kan.
# Het probleem is dat je deze website wss niet op de uni kan runnen. Want wij kunnen niet bij de modem instellingen van de TU/e.
# En een intern IP op TU/e gebruiken gaat wss niet omdat de TU's firewall dat blokkeerd.
# Ik wil kijken of ik de website bijvoorbeeld op een raspberry pi kan runnen en die dan gewoon altijd aan laten ergens in een kastje.
=======
>>>>>>> parent of b0236e7 (opgeschoont):Test_website.py
