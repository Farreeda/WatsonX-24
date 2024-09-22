# api/routes.py
from flask import Blueprint, jsonify, request
from .models import db, DataEntry
from .helpers import append_prompt, update_file, extract_text_from_pdf, add_context_to_file, clear_file # process_and_embed_text
####
import json
import os
import getpass
import CONSTANTS as constants
# from langchain_ibm import WatsonxLLM
# from langchain.chains import RetrievalQA
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
    
    # db.session.add(new_entry)
    # db.session.commit()
    #update_file(data['message'], generated_response)
    return jsonify({"response": generated_response}), 201


@main.route('/get-file-tree', methods=['GET'])
def get_file_tree():
    path = request.args.get('path', '')
    if not os.path.exists(path):
        return jsonify([]), 404

    # List all files and directories in the specified path
    try:
        files = os.listdir(path)
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/send-file-path', methods=['POST'])
def send_file_path():
    data = request.get_json()
    file_path = data.get('filePath', '')
    print(f"Received file path: {file_path}")
    
    text = extract_text_from_pdf(file_path)
    add_context_to_file(text)

    return jsonify({'status': 'success'}), 200

@main.route('/api/clear', methods=['POST'])
def clear_request():
    clear_file()
    return  jsonify({'status': 'success'}), 200
