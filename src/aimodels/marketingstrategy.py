from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from typing import Dict, Optional
from dotenv import load_dotenv
import os
from flask_cors import CORS  # Import CORS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
 # Load .env file

app = Flask(__name__)
CORS(app)

class MarketingStrategyPlanner:
    def __init__(self, api_key: str):
        """Initialize the planner with API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-exp-1206')

    def create_marketing_strategy_prompt(self, inputs: Dict[str, str]) -> str:
        """Creates a concise prompt with essential inputs for generating a marketing strategy."""
        return f"""As a professional marketing consultant, create a detailed and actionable marketing strategy based on the inputs provided below. Separate the explanation into **Input Details** and **Recommended Marketing Strategy**.

 **INPUT DETAILS**

    BASIC BUSINESS INFORMATION:
    - Product/Service: {inputs.get('product_service', 'Your Product/Service')}
    - Budget (Monthly): {inputs.get('budget', '$1000')}
    - Time Available Per Week: {inputs.get('time_per_week', '10 hours')}

    TARGET CUSTOMER PROFILE:
    - Age Group: {inputs.get('age_group', '18-25')}
    - Income Level: {inputs.get('income_level', 'Middle income')}
    - Location: {inputs.get('location', 'City-wide')}

    MARKETING CHANNELS:
    - Social Media Platforms: {inputs.get('social_media', 'Instagram, WhatsApp Business')}
    - Local Marketing Methods: {inputs.get('local_marketing', 'Flyers, Local events')}
    - Online Presence: {inputs.get('online_presence', 'Google Business Profile')}

    **RECOMMENDED MARKETING STRATEGY**
    - Based on the input details above, provide a tailored marketing plan that aligns with the given budget, time availability, and customer profile.
    """

    def generate_marketing_strategy(self, user_inputs: Dict[str, str]) -> Optional[str]:
        """Generates a marketing strategy using the Gemini API."""
        try:
            prompt = self.create_marketing_strategy_prompt(user_inputs)
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=8192
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating marketing strategy: {str(e)}")
            return None

generator = None



@app.route('/generate', methods=['POST'])
def generate_strategy():
    try:
        data = request.get_json()
        marketing_strategy = generator.generate_marketing_strategy(data)
        if marketing_strategy:
            return jsonify({'success': True, 'strategy': marketing_strategy})
        return jsonify({'success': False, 'error': 'Failed to generate strategy'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    generator = MarketingStrategyPlanner(api_key)
    app.run(debug=True, port=5000)
