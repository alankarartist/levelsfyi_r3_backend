from flask import Flask, request, jsonify
from ingestion import ingest_data
from retrieval import get_median
import json
import urllib.parse

# Initialize Flask app
app = Flask(__name__)

# Endpoint for data ingestion
@app.route('/ingest', methods=['GET', 'POST'])
def ingest():
    url = request.args.get('url')
    url = urllib.parse.unquote(url)
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        # Call the ingestion logic
        ingest_data(url)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for retrieving the median of sensor readings
@app.route('/median', methods=['GET'])
def median():
    # Retrieve filters from query parameters
    filter_json = request.args.get('filter', '{}')
    filter_json = urllib.parse.unquote(filter_json)
    filters = json.loads(filter_json)
    try:
        # Call the retrieval logic to get the median
        result = get_median(filters)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main entry point for running the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
