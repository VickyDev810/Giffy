
import google.generativeai as genai
import os
import json
from typing import Dict, Any, Optional

class GeminiService:
    _configured = False

    @classmethod
    def configure(cls):
        if cls._configured:
            return
            
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found")
            return
        genai.configure(api_key=api_key)
        cls._configured = True

    @classmethod
    async def analyze_profile(cls, profile_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze Instagram profile data using Gemini to generate persona and gift ideas
        """
        cls.configure()
        try:
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            # Extract relevant text data
            captions = [p.get('caption') for p in profile_data.get('recent_posts', []) if p.get('caption')]
            
            prompt = f"""
            You are an expert gift consultant. Analyze this Instagram profile data to create a detailed gift persona.
            
            Profile Context:
            Username: {profile_data.get('username')}
            Full Name: {profile_data.get('full_name')}
            Bio: {profile_data.get('bio')}
            Recent Post Captions: {json.dumps(captions[:10])}
            
            Based on this, generate a JSON response with the following structure:
            {{
                "vibe_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
                "interests": ["interest 1", "interest 2", "interest 3", "interest 4", "interest 5"],
                "gift_ideas": ["Specific Gift 1", "Specific Gift 2", "Specific Gift 3", "Specific Gift 4", "Specific Gift 5"],
                "summary": "A concise 2-sentence summary of their personality and style."
            }}
            
            The 'vibe_tags' should be single words like 'chaotic', 'minimalist', 'foodie', 'techie', 'artistic', etc.
            The 'gift_ideas' should be creative and specific, not generic.
            
            Return ONLY the valid JSON object. Do not include markdown formatting.
            """
            
            response = await model.generate_content_async(prompt)
            text = response.text.strip()
            
            # Clean up markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            return json.loads(text.strip())
            
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            return None
