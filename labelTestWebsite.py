from flask import Flask, render_template, request

import sys
import json

import torch
from utils import (load_tokenizer, load_model, load_peft_model, get_device, 
                   generate_text, run_prompt, check_adapter_path, generate_string)

app = Flask(__name__)

class LabelManager:
    def __init__(self):
        self.initialized = False
        self.labels = []
        self.model_name = "../model-cache/microsoft/phi-2"
        self.adapters_name = "../models/qlora/qlora/gpu-cpu_model/adapter"  # Ensure this path is correctly set before running
        self.torch_dtype = torch.bfloat16  # Set the appropriate torch data type
        self.quant_type = 'nf4'  # Set the appropriate quantization type
        self.model = None

    def initialize(self):
        check_adapter_path(self.adapters_name)
        self.tokenizer = load_tokenizer(self.model_name)

        self.model = load_model(self.model_name, self.torch_dtype, self.quant_type)
        self.model.resize_token_embeddings(len(self.tokenizer))
        
        self.model = load_peft_model(self.model, self.adapters_name)
        self.device = get_device()
        self.model.to(self.device)
        self.initialized = True

    def hasInitialized(self):
        return self.initialized

    def getLabels(self, inputString):
        template = "Your job is to label GitHub issues to help teams identify which part of the product the issue is in. You should apply labels that best describe the area of the product that the issue is related to. Output them as a comma separated list, and do not output anything else besides a label list.\n\n===Issue Info===\n{}\n\n===Labels to apply===\n"
        resultString = generate_string(self.model, self.tokenizer, self.device, inputString, template)
        return resultString
    
labelManager = LabelManager()

def my_python_function():
    # Replace this with your actual function
    return "Hello, World!"

@app.route('/')
def home():
    result = my_python_function()
    return render_template('index.html')

@app.route('/api/calculateLabels', methods=['POST'])
def get_ticket_labels():
    data = request.get_json()
    
    if not labelManager.hasInitialized():
        return "Error: Not initialized"

    if 'inputText' not in data:
        return "Error: No inputText provided"
    
    returnLabels = labelManager.getLabels(data['inputText'])
    
    return returnLabels

@app.route('/api/loadModel')
def loadModel():
    
    labelManager.initialize()
    
    return "Model loaded!"

if __name__ == '__main__':
    app.run(debug=True)