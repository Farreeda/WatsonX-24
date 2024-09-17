# api/routes.py
from flask import Blueprint, jsonify, request
from .models import db, DataEntry
from .events import socketio
####
import os
import getpass
import CONSTANTS as constants
from ibm_watsonx_ai.foundation_models import Model
####

model_id = "ibm/granite-13b-chat-v2"

parameters = {
    "decoding_method": "sample",
    "max_new_tokens": 1024,
    "random_seed": 1235676543234,
    "temperature": 1.04,
    "top_k": 33,
    "top_p": 0.89,
    "repetition_penalty": 1
}

project_id = constants.project_id

model = Model(
	model_id = model_id,
	params = parameters,
	credentials = constants.g_credentials,
	project_id = project_id
	)

main = Blueprint('main', __name__)

@main.route('/api/data', methods=['GET'])
def get_data():
    entries = DataEntry.query.all()
    data = [{'id': entry.id, 'content': entry.content} for entry in entries]
    return jsonify(data), 200

@main.route('/api/data', methods=['POST'])
def set_data():
    data = request.json

    generated_response = model.generate_text(prompt=data['content'], guardrails=False)   #Get Model Response

    new_entry = DataEntry(content=generated_response)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'status': 'success', 'id': new_entry.id}), 201

main.route('/api/update')
def update():
    # Your database update logic here
    socketio.emit('update_event', {'data': 'New Data'})
    return jsonify({'status': 'updated'})