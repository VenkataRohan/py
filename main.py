import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from test import dataframe_unmatched_col
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use 465 for SSL or 587 for TLS
sender_email = 'rohankvr12@gmail.com'
sender_password =os.getenv("PASSWORD")
recipient_email = 'venkatarohank@gmail.com'
subject = 'Unmatched columns'



# Convert the DataFrame to a CSV file
csv_data = dataframe_unmatched_col.to_csv(index=False)

# Create an email message
email_message = MIMEMultipart()
email_message['From'] = sender_email
email_message['To'] = recipient_email
email_message['Subject'] = subject

# Attach the CSV data as an attachment
attachment = MIMEApplication(csv_data.encode('utf-8'))
attachment.add_header('content-disposition', 'attachment', filename='data.csv')
email_message.attach(attachment)

# Connect to the SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as server:
    # Start TLS (Transport Layer Security) for security (if using port 587)
    server.starttls()

    # Log in to the email account
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, email_message.as_string())

print('Email with DataFrame attached sent successfully.')