from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/')

def index():
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y")
    return render_template('index.html', current_date=formatted_date)

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


