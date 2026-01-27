"""
Vision Processor Module
Handles OCR, element detection, and visual analysis of plots
"""

import os
import json
from typing import Dict, List, Any
import base64
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system environment variables

class VisionProcessor:
    """Process scientific plots using GPT-4o Vision"""
    
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found!\n\n"
                "Please set your API key:\n"
                "  Windows CMD: set ANTHROPIC_API_KEY=your-key-here\n"
                "  Windows PowerShell: $env:ANTHROPIC_API_KEY='your-key-here'\n"
                "  Mac/Linux: export ANTHROPIC_API_KEY=your-key-here\n\n"
                "Or create a .env file with:\n"
                "  ANTHROPIC_API_KEY=your-key-here\n\n"
                "Get your key at: https://console.anthropic.com/"
            )
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_plot(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a scientific plot and extract structured information
        
        Args:
            image_path: Path to the plot image
            
        Returns:
            Dictionary containing plot analysis
        """
        
        # Encode image
        base64_image = self.encode_image(image_path)
        
        # Determine media type
        file_ext = Path(image_path).suffix.lower()
        media_type = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.pdf': 'application/pdf'
        }.get(file_ext, 'image/png')
        
        # Create analysis prompt
        analysis_prompt = """You are an expert at analyzing scientific data visualizations from academic papers.

Analyze this plot and provide a structured JSON response with the following information:

{
  "plot_type": "type of plot (bar chart, line graph, scatter plot, etc.)",
  "title": "plot title if present",
  "axes": {
    "x_axis": {
      "label": "x-axis label",
      "scale": "linear/logarithmic/other",
      "range": "min to max values",
      "units": "units if specified"
    },
    "y_axis": {
      "label": "y-axis label",
      "scale": "linear/logarithmic/other",
      "range": "min to max values",
      "units": "units if specified"
    }
  },
  "data_series": [
    {
      "name": "series name/legend label",
      "type": "line/bar/scatter/etc",
      "color": "approximate color",
      "description": "brief description of the series"
    }
  ],
  "statistical_elements": [
    {
      "type": "error bars/confidence interval/shaded region/etc",
      "description": "what it represents"
    }
  ],
  "text_items": [
    "any annotations, labels, or text on the plot"
  ],
  "key_features": [
    "notable trends, patterns, outliers, or important characteristics"
  ],
  "domain": "likely scientific domain (biology, physics, psychology, CS, etc.)"
}

Be precise about numeric values and scale types. If something is unclear or not present, indicate that explicitly.

RESPOND ONLY WITH VALID JSON. DO NOT include any other text, markdown formatting, or explanations outside the JSON structure."""

        try:
            # Call Claude API
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_image,
                                }
                            },
                            {
                                "type": "text",
                                "text": analysis_prompt
                            }
                        ]
                    }
                ]
            )
            
            # Extract JSON from response
            response_text = message.content[0].text
            
            # Clean up response (remove markdown code blocks if present)
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            analysis = json.loads(response_text)
            
            # Add metadata
            analysis['image_path'] = image_path
            analysis['raw_response'] = message.content[0].text
            
            return analysis
            
        except Exception as e:
            print(f"Error in plot analysis: {e}")
            # Return basic fallback analysis
            return {
                'plot_type': 'unknown',
                'title': 'Unable to extract',
                'axes': {},
                'data_series': [],
                'statistical_elements': [],
                'text_items': [],
                'key_features': [],
                'domain': 'unknown',
                'error': str(e),
                'image_path': image_path
            }
    
    def extract_numeric_values(self, image_path: str, query: str) -> Dict[str, Any]:
        """
        Extract specific numeric values from a plot
        
        Args:
            image_path: Path to the plot image
            query: Specific question about numeric values
            
        Returns:
            Dictionary with extracted values
        """
        
        base64_image = self.encode_image(image_path)
        
        file_ext = Path(image_path).suffix.lower()
        media_type = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg'
        }.get(file_ext, 'image/png')
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_image,
                                }
                            },
                            {
                                "type": "text",
                                "text": f"Extract the following numeric information from this plot: {query}\n\nProvide precise values with units if available."
                            }
                        ]
                    }
                ]
            )
            
            return {
                'query': query,
                'response': message.content[0].text
            }
            
        except Exception as e:
            return {
                'query': query,
                'response': f"Error extracting values: {str(e)}"
            }
