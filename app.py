from flask import Flask, render_template, request, jsonify
from main import takeCommand, process_query

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/listen', methods=['POST'])
def listen():
    try:
        query = takeCommand()
        if query:
            return jsonify({"success": True, "query": query})
        return jsonify({"success": False, "query": ""})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        query = data.get('query', '')
        if query:
            response_text = process_query(query)
            return jsonify({"success": True, "response": response_text})
        return jsonify({"success": False, "response": "Empty query."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001