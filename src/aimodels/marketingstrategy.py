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
        """Creates a structured prompt from user's inputs."""
        return f"""As a professional marketing consultant, create a detailed marketing strategy based on this information:

BASIC BUSINESS INFORMATION:
- Business Name: {inputs.get('business_name', 'Your Business Name')}
- Product/Service: {inputs.get('product_service', 'Your Product/Service')}
- Budget (Monthly): {inputs.get('budget', '$1000')}
- Time Available Per Week: {inputs.get('time_per_week', '10 hours')}

TARGET CUSTOMER PROFILE:
- Age Group: {inputs.get('age_group', '18-25')}
- Income Level: {inputs.get('income_level', 'Middle income')}
- Location: {inputs.get('location', 'City-wide')}

MARKETING CHANNELS:
- Social Media Platforms: {inputs.get('social_media', 'Instagram, Facebook, WhatsApp Business')}
- Local Marketing Methods: {inputs.get('local_marketing', 'Flyers, Local events')}
- Online Presence: {inputs.get('online_presence', 'Google Business Profile, Simple website')}

CONTENT PLAN:
- Weekly Tasks:
  - Post photos of products/services: {inputs.get('post_photos', '2-3 times per week')}
  - Share customer reviews: {inputs.get('share_reviews', '1-2 times per week')}
  - Announce offers/updates: {inputs.get('announce_offers', '1 time per week')}
  - Respond to customer messages: {inputs.get('respond_messages', 'Daily')}

BUDGET DIVISION:
- Online advertising: {inputs.get('online_advertising', '50%')}
- Printed materials: {inputs.get('printed_materials', '20%')}
- Events/local marketing: {inputs.get('local_marketing_budget', '20%')}
- Customer offers: {inputs.get('customer_offers_budget', '10%')}

SUCCESS TRACKING:
- Metrics to track:
  - New customers per week
  - Customer feedback ratings
  - Weekly sales increase
  - Social media followers growth
  - WhatsApp group engagement

Please create a detailed and actionable marketing strategy based on these inputs."""

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
    app.run(debug=True)
