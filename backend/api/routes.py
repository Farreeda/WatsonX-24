# api/routes.py
from flask import Blueprint, jsonify, request
from .models import db, DataEntry

main = Blueprint('main', __name__)

@main.route('/api/data', methods=['GET'])
def get_data():
    entries = DataEntry.query.all()
    data = [{'id': entry.id, 'content': entry.content} for entry in entries]
    return jsonify(data), 200

@main.route('/api/data', methods=['POST'])
def set_data():
    data = request.json
    new_entry = DataEntry(content=data['content'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'status': 'success', 'id': new_entry.id}), 201
