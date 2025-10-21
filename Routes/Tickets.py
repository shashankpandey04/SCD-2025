from flask import Blueprint, render_template, jsonify, request
from Database.mongo import db
from datetime import datetime
from pymongo import ReturnDocument

ticket_bp = Blueprint('ticket', __name__, url_prefix='/ticket')


@ticket_bp.route('/', methods=['GET'])
def ticket_page():
    tiers = list(db.ticket_tiers.find({}, {"_id": 0}))
    return render_template("ticket/index.html", tiers=tiers)


@ticket_bp.route('/process', methods=['POST'])
def process_ticket():
    data = request.form
    tier = data.get("tier")
    name = data.get("name")
    email = data.get("email")
    company = data.get("company")
    role = data.get("role")

    if not tier:
        return jsonify({"error": "Ticket tier not selected"}), 400

    # Step 1: Atomically check and increment the sold count
    result = db.ticket_tiers.find_one_and_update(
        {"tier": tier, "$expr": {"$lt": ["$sold", "$limit"]}},
        {"$inc": {"sold": 1}},
        return_document=ReturnDocument.AFTER
    )

    if not result:
        # Tier full (no tickets left)
        return jsonify({"error": f"{tier} tickets are sold out."}), 400

    # Step 2: Create ticket record
    ticket_doc = {
        "tier": tier,
        "name": name,
        "email": email,
        "company": company,
        "role": role,
        "payment_status": "pending",
        "timestamp": datetime.utcnow()
    }

    db.tickets.insert_one(ticket_doc)

    # TODO: integrate payment gateway (Razorpay, Stripe, etc.)
    # For now we return a success
    return jsonify({
        "success": f"Your {tier} ticket has been reserved successfully!",
        "tier": tier
    })
