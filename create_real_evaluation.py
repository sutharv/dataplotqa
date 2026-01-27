"""
Create Evaluation Report from Real DataPlotQA Data
Extracts actual interactions from the database and generates evaluation report
"""

import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
from pathlib import Path
from utils.database import Database
from utils.report_generator import EvaluationReportGenerator


def extract_real_data_from_database():
    """
    Extract real interaction data from DataPlotQA database
    """
    print("\n" + "="*70)
    print("Extracting Real Data from Database")
    print("="*70 + "\n")

    # Initialize database
    db = Database()
    print("[OK] Database initialized\n")

    # Get all interactions from database
    print("Step 1: Loading interactions from database...")

    try:
        # Get plot history first
        plots = db.get_plot_history(limit=1000)  # Get all plots

        if not plots or len(plots) == 0:
            print("\n[WARNING] No plots found in database!")
            print("You need to use the DataPlotQA app first to generate interactions.\n")
            print("How to generate data:")
            print("1. Run: streamlit run app/main.py")
            print("2. Upload some plots")
            print("3. Ask questions and get AI responses")
            print("4. Come back and run this script again\n")
            return None

        print(f"[OK] Found {len(plots)} plots\n")

        # Get all interactions for all plots
        all_interactions = []
        interaction_count = 0

        for plot in plots:
            plot_id = plot['id']
            interactions = db.get_interactions_for_plot(plot_id)

            for interaction in interactions:
                interaction_count += 1
                all_interactions.append({
                    'id': interaction['id'],
                    'plot_id': plot_id,
                    'image_path': plot['image_path'],
                    'question': interaction['question'],
                    'response': interaction['response'],
                    'timestamp': interaction['timestamp'],
                    'plot_type': plot.get('plot_type', 'unknown'),
                    'domain': plot.get('domain', 'unknown')
                })

        if interaction_count == 0:
            print("\n[WARNING] No interactions found!")
            print("Please use the app to ask questions about your plots.\n")
            return None

        print(f"[OK] Found {interaction_count} interactions across {len(plots)} plots\n")

        return all_interactions

    except Exception as e:
        print(f"[ERROR] Database query failed: {str(e)}")
        print(f"[DEBUG] Error details: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you have used the DataPlotQA app to create some interactions first.\n")
        return None


def create_evaluation_data_from_interactions(interactions):
    """
    Convert database interactions into evaluation format

    Note: Since we don't have human responses yet, this creates a template
    where you need to manually add human ratings
    """
    print("Step 2: Converting to evaluation format...")

    # Map question types to categories
    category_keywords = {
        'visualization_purpose': ['purpose', 'goal', 'why', 'show'],
        'axis_interpretation': ['axis', 'axes', 'scale', 'label', 'unit'],
        'trend_identification': ['trend', 'pattern', 'increase', 'decrease', 'change'],
        'statistical_indicators': ['error', 'confidence', 'significance', 'p-value', 'statistical'],
        'research_conclusions': ['conclusion', 'finding', 'result', 'implication', 'suggest']
    }

    def categorize_question(question):
        """Categorize question based on keywords"""
        question_lower = question.lower()
        for category, keywords in category_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        return 'general'

    eval_data = []

    for interaction in interactions:
        # Categorize the question
        category = categorize_question(interaction['question'])

        # Create evaluation entry
        # Note: AI ratings would need to be collected from human raters
        # For now, we'll create a template with placeholder values
        eval_data.append({
            'interaction_id': interaction['id'],
            'plot_path': interaction['image_path'],
            'question': interaction['question'],
            'ai_response': interaction['response'],
            'created_at': interaction['timestamp'],
            'plot_type': interaction['plot_type'],
            'domain': interaction['domain'],
            'category': category,
            # Placeholder ratings - NEED TO BE FILLED BY HUMAN RATERS
            'ai_clarity': 0.0,
            'ai_helpfulness': 0.0,
            'ai_accuracy': 0.0,
            'human_clarity': 0.0,
            'human_helpfulness': 0.0,
            'human_accuracy': 0.0
        })

    df = pd.DataFrame(eval_data)
    print(f"[OK] Converted {len(df)} interactions\n")

    return df


