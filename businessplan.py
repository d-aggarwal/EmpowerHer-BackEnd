from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from typing import Dict, Optional
import os
from dotenv import load_dotenv
from flask_cors import CORS 

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
 # Load .env file

app = Flask(__name__)
CORS(app)

class BusinessPlanGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-exp-1206')

    def create_business_plan_prompt(self, answers: Dict[str, str]) -> str:
        return f"""You are a professional business consultant. Based on the following information, generate a detailed, practical business plan:

Basic Information:
- Product/Service: {answers.get('product', '')}
- Initial Investment: {answers.get('investment', '')}
- Location: {answers.get('location', '')}
- Target Market: {answers.get('target_market', '')}
- Available Time: {answers.get('hours_per_day', '')} hours per day
- Available Help: {answers.get('help', '')}

Market Analysis:
- Competition Level: {answers.get('competition', '')}
- Location Type: {answers.get('location_type', '')}
- Target Customer Demographics: {answers.get('target_customers', '')}

Financial Overview:
- Starting Capital Range: {answers.get('starting_money', '')}
- Expected Monthly Expenses: {answers.get('monthly_expenses', '')}"""

    def generate_business_plan(self, user_answers: Dict[str, str]) -> Optional[str]:
        try:
            prompt = self.create_business_plan_prompt(user_answers)
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating business plan: {str(e)}")
            return None

generator = None


@app.route('/plangenerate', methods=['POST'])
def generate_plan():
    try:
        data = request.get_json()
        business_plan = generator.generate_business_plan(data)
        if business_plan:
            return jsonify({'success': True, 'plan': business_plan})
        return jsonify({'success': False, 'error': 'Failed to generate plan'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    generator = BusinessPlanGenerator(api_key)
    app.run(debug=True, port = 5001)
