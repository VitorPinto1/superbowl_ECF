from flask import Flask, render_template, redirect, session, request, url_for, jsonify, flash, Blueprint
from flask_pymongo import PyMongo
from pymongo import MongoClient
from decouple import config
from bson.objectid import ObjectId, InvalidId
from itertools import combinations 
from flask_apscheduler import APScheduler



from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
from functools import wraps
from decimal import Decimal
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import json
import random
import string

from flaskext.mysql import MySQL

from dotenv import load_dotenv
import os
from faker import Faker 
fake = Faker()

