from flask import Flask, request, jsonify, send_file, render_template
from typing import Dict, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),'..', '.env'))
 # Load .env file

app = Flask(__name__)
CORS(app)

class BusinessNameGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-exp-1206')

    def create_name_prompt(self, answers: Dict[str, str]) -> str:
        return f"""You are a professional naming consultant. Based on the following preferences, generate creative and practical business name suggestions:

Business Basics:
- Industry type: {answers.get('industry', '')}
- Main products/services: {answers.get('products', '')}
- Target audience: {answers.get('audience', '')}
- Location: {answers.get('location', '')}

Name Preferences:
- Preferred starting letter(s): {answers.get('starting_letters', '')}
- Maximum word length: {answers.get('max_length', '')}
- Include location in name: {answers.get('include_location', '')}
- Name style: {answers.get('name_style', '')}

Additional Requirements:
- Must include specific words: {answers.get('include_words', '')}
- Words to avoid: {answers.get('avoid_words', '')}
- Language preference: {answers.get('language', '')}
- Should rhyme: {answers.get('rhyme', '')}
"""

    def generate_names(self, user_answers: Dict[str, str]) -> Optional[Dict[str, str]]:
        try:
            prompt = self.create_name_prompt(user_answers)
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
            print(f"Error generating names: {str(e)}")
            return None

generator = None

@app.route('/namegenerate', methods=['POST'])
def generate_name():
    try:
        data = request.get_json()
        business_names = generator.generate_names(data)
        if business_names:
            return jsonify({'success': True, 'names': business_names})
        return jsonify({'success': False, 'error': 'Failed to generate names'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    generator = BusinessNameGenerator(api_key)
    app.run(debug=True, port = 5002)
