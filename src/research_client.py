"""Research client using Google's Gemini API with search capability."""
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from .config import settings

class ResearchClient:
    """Client for researching topics using Gemini with grounded search."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini client.
        
        Args:
            api_key: Optional API key. If not provided, loads from environment.
        """
        self.api_key = api_key or settings.google_api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 1,
            'top_k': 1,
            'max_output_tokens': 2048
        }

    def research_with_search(self, query: str) -> Dict:
        """Research a topic with search capability.
        
        Args:
            query: The topic to research.
            
        Returns:
            Dict containing research results and citations.
        """
        prompt = f"""Research the following topic using search results: {query}
        
        Please provide:
        1. A comprehensive analysis
        2. Key findings and insights
        3. Citations for all sources used
        
        Format the response as a JSON with the following structure:
        {{
            "analysis": "detailed analysis here",
            "key_findings": ["finding1", "finding2", ...],
            "citations": ["citation1", "citation2", ...]
        }}
        """
        
        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config=self.generation_config
            )
            
            if not response.text:
                return {
                    "error": "No response generated",
                    "details": "The model did not return any content"
                }
            
            # Clean up the response text
            text = response.text.strip()
            
            # Remove code block markers if present
            if text.startswith("```") and text.endswith("```"):
                # Extract the content between the backticks
                lines = text.split("\n")
                if len(lines) > 2:  # At least 3 lines (opening ```, content, closing ```)
                    # Remove first and last lines (backticks)
                    text = "\n".join(lines[1:-1])
                    # If the first line is a language identifier (e.g., ```json), remove it
                    if text.startswith("json") or text.startswith("JSON"):
                        text = "\n".join(text.split("\n")[1:])
            
            try:
                return json.loads(text.strip())
            except json.JSONDecodeError:
                return {
                    "error": "Invalid JSON response",
                    "details": text
                }
                
        except Exception as e:
            return {
                "error": "Research failed",
                "details": str(e)
            }

    def research_without_search(self, query: str) -> Dict:
        """Research a topic without search capability.
        
        Args:
            query: The topic to research.
            
        Returns:
            Dict containing research results.
        """
        prompt = f"""Research the following topic using your knowledge: {query}
        
        Please provide:
        1. A comprehensive analysis
        2. Key findings and insights
        
        Format the response as a JSON with the following structure:
        {{
            "analysis": "detailed analysis here",
            "key_findings": ["finding1", "finding2", ...]
        }}
        """
        
        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config=self.generation_config
            )
            
            if not response.text:
                return {
                    "error": "No response generated",
                    "details": "The model did not return any content"
                }
            
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return {
                    "error": "Invalid JSON response",
                    "details": response.text
                }
                
        except Exception as e:
            return {
                "error": "Research failed",
                "details": str(e)
            }

    def generate_thread(self, research_data: Dict) -> List[str]:
        """Generate a Twitter thread from research data.
        
        Args:
            research_data: Research results from research_with_search()
            
        Returns:
            List of tweet texts forming a thread
        """
        prompt = """Convert this research into an engaging Twitter thread.
        Each tweet should be under 280 characters and flow naturally.
        Make it informative yet conversational.
        Include relevant hashtags where appropriate.
        Return ONLY a JSON array of tweet texts, nothing else.
        
        Research data:
        {research_json}
        """.format(research_json=json.dumps(research_data))
        
        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config=self.generation_config
            )
            
            if not response.text:
                raise ResearchError("No response generated")
            
            # Clean up the response text
            text = response.text.strip()
            
            # Remove code block markers if present
            if text.startswith("```") and text.endswith("```"):
                # Extract the content between the backticks
                lines = text.split("\n")
                if len(lines) > 2:  # At least 3 lines (opening ```, content, closing ```)
                    # Remove first and last lines (backticks)
                    text = "\n".join(lines[1:-1])
                    # If the first line is a language identifier (e.g., ```json), remove it
                    if text.startswith("json") or text.startswith("JSON"):
                        text = "\n".join(text.split("\n")[1:])
            
            try:
                tweets = json.loads(text.strip())
                if isinstance(tweets, list) and tweets:
                    return tweets
                raise ResearchError("Invalid tweet list format")
            except json.JSONDecodeError:
                raise ResearchError(f"Failed to parse tweets: {text}")
                
        except Exception as e:
            raise ResearchError(f"Failed to generate thread: {str(e)}")

class ResearchError(Exception):
    """Custom exception for research operations."""
    pass 