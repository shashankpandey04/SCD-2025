from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from flask import Blueprint, render_template, flash, redirect, jsonify, request, session
from flask_login import login_required, current_user
from Database.mongo import db
from dotenv import load_dotenv
import os

cashfree_bp = Blueprint('cashfree', __name__)

load_dotenv()

CASHFREE_CLIENT_ID = os.getenv("CASHFREE_CLIENT_ID")
CASHFREE_CLIENT_SECRET = os.getenv("CASHFREE_CLIENT_SECRET")
CASHFREE_ENVIRONMENT = os.getenv("CASHFREE_ENVIRONMENT")

TICKET_PRICE = os.getenv('TICKET_PRICE')

Cashfree.XClientId = CASHFREE_CLIENT_ID
Cashfree.XClientSecret = CASHFREE_CLIENT_SECRET
Cashfree.XEnvironment = CASHFREE_ENVIRONMENT
x_api_version = "2025-01-01"

#DOCS
#https://www.cashfree.com/docs/payments/online/web/redirect

#https://www.cashfree.com/docs/api-reference/payments/latest/orders/create

