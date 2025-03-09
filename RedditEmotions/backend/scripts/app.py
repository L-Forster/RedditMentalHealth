import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Use direct imports since they're in the same directory
import classify_facade
import scraper_facade
import training_facade

# Add at the beginning of your Flask app
required_directories = ['user', 'models', 'positive_samples']
for directory in required_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
app = Flask(__name__)
CORS(app)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json

    # Check all required parameters
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    subreddit = data.get('subreddit')
    username = data.get('username')

    if not subreddit:
        return jsonify({'error': 'Missing required parameter: subreddit'}), 400
    if not username:
        return jsonify({'error': 'Missing required parameter: username'}), 400

    try:
        # Check if model exists for this subreddit
        if not os.path.exists("../models"):
            os.makedirs("../models")

        model_files = os.listdir("../models")
        model_file = subreddit + ".sav"

        if model_file not in model_files:
            # Create model if it doesn't exist
            if not os.path.exists("../positive_samples"):
                os.makedirs("../positive_samples")

            samples_files = os.listdir("../positive_samples")
            samples_file = subreddit + ".csv"

            if samples_file not in samples_files:
                # Create the subreddit data
                scraper_facade.main(subreddit, "create")
            # Train the model
            training_facade.main(subreddit, "../positive_samples")

        # Analyze the user's content
        scraper_facade.main(username, "user")
        result = classify_facade.main(subreddit, username)

        # Return the probability
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/api/update-model', methods=['POST'])
def update_model():
    data = request.json
    subreddit = data.get('subreddit')

    if not subreddit:
        return jsonify({'error': 'Missing subreddit parameter'}), 400

    try:
        # Update the subreddit data and retrain model
        scraper_facade.main(subreddit, "update")
        training_facade.main(subreddit, "../positive_samples")

        return jsonify({
            'success': True,
            'message': f'Model for r/{subreddit} updated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-raw', methods=['POST'])
def analyze_raw():
    data = request.json

    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    subreddit = data.get('subreddit')
    raw_text = data.get('text')

    if not subreddit:
        return jsonify({'error': 'Missing required parameter: subreddit'}), 400
    if not raw_text:
        return jsonify({'error': 'Missing required parameter: text'}), 400

    try:
        # Check if model exists for this subreddit
        if not os.path.exists("../models"):
            os.makedirs("../models")

        model_file = subreddit + ".sav"
        if model_file not in os.listdir("../models"):
            # Create model if it doesn't exist
            if not os.path.exists("../positive_samples"):
                os.makedirs("../positive_samples")

            samples_file = subreddit + ".csv"
            if samples_file not in os.listdir("../positive_samples"):
                scraper_facade.main(subreddit, "create")
            training_facade.main(subreddit, "../positive_samples")

        # Analyze raw text
        prob = classify_facade.classify_raw(subreddit, raw_text)
        result = prob[1] if isinstance(prob, list) and len(prob) > 1 else prob

        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)