# api/routes.py
from flask import Blueprint, jsonify, request
from .models import db, DataEntry
from .helpers import append_prompt, update_file
####
import json
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
    "temperature": 1.2,
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


@main.route('/api/chat', methods=['POST'])
def set_data():
    data = request.json
    
    message = append_prompt(data['message'])

    generated_response = model.generate_text(prompt=message, guardrails=False)   #Get Model Response

    new_entry = DataEntry(content=generated_response)
    
    # db.session.add(new_entry)
    # db.session.commit()
    update_file(data['message'], generated_response)
    return jsonify({"response": generated_response}), 201


