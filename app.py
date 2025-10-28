
# pyright: ignore[reportMissingImports]
from flask import Flask, render_template, request, flash, redirect, url_for #type: ignore
import os
import smtplib
from email.message import EmailMessage


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-change-me')


load_dotenv = lambda: None  
try:
    
    from dotenv import load_dotenv # type: ignore
    load_dotenv()  # <-- only runs if package exists
except ImportError:
    pass  

MAIL_SERVER   = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT     = int(os.getenv('MAIL_PORT', '587'))
MAIL_USE_TLS  = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not all([name, email, message]):
            flash('Please fill all fields.', 'danger')
            return redirect(url_for('contact'))

        # Try to send email
        if MAIL_USERNAME and MAIL_PASSWORD:
            try:
                msg = EmailMessage()
                msg['Subject'] = f"Portfolio: {name}"
                msg['From'] = MAIL_USERNAME
                msg['To'] = MAIL_USERNAME
                msg.set_content(f"Name: {name}\nEmail: {email}\n\n{message}")

                with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
                    if MAIL_USE_TLS:
                        server.starttls()
                    server.login(MAIL_USERNAME, MAIL_PASSWORD)
                    server.send_message(msg)
                flash('Message sent!', 'success')
            except Exception as e:
                print(f"[EMAIL ERROR] {e}")
                flash('Could not send email. Check terminal.', 'warning')
        else:
            # No email config → print to terminal
            print(f"[FORM] Name: {name}, Email: {email}, Message: {message}")
            flash('Email not configured – message printed to terminal.', 'info')

        return redirect(url_for('contact'))

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)