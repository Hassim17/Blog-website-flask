import jinja2.exceptions
from flask import Flask, render_template, request
import requests
import smtplib

NPOINT = 'https://api.npoint.io/271630460a389ecb68ed'

app = Flask(__name__)

response = requests.get(NPOINT)
posts = response.json()


@app.route('/')
def home():
    return render_template('index.html', blog_posts=posts)


@app.route('/<page>')
def other(page):
    return render_template(page, blog_posts=posts, heading="Contact")


@app.route("/<int:index>")
def show_posts(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=['POST', 'GET'])
def receive_data():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(f"{name}\n{email}\n{phone}\n{message}")
        send_mail(name, email, phone, message)

        return render_template('contact.html', heading="Successfully sent message")
    else:
        return render_template('contact.html', heading="Contact")


def send_mail(name, email, phone, message):
    email_message = f"Subject : Thank you for Contacting\n\nName: {name}\nEmail: {email}\n" \
                    f"Phone Number: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="nowayhome017@gmail.com", password='homecoming17th')
        connection.sendmail(from_addr="nowayhome017@gmail.com", to_addrs=email,
                            msg=email_message)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
