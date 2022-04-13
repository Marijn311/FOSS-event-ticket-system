# -*- coding: utf-8 -*-
"""
Ticket systeem 
Made by Marijn Borghouts
"""
import random 
import string
import smtplib
import pandas as pd
import json
import mysql.connector
#pip3 install mysql-connector-python-rf

# Connect to database
mydb = mysql.connector.connect(
  host="localhost",  #To manage database type this IP followed by :8080 in a browser and login with these credentials.
  user="root",
  password="marijn",
  database="Tickets",
  port="3308",
)

# Create cursor in that database, this is an object needed to send and retrieve info from the database
mycursor = mydb.cursor(buffered=True)


#Load email list 
loaded_exel = pd.read_excel (r'C:/Users/20192010/Downloads/a_commissies/a_fissacom/Tickets/Deelnemerslijst.xlsx') 
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
    random_code = random_code.upper() #Make it all capital letters
    return random_code
# =============================================================================
#KUTTT vgm is er een kasn dat er twee keer dezelfde random code gegeneerd wordt
#Dit mag natuurlijk niet.
# =============================================================================

# deze moeten in de database worden geupload als we die gaan gebruiken
valid_codes=[]



#To send an email. (Be aware that it may end up in the spam folder...)
#You need to allow less secure apps to acces gmail in your gmail settings in order to allow this script to send mails via your account.
#I suggest making a new gmail account when we use this more often for Prot activities.
sender_email= 'marijnborghouts@gmail.com'
password = input(str("please enter gmail (google) password. BE AWARE!!!; entering a correct password will automatically send out all the mails!!!:"))


#clear out the table
query = "DELETE FROM Tickets"
mycursor.execute(query)
mydb.commit()

with smtplib.SMTP('smtp.gmail.com', 587) as smtp: #587 is the port number 
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    
    smtp.login(sender_email, password)
    
    
    #Change the contents of the mail based on the activity
    for i in range(len(email_list)):
        receiver_email=email_list[i]
        save_code = generate_code()
        subject = 'Jouw unieke toegangscode voor activiteit X'
        body = 'Beste ' + names_list[i] + ', jouw unieke toegangscode is: ' + save_code #Here you write the actual message
        message = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(sender_email, receiver_email, message)
        valid_codes.append(save_code) #add codes to local python list
        
        #Add files to database
        query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
        val = (names_list[i], receiver_email, save_code, True)
        mycursor.execute(query, val)
        mydb.commit()
        
print('Emails with tickets have succesfully been send.')
        
#Save the generated valid codes to use later whilst checking the tickets.
with open('saved_valid_codes.txt', 'w') as f:
    f.write(json.dumps(valid_codes))
    

 