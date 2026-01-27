"""
Explanation Generator Module
Generates pedagogical explanations for scientific plots
"""

import os
from typing import Dict, List, Any
import json

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system environment variables

class ExplanationGenerator:
    """Generate structured, pedagogical explanations for plots"""
    
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
        
        # Pedagogical template
        self.system_prompt = """You are DataPlotQA, an expert teaching assistant specializing in scientific data visualization interpretation. Your role is to help students understand academic plots through clear, pedagogical explanations.

CORE PRINCIPLES:
1. **Clarity First**: Use simple, accessible language appropriate for undergraduate STEM students
2. **Structured Teaching**: Break down complex visualizations into digestible components
3. **Build Understanding**: Progress from basic elements to advanced interpretation
4. **Encourage Reasoning**: Help students develop analytical skills, not just answer questions
5. **Be Precise**: Provide accurate information about scales, units, and statistical indicators

EXPLANATION STRUCTURE:
When explaining plots, follow this pedagogical framework:
1. **Context**: What is being shown and why
2. **Components**: Axes, scales, units, and visual elements
3. **Patterns**: Trends, relationships, and key observations
4. **Statistics**: Error bars, confidence intervals, significance
5. **Interpretation**: What conclusions can be drawn
6. **Connections**: Link to broader scientific concepts when relevant

RESPONSE STYLE:
- Start with direct answers, then provide deeper explanation
- Use analogies and examples when helpful
- Acknowledge uncertainty when interpretation is ambiguous
- Encourage follow-up questions
- Avoid overwhelming students with unnecessary jargon
- When explaining error bars or confidence intervals, be especially clear about what they represent

Remember: You're not just answering questions - you're teaching students how to read and interpret scientific visualizations independently."""

    def generate_initial_explanation(self, plot_analysis: Dict[str, Any]) -> str:
        """
        Generate initial pedagogical explanation when a plot is uploaded
        
        Args:
            plot_analysis: Structured analysis from VisionProcessor
            
        Returns:
            Initial explanation string
        """
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Create context from analysis
            context = f"""I have analyzed a scientific plot. Here is the structured information:

{json.dumps(plot_analysis, indent=2)}

Please provide a welcoming, pedagogical introduction to this plot that covers:
1. A brief overview of what type of visualization this is
2. The main purpose/what it's trying to show
3. Key components students should pay attention to
4. An invitation to ask questions

Keep it concise (3-4 paragraphs) and encouraging."""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=800,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": context
                    }
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"""Welcome! I've analyzed your plot, which appears to be a {plot_analysis.get('plot_type', 'scientific visualization')}.

I'm here to help you understand this visualization through interactive dialogue. You can ask me about:
- The purpose and context of this plot
- How to read the axes and scales
- What trends or patterns are visible
- What statistical indicators (like error bars) mean
- What conclusions we can draw from the data

Feel free to ask any questions!

(Note: There was a technical issue with the detailed analysis: {str(e)})"""
    
    def generate_response(
        self,
        question: str,
        plot_analysis: Dict[str, Any],
        chat_history: List[Dict[str, str]]
    ) -> str:
        """
        Generate a pedagogical response to a student question
        
        Args:
            question: Student's question
            plot_analysis: Structured plot analysis
            chat_history: Previous conversation messages
            
        Returns:
            Response string
        """
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Build conversation context
            messages = []
            
            # Add plot analysis as initial context
            messages.append({
                "role": "user",
                "content": f"""Here is the plot analysis I'm working with:

{json.dumps(plot_analysis, indent=2)}

I'll be asking questions about this plot."""
            })
            
            messages.append({
                "role": "assistant",
                "content": "I understand. I have the plot analysis and I'm ready to answer your questions about this visualization in a clear, pedagogical way."
            })
            
            # Add relevant chat history (last 6 messages to stay within context)
            recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
            for msg in recent_history:
                if msg['role'] in ['user', 'assistant']:
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            # Add current question
            messages.append({
                "role": "user",
                "content": question
            })
            
            # Generate response
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1200,
                system=self.system_prompt,
                messages=messages
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"""I apologize, but I encountered an error generating a response: {str(e)}

Based on the plot analysis, I can tell you that this is a {plot_analysis.get('plot_type', 'visualization')} showing {plot_analysis.get('title', 'data')}.

Could you please try rephrasing your question?"""
    
    def generate_comparison_explanation(
        self,
        plot_analysis: Dict[str, Any],
        comparison_type: str
    ) -> str:
        """
        Generate explanations for specific comparison tasks
        
        Args:
            plot_analysis: Structured plot analysis
            comparison_type: Type of comparison (trends, groups, timepoints, etc.)
            
        Returns:
            Explanation string
        """
        
        comparison_prompts = {
            'trends': 'Explain how to compare trends across different data series in this plot.',
            'groups': 'Explain how to compare different groups shown in this visualization.',
            'timepoints': 'Explain how to compare values at different time points.',
            'statistical': 'Explain how to interpret and compare the statistical indicators (error bars, confidence intervals) in this plot.'
        }
        
        prompt = comparison_prompts.get(
            comparison_type,
            'Explain how to make meaningful comparisons in this plot.'
        )
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Plot analysis:
{json.dumps(plot_analysis, indent=2)}

{prompt}"""
                    }
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"Error generating comparison explanation: {str(e)}"
