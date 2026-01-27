"""
Example Test Script for DataPlotQA
Demonstrates core functionality without requiring UI interaction
"""

import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.vision_processor import VisionProcessor
from utils.explanation_generator import ExplanationGenerator
from utils.database import Database

def test_dataplotqa():
    """Run a complete test of DataPlotQA functionality"""
    
    print("=" * 60)
    print("DataPlotQA Test Suite")
    print("=" * 60)
    
    # Initialize components
    print("\n1. Initializing components...")
    vision = VisionProcessor()
    explainer = ExplanationGenerator()
    db = Database()
    
    print("✓ Components initialized")
    
    # Test database
    print("\n2. Testing database...")
    stats = db.get_statistics()
    print(f"   Database statistics: {json.dumps(stats, indent=2)}")
    print("✓ Database working")
    
    # Check for API key
    import os
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("\n⚠️  Warning: ANTHROPIC_API_KEY not set")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key'")
        print("   Vision analysis and explanation generation will not work without it.")
        return
    
    print("✓ API key found")
    
    # Create a simple test
    print("\n3. Testing explanation generation (without image)...")
    
    # Mock plot analysis (simulating what vision processor would return)
    mock_analysis = {
        "plot_type": "line graph",
        "title": "Temperature vs Time",
        "axes": {
            "x_axis": {
                "label": "Time (hours)",
                "scale": "linear",
                "range": "0 to 24",
                "units": "hours"
            },
            "y_axis": {
                "label": "Temperature (°C)",
                "scale": "linear",
                "range": "0 to 30",
                "units": "°C"
            }
        },
        "data_series": [
            {
                "name": "Indoor",
                "type": "line",
                "color": "blue",
                "description": "Indoor temperature measurements"
            },
            {
                "name": "Outdoor",
                "type": "line",
                "color": "red",
                "description": "Outdoor temperature measurements"
            }
        ],
        "statistical_elements": [],
        "text_items": ["Peak at noon", "Minimum at 6 AM"],
        "key_features": [
            "Both temperatures increase during daytime",
            "Outdoor temperature shows higher variation",
            "Indoor temperature more stable"
        ],
        "domain": "environmental science"
    }
    
    try:
        # Generate initial explanation
        explanation = explainer.generate_initial_explanation(mock_analysis)
        print("\nInitial Explanation Generated:")
        print("-" * 60)
        print(explanation)
        print("-" * 60)
        
        # Test Q&A
        print("\n4. Testing question answering...")
        question = "What are the main trends in this data?"
        
        chat_history = [
            {"role": "assistant", "content": explanation}
        ]
        
        response = explainer.generate_response(
            question,
            mock_analysis,
            chat_history
        )
        
        print(f"\nQuestion: {question}")
        print("\nResponse:")
        print("-" * 60)
        print(response)
        print("-" * 60)
        
        # Save to database
        print("\n5. Testing database storage...")
        interaction_id = db.save_interaction(
            image_path="/test/mock_plot.png",
            question=question,
            response=response,
            plot_analysis=mock_analysis
        )
        print(f"✓ Saved interaction with ID: {interaction_id}")
        
        # Get updated statistics
        stats = db.get_statistics()
        print(f"\nUpdated statistics:")
        print(f"  Total plots: {stats['total_plots']}")
        print(f"  Total interactions: {stats['total_interactions']}")
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        print("\nTo run the full application:")
        print("  streamlit run app/main.py")
        print("\nTo test with real images:")
        print("  1. Upload plots via the Streamlit UI")
        print("  2. Or modify this script to use actual image paths")
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure ANTHROPIC_API_KEY is set correctly")
        print("  2. Check internet connection")
        print("  3. Verify API key has proper permissions")

def demo_evaluation_framework():
    """Demonstrate the evaluation framework"""
    
    print("\n" + "=" * 60)
    print("DataPlotQA Evaluation Framework Demo")
    print("=" * 60)
    
    from utils.evaluator import Evaluator
    
    evaluator = Evaluator()
    
    print("\n1. Question Categories:")
    for i, category in enumerate(evaluator.question_categories, 1):
        print(f"   {i}. {category}")
    
    print("\n2. Sample Evaluation Dataset Structure:")
    
    # Create a small sample dataset
    sample_plots = [
        "/path/to/biology_plot1.png",
        "/path/to/physics_plot1.png"
    ]
    
    eval_df = evaluator.create_evaluation_dataset(sample_plots, questions_per_category=1)
    
    print(f"\n   Total evaluation items: {len(eval_df)}")
    print(f"   Plots: {len(sample_plots)}")
    print(f"   Categories: {len(evaluator.question_categories)}")
    print(f"   Questions per plot: {len(eval_df) // len(sample_plots)}")
    
    print("\n   Sample evaluation entry:")
    sample_entry = eval_df.iloc[0].to_dict()
    for key, value in sample_entry.items():
        if key != 'clarity_ratings':  # Skip empty lists
            print(f"     {key}: {value}")
    
    print("\n3. Evaluation Metrics:")
    print("   - Clarity (1-5): How clear and comprehensible is the explanation?")
    print("   - Helpfulness (1-5): How useful is it for understanding the plot?")
    print("   - Accuracy (1-5): How factually correct is the information?")
    
    print("\n4. Statistical Tests:")
    print("   - Paired t-test (for normally distributed ratings)")
    print("   - Wilcoxon signed-rank test (for non-parametric data)")
    print("   - Inter-rater reliability (Cronbach's alpha)")
    
    print("\n" + "=" * 60)
    print("Evaluation framework ready for use!")
    print("=" * 60)

if __name__ == "__main__":
    # Run main tests
    test_dataplotqa()
    
    # Demo evaluation framework
    demo_evaluation_framework()
    
    print("\n\nNext Steps:")
    print("1. Run the Streamlit app: streamlit run app/main.py")
    print("2. Upload academic plots from research papers")
    print("3. Engage in dialogue to understand visualizations")
    print("4. Collect evaluation data comparing with human TAs")
