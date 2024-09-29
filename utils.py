import random
import string
import smtplib
from flask import flash

# Generate random codes
def generate_code():
    """
    With 3 letters in a code there are 26^3=17.576 possible combinations. 
    # Assume a party or other activity has a maximum of 200 guests than one in 17.576/200=~88 codes are valid, 
    # so guessing won't effectively work. It is always possible to change the code length to create more possible combinations. 
    # Using letter codes instead of QR codes saves phone battery for the scanner. Besides, people can remember three letters
    # so you do not need to wait for everyone to take out there phone at the door.
    """
    code_length = 3 
    random_code = ''.join(random.choices(string.ascii_letters,k=code_length))
    random_code = random_code.upper()
    return random_code



def send_emails(sender_email, password, subject, message, df):
    """
    Sends personalized emails to a list of recipients.
    Args:
        sender_email (str): The email address of the sender.
        password (str): The automation password for the sender's email account.
        subject (str): The subject of the email.
        message (str): The body of the email, containing placeholders [Name] and [Code] for personalization.
        df (pandas.DataFrame): A DataFrame containing recipient information with columns 'Email', 'Name', and 'Code'.
    Returns:
        None
    Raises:
        smtplib.SMTPException: If there is an error with the SMTP connection or sending the email.
    """

    # Setup the email connection
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp: #587 is the port number
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender_email, password)
        for i in range(len(df)):
            receiver_email = df['Email'][i]
            code = df['Code'][i]
            name = df['Name'][i]

            # In message replace [Name] with the name of the person
            message_personal = message.replace('[Name]', name)
            # In message replace [Code] with the code of the person
            message_personal = message_personal.replace('[Code]', code)

            email_content = f'Subject: {subject}\n\n{message_personal}'
            smtp.sendmail(sender_email, receiver_email, email_content)

        # Flash confirmation message
        flash('Tickets have been successfully sent to all recipients!', 'success')   