def save_template_for_rating(df, output_path):
    """
    Save a template CSV that human raters can fill in
    """
    print("Step 3: Creating rating template...")

    # Select columns for rating template
    rating_template = df[[
        'interaction_id',
        'plot_path',
        'category',
        'question',
        'ai_response',
        'ai_clarity',
        'ai_helpfulness',
        'ai_accuracy',
        'human_clarity',
        'human_helpfulness',
        'human_accuracy'
    ]].copy()

    # Save template
    template_path = Path(output_path)
    template_path.parent.mkdir(parents=True, exist_ok=True)
    rating_template.to_csv(template_path, index=False)

    print(f"[OK] Template saved to: {template_path}\n")

    return template_path


def generate_demo_report_from_real_data(df):
    """
    Generate a demo report with simulated ratings based on real interactions
    """
    print("Step 4: Generating demo report with simulated ratings...")
    print("[NOTE] Using simulated ratings for demonstration\n")

    # Simulate ratings for demonstration
    np.random.seed(42)
    n = len(df)

    df['ai_clarity'] = np.clip(np.random.normal(4.2, 0.6, n), 1, 5).round(1)
    df['ai_helpfulness'] = np.clip(np.random.normal(4.1, 0.7, n), 1, 5).round(1)
    df['ai_accuracy'] = np.clip(np.random.normal(4.0, 0.5, n), 1, 5).round(1)
    df['human_clarity'] = np.clip(np.random.normal(3.8, 0.8, n), 1, 5).round(1)
    df['human_helpfulness'] = np.clip(np.random.normal(3.7, 0.9, n), 1, 5).round(1)
    df['human_accuracy'] = np.clip(np.random.normal(3.6, 0.7, n), 1, 5).round(1)

    # Save the data
    data_path = Path('reports/data/real_interactions_demo.csv')
    data_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_path, index=False)

    print(f"[OK] Data saved to: {data_path}\n")

    # Generate report
    print("Step 5: Generating HTML report...")
    generator = EvaluationReportGenerator(output_dir='reports/real_data')

    results = generator.generate_complete_report(
        evaluation_data_path=str(data_path),
        title=f"DataPlotQA Evaluation - Real Interactions (n={len(df)})"
    )

    print("[OK] Report generated\n")

    return results


def main():
    """Main function"""
    print("\n" + "="*70)
    print("DataPlotQA Real Data Evaluation Report Generator")
    print("="*70)

    # Extract real data from database
    interactions = extract_real_data_from_database()

    if interactions is None:
        print("="*70)
        print("[INFO] Setup Instructions")
        print("="*70)
        print("\nTo generate evaluation reports from real data:")
        print("\n1. First, use your DataPlotQA app:")
        print("   streamlit run app/main.py")
        print("\n2. Upload some plots and ask questions")
        print("\n3. After you have interactions, run this script again:")
        print("   python create_real_evaluation.py")
        print("\n" + "="*70 + "\n")
        return

    # Convert to evaluation format
    df = create_evaluation_data_from_interactions(interactions)

    # Save template for human raters
    template_path = save_template_for_rating(
        df,
        'reports/data/rating_template.csv'
    )

    print("="*70)
    print("RATING TEMPLATE CREATED")
    print("="*70)
    print(f"\nTemplate file: {template_path.absolute()}")
    print("\nNext steps to get REAL evaluation:")
    print("1. Open the template CSV file")
    print("2. Have human raters read each AI response")
    print("3. Rate each response on 1-5 scale for:")
    print("   - Clarity (how clear is it?)")
    print("   - Helpfulness (how helpful for learning?)")
    print("   - Accuracy (is information correct?)")
    print("4. Get human TA responses and rate them too")
    print("5. Fill in the rating columns")
    print("6. Save the file")
    print("7. Run: python generate_report.py [your_filled_template.csv]")
    print("\n" + "="*70 + "\n")

    # Generate demo report with simulated ratings
    print("="*70)
    print("DEMO REPORT (with simulated ratings)")
    print("="*70 + "\n")

    results = generate_demo_report_from_real_data(df)

    print("="*70)
    print("DEMO REPORT GENERATED")
    print("="*70)
    print(f"\n[FILE] HTML Report: {results['html_report']}")
    print(f"[FILE] Statistics: {results['statistics_json']}")
    print(f"[FILE] Plots: {len(results['plots'])} visualizations")
    print("\n[NOTE] This demo report uses:")
    print("  - Real questions from your database")
    print("  - Real AI responses from your system")
    print("  - SIMULATED ratings (not real human ratings)")
    print("\nFor a REAL evaluation, follow the steps above!")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
