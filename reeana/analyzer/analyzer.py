#ResumeAnalyzer
# Get secrets from environment variables
from google import genai
import json
from typing import Dict, Any
from reeana.api import config
import os
import logging

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """Handles all resume analysis logic using Google Gemini"""
    
    def __init__(self, api_key: str):
        """Initialize the analyzer with API credentials"""
                     
        # Initialize the model
        self.model_name = config.settings.model_name
        self.model = genai.Client(api_key=api_key)

    def _build_analysis_prompt(self, resume_text: str, job_role: str) -> str:
        """Build prompt with anti-hallucination measures"""
        return f"""
        You are an expert resume reviewer specializing in {job_role} roles.

        Analyze this resume and Follow these rules STRICTLY:

        1. Only reference information EXPLICITLY stated in the resume and job role
        2. If something is not in the resume, do NOT invent it
        3. If you're unsure, say "Not enough information" rather than guessing
        4. When citing skills or achievements, they must appear verbatim in the resume
        5. Also compare and constrast if the skills and other content of the resume fits the inputed job role {job_role}
        then provide feedback about the resume in relationship to the stated Job role that is if the resume
        fits the role or not 
        as valid JSON with this EXACT structure:
        {{
            "overall_score": <number between 1-10>,
            "strengths": ["strength1", "strength2", "strength3"],
            "weaknesses": [
                {{"issue": "specific problem", "fix": "specific solution"}},
                {{"issue": "specific problem", "fix": "specific solution"}}
            ],
            "keyword_gaps": ["missing skill 1 requrired for role", "missing skill 2 requrired for role"],
            "top_priority": "single most impactful change to make"
        }}

        Rules:
        - Be specific about both the skills, resume and job role, not generic
        - Reference actual content from the resume in relationship to the defined Job role
        - Provide actionable advice
        - Focus on impact and results
        - Return ONLY the JSON object, no additional text

        Resume:
        {resume_text}
        """
    
           
    def analyze(self, resume_text: str, job_role: str = "general") -> Dict[str, Any]:
        """
        Analyze resume and return structured feedback.
        
        Args:
            resume_text: Extracted text from resume
            job_role: Target role for optimization
        
        Returns:
            Dictionary with structured feedback
        """
        
        # Build prompt
        prompt = self._build_analysis_prompt(resume_text, job_role)
        
        try:
            # Call Gemini API
            response = self.model.models.generate_content(
                contents = prompt,
                model = self.model_name
            )
            
            # Extract text
            response_text = response.text
            
            print(f"🔍 RAW RESPONSE FROM GEMINI:\n{response_text}\n")
            print(f"🔍 RESPONSE TYPE: {type(response_text)}")
            # Parse and validate
            feedback = self._parse_and_validate(response_text)
            logger.info(f"Analysis successful | Score: {feedback['overall_score']}")
            return feedback
            
        except Exception as e:
            logger.info(f"Failed to analyze resume: {str(e)}")
            raise ValueError(f"Failed to analyze resume: {str(e)}")

        except Exception as e:
            error_message = str(e)
            
            # Check for high demand / rate limit errors
            if "503" in error_message or "high demand" in error_message.lower():
                logger.warning("Gemini API experiencing high demand")
                raise ValueError(
                    "Our AI service is experiencing high demand right now. "
                    "This usually resolves in a few seconds."
                    "Please try again shortly."
                )
            # Check for rate limit
            elif "429" in error_message or "rate limit" in error_message.lower():
                logger.warning("Rate limit exceeded")
                raise ValueError(
                    "Too many requests. Please wait a moment and try again."
                )
    
    def _parse_and_validate(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate LLM's response"""
        
        try:
            # Since we used response_mime_type="application/json",
            # Gemini should return clean JSON
            feedback = json.loads(response_text)
            
            # Basic validation
            required_fields = ['overall_score', 'strengths', 'weaknesses', 
                             'keyword_gaps', 'top_priority']
            
            for field in required_fields:
                if field not in feedback:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate types
            if not isinstance(feedback['overall_score'], (int, float)):
                raise ValueError("overall_score must be a number")
            
            if not isinstance(feedback['strengths'], list):
                raise ValueError("strengths must be a list")
            
            if not isinstance(feedback['weaknesses'], list):
                raise ValueError("weaknesses must be a list")
            
            # Validate score range
            if not (1 <= feedback['overall_score'] <= 10):
                raise ValueError("overall_score must be between 1 and 10")
            
            return feedback
            
        except json.JSONDecodeError as e:
            # Fallback: try to extract JSON from markdown
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            else:
                raise ValueError(f"Failed to parse JSON response: {e}")
