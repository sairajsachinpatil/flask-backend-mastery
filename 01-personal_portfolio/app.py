import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()


# =========================
# CREATE FLASK APP
# =========================

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


# =========================
# EMAIL CONFIGURATION
# =========================

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("home.html")


# =========================
# PROJECTS
# =========================

@app.route("/projects")
def projects():
    return render_template("projects.html")


# =========================
# CONTACT FORM
# =========================

@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    try:

        msg = Message(
            subject=f"Portfolio Contact: {subject}",
            sender=app.config["MAIL_USERNAME"],
            recipients=[app.config["MAIL_USERNAME"]],
            reply_to=email
        )

        msg.body = f"""
You received a new message from your portfolio website.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

        mail.send(msg)

        flash(
            "Your message has been sent successfully!",
            "success"
        )

    except Exception as e:

        print("EMAIL ERROR:", e)

        flash(
            "Sorry, something went wrong. Please try again.",
            "error"
        )

    return redirect(url_for("home") + "#contact")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)