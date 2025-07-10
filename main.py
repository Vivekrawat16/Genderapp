import os
from flask import Flask
from app import views

app = Flask(__name__)

app.add_url_rule(rule='/', endpoint='home', view_func=views.index)
app.add_url_rule(rule='/app/', endpoint='app', view_func=views.app)
app.add_url_rule(rule='/app/gender/', 
                 endpoint='gender',
                 view_func=views.genderapp,
                 methods=['GET', 'POST'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # use PORT if set, else default to 8080
    app.run(host="0.0.0.0", port=port)
