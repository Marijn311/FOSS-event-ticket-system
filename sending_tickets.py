# -*- coding: utf-8 -*-
"""
Ticket systeem 
Made by Marijn Borghouts
"""
import random 
import string
import smtplib
import pandas as pd
import mysql.connector # pip3 install mysql-connector-python-rf

"""
Connect to database
This is a very small database that is hosted online on "clever cloud".
Clever cloud offers a free hosted database for very small developer testing.
It can store something like 10MB but that is enough for this purpose.
"""
mydb = mysql.connector.connect(
  host="balbwuq2vgphmafftda4-mysql.services.clever-cloud.com",  
  user="u0rzyyrzeczuua0e",
  password="0gAOcli6gNMMMn3zzz31",
  database="balbwuq2vgphmafftda4",
  port="3306",
)
# Create cursor in the database, this is an object needed to send and retrieve info from the database
mycursor = mydb.cursor(buffered=True)


# Load email list 
# This locations has to be adjusted depending on where the "participants" excel file is safed.
loaded_exel = pd.read_excel (r'C:/Users/20192010/Downloads/a_commissies/a_fissacom/Tickets/EventTiks/participants#.xlsx') 
email_list = loaded_exel['Email'].tolist()
names_list = loaded_exel['Names'].tolist() 
"""
For privacy reasons it is better to not put more info than a first name int he datbase.
Since this is not needed for the script to work. 
'Email' has to be the name (value of first row) of a column. The same goes for "Names" etc
Place "r" before the path string to address special character, such as '\'. 
"""

# Generate random codes
def generate_code():
    code_length=3 
    """
    With 3 letters in a code there 26^3=17.576 possible combinations. 
    # Assume a party or other activate has 200 guests than one in 17.576/200=~88 codes are valid. 
    # So guessing won't effectively work. If you update it to 4 letters than there are way more options. 
    # Using letter codes instead of QR codes saves phone battery for the scanner and save 4G data usage.
    """
    random_code = ''.join(random.choices(string.ascii_letters,k=code_length))
    random_code = random_code.upper()
    return random_code

"""
To send an email the follwoing section is used. (Be aware that it may end up in the spam folder...)
You need to allow less secure apps to acces gmail in your gmail settings in order to allow this script to send mails via your account.
I suggest making a new gmail account when we use this more often for Prot activities.
"""
sender_email= 'marijnborghouts@gmail.com'
password = input(str("Please enter gmail (google) password. BE AWARE!!!; entering a correct password will automatically send out all the mails!!!:"))

# Clear out the Tickets table before filling it again (* did not work so I just dirty fixed it by taking valid!=5, since this includes all values)
query = "DELETE FROM Tickets WHERE valid!=5"
mycursor.execute(query)
mydb.commit()

# Setup the email connection
with smtplib.SMTP('smtp.gmail.com', 587) as smtp: #587 is the port number 
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender_email, password)
    valid_codes=[]  
    # Change the contents of the mail based on the activity
    for i in range(len(email_list)):
        receiver_email=email_list[i]
        save_code = generate_code()
        # If the generated random code already exists, make a new code
        if save_code in valid_codes:
            save_code = generate_code()
        valid_codes.append(save_code)
        # Here you write the actual message that people get in the mail.    
        subject = 'Jouw unieke toegangscode voor activiteit X'
        body = f'Beste {names_list[i]},\n\n jouw unieke toegangscode is: {save_code}. \n\n Have Fun!' 
        message = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(sender_email, receiver_email, message)
        
        # Add the send-out ticket to the database
        query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
        val = (names_list[i], receiver_email, save_code, True)
        mycursor.execute(query, val)
        mydb.commit()
        
print('Emails with tickets have succesfully been send.')