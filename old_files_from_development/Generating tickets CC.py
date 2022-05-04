# -*- coding: utf-8 -*-
"""
Ticket systeem 
Made by Marijn Borghouts
"""
import random 
import string
import smtplib
import pandas as pd
import mysql.connector
#pip3 install mysql-connector-python-rf

# Connect to database
mydb = mysql.connector.connect(
  host="balbwuq2vgphmafftda4-mysql.services.clever-cloud.com",  
  user="u0rzyyrzeczuua0e",
  password="0gAOcli6gNMMMn3zzz31",
  database="balbwuq2vgphmafftda4",
  port="3306",
)

# Create cursor in that database, this is an object needed to send and retrieve info from the database
mycursor = mydb.cursor(buffered=True)


#Load email list 
loaded_exel = pd.read_excel (r'C:/Users/20192010/Downloads/a_commissies/a_fissacom/Tickets/EventTiks/Deelnemerslijst.xlsx') 
email_list = loaded_exel['Email'].tolist()
names_list = loaded_exel['Names'].tolist()
#'Email' has to be the name (value of first row) of a column. The same goes for "Names" etc
#Place "r" before the path string to address special character, such as '\'. 


#Generate random codes
def generate_code():
    code_length=3 
    #With 3 letters in a code there 26^3=17.576 possible combinations. Assume a party has 
    #guests than one in 17.576/200=88 codes are valid. So guessing won't effectively work.
    random_code = ''.join(random.choices(string.ascii_letters,k=code_length))
    random_code = random_code.upper()
    return random_code


#To send an email. (Be aware that it may end up in the spam folder...)
#You need to allow less secure apps to acces gmail in your gmail settings in order to allow this script to send mails via your account.
#I suggest making a new gmail account when we use this more often for Prot activities.
sender_email= 'marijnborghouts@gmail.com'
password = input(str("Please enter gmail (google) password. BE AWARE!!!; entering a correct password will automatically send out all the mails!!!:"))


# #Delete table called Tickets
# query = "DROP TABLE Tickets"
# mycursor.execute(query)
# mydb.commit()


# #Create table called Tickets
# query = "CREATE TABLE Tickets (name VARCHAR(30) NOT NULL, email VARCHAR(30) NOT NULL, code VARCHAR(50) PRIMARY KEY, valid TINYINT(1))"
# mycursor.execute(query)
# mydb.commit()


# #Delete table called Accounts
# query = "DROP TABLE Accounts"
# mycursor.execute(query)
# mydb.commit()


# #Create table called Accounts
# query = "CREATE TABLE Accounts (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30) NOT NULL, password VARCHAR(200) NOT NULL)"
# mycursor.execute(query)
# mydb.commit()

# query = "INSERT INTO Accounts (username, password) VALUES ('testusername', 'testpass')"
# mycursor.execute(query)
# mydb.commit()

#Clear out the table before filling it again (* did not work so I just dirty fixt it by taking valid!=5)
query = "DELETE FROM Tickets WHERE valid!=5"
mycursor.execute(query)
mydb.commit()


valid_codes=[]

with smtplib.SMTP('smtp.gmail.com', 587) as smtp: #587 is the port number 
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender_email, password)
    
    
    #Change the contents of the mail based on the activity
    for i in range(len(email_list)):
        receiver_email=email_list[i]
        save_code = generate_code()
        #if the generated random code already exists, make a new code
        if save_code in valid_codes:
            save_code = generate_code()
        valid_codes.append(save_code)
            
        subject = 'Jouw unieke toegangscode voor activiteit X'
        body = 'Beste ' + names_list[i] + ', jouw unieke toegangscode is: ' + save_code #Here you write the actual message
        message = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(sender_email, receiver_email, message)
        
        #Add rows to the database
        query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
        val = (names_list[i], receiver_email, save_code, True)
        mycursor.execute(query, val)
        mydb.commit()
        
print('Emails with tickets have succesfully been send.')
        

#print table contents
query = "SELECT * FROM Tickets ORDER BY name ASC"
mycursor.execute(query)
mydb.commit() 
# fetch all rows 
result = mycursor.fetchall()
for row in result:
    print(row)
    print("\n")