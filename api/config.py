from flask import Flask, render_template, redirect, session, request, url_for, jsonify, flash, Blueprint
from flask_bootstrap import Bootstrap
from datetime import datetime
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

