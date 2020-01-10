from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap
import pymonetdb
import os

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
from flask_bootstrap import WebCDN
app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    '//cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/'
)
from app import routes

db_connection = pymonetdb.connect(username="voc", password="voc", hostname="172.19.0.1", database="voc", port="50000")
