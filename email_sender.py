import smtplib
from email.mime.text import MIMEText

def send_email(sender, password, recipient, subject, body):
    """
    Send an email using SMTP.
    Note: For Gmail, enable 'Less secure app access' or use App Passwords.
    Replace with your email provider's SMTP settings if not using Gmail.
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your actual credentials and details
    send_email(
        sender='your_email@gmail.com',
        password='your_app_password',  # Use App Password for Gmail
        recipient='recipient@example.com',
        subject='Test Email',
        body='This is a test email sent from Python.'
    )