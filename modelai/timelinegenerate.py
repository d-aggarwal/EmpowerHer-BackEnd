import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),'..', '.env'))
 # Load .env file

app = Flask(__name__)
CORS(app)

class TimelinePlanner:
    def __init__(self, api_key: str):
        """Initialize the planner with the API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-exp-1206')

    def generate_timeline(self, business_idea: str):
        """Generate a timeline planner for the business idea."""
        try:
            prompt = f"""
            Create a timeline for implementing the business idea: {business_idea}.
            Include major milestones such as:
            - Research and planning
            - Product development
            - Market entry and customer acquisition
            - Scaling and growth
            - Long-term goals and expansion
            Provide specific tasks and target months for completion.
            """
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=8192
                )
            )
            tasks = response.text.split('\n')
            timeline = {}
            for task in tasks:
                match = re.search(r"(.+):\s*(.+)", task)
                if match:
                    milestone, target_date = match.groups()
                    timeline[milestone.strip()] = target_date.strip()
            return timeline
        except Exception as e:
            print(f"Error generating timeline: {str(e)}")
            return None


@app.route('/timelinegenerate', methods=['POST'])
def generate():
    try:
        # Get JSON input from the request
        data = request.get_json()
        business_idea = data.get('business_idea')

        if not business_idea:
            return jsonify({"error": "Business idea is required."}), 400

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({"error": "API key is not configured."}), 500

        # Initialize the planner with the API key
        planner = TimelinePlanner(api_key)
        timeline = planner.generate_timeline(business_idea)

        if timeline:
            return jsonify(timeline)
        else:
            return jsonify({"error": "Failed to generate timeline."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port =  5004)
