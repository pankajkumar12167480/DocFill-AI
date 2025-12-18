"""
LLM Processor Module
Integrates with Groq API for fast, free LLM inference.
"""

import requests
import json
from typing import Dict, List, Optional


class LLMProcessor:
    """
    Handles LLM API calls for extracting field values from text.
    Uses Groq API (generous free tier - 14,400 requests/day).
    """
    
    # Groq API endpoint
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    # Available Groq models (all free)
    GROQ_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]
    
    def __init__(self, api_key: str, model: str = None):
        """
        Initialize the LLM processor.
        
        Args:
            api_key: Groq API key
            model: Model to use (defaults to llama-3.3-70b-versatile)
        """
        self.api_key = api_key
        self.model = model or self.GROQ_MODELS[0]
    
    def call_api(self, prompt: str, system_prompt: str = None) -> str:
        """
        Make an API call to Groq.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            LLM response text
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 8000
        }
        
        try:
            response = requests.post(
                self.GROQ_API_URL,
                headers=headers,
                json=data,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            try:
                error_detail = response.json()
                if "error" in error_detail:
                    error_msg = error_detail["error"].get("message", error_msg)
            except:
                pass
            raise Exception(f"API request failed: {error_msg}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {str(e)}")


def extract_field_values(
    template_text: str,
    report_text: str,
    api_key: str,
    model: str = None
) -> Dict[str, str]:
    """
    Use LLM to extract field values from report text based on template fields.
    
    Args:
        template_text: The template document text with field names
        report_text: Extracted text from photo reports
        api_key: Google Gemini API key
        model: Optional model override
        
    Returns:
        Dictionary mapping field names to extracted values
    """
    processor = LLMProcessor(api_key, model)
    
    system_prompt = """You are an expert insurance document processor. Your task is to:
1. Analyze the insurance template to identify all fields that need to be filled
2. Extract corresponding values from the photo report text
3. Return a JSON object mapping field names to their values

Rules:
- Be precise and extract exact values from the report
- If a value cannot be found, use "N/A"
- Format dates consistently as MM/DD/YYYY
- Format currency with $ symbol
- Keep field names exactly as they appear in the template
- Return ONLY valid JSON, no additional text"""

    prompt = f"""INSURANCE TEMPLATE:
{template_text}

PHOTO REPORT CONTENT:
{report_text}

Based on the template above, extract all relevant information from the photo report.
Identify each field in the template that needs to be filled and find its corresponding value.

Return a JSON object where:
- Keys are the field names/labels from the template
- Values are the extracted data from the report

Return ONLY the JSON object, nothing else."""

    try:
        response = processor.call_api(prompt, system_prompt)
        
        # Clean the response - extract JSON if wrapped in code blocks
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        # Parse JSON
        field_values = json.loads(response)
        return field_values
    
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse LLM response as JSON: {str(e)}\nResponse: {response[:500]}")
    except Exception as e:
        raise Exception(f"Field extraction failed: {str(e)}")


def get_available_models() -> List[str]:
    """
    Get list of available Groq models.
    
    Returns:
        List of model identifiers
    """
    return LLMProcessor.GROQ_MODELS.copy()


if __name__ == "__main__":
    # Test the module
    print("Available Groq models:", get_available_models())
