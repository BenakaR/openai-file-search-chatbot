from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from utils.chat_handler import generate_context_from_files, ask_chatbot
import markdown

md = markdown.Markdown(extensions=["fenced_code"])

history = {}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        result = generate_context_from_files(file_path)
        return jsonify({'success': True, 'file_ids': result})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = ask_chatbot(data['message'], history)
        history[data['message']] = response
        return jsonify({'response': md.convert(response)})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/get_history', methods=['GET'])
def get_history():
    data = []
    for key, value in history.items():
        data.append({'user': key, 'assistant': value})

    try:
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)