"""
Quick Script to Check Evaluation Data Accuracy
Run this anytime to see what data has been collected
"""

import sys
import io
import json
from pathlib import Path

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from utils.auto_evaluator import get_current_stats
import pandas as pd


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def check_data():
    """Check current evaluation data"""

    print_header("DataPlotQA Evaluation Data Status")

    # Get statistics
    try:
        stats = get_current_stats()
    except Exception as e:
        print(f"[ERROR] Could not load statistics: {e}")
        return

    # Overall Stats
    print("OVERALL STATISTICS")
    print("-" * 70)
    print(f"Total Interactions:  {stats['total_interactions']}")
    print(f"Total Plots:         {stats['total_plots']}")
    print(f"Last Updated:        {stats['last_updated']}")
    print()

    # Category Breakdown
    print("QUESTION CATEGORIES")
    print("-" * 70)
    categories = stats['categories']
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / stats['total_interactions'] * 100) if stats['total_interactions'] > 0 else 0
        print(f"{category:30s}  {count:3d}  ({percentage:5.1f}%)")
    print()

    # Plot Types
    print("PLOT TYPES")
    print("-" * 70)
    plot_types = stats['plot_types']
    for ptype, count in sorted(plot_types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / stats['total_interactions'] * 100) if stats['total_interactions'] > 0 else 0
        print(f"{ptype[:40]:40s}  {count:3d}  ({percentage:5.1f}%)")
    print()

    # Domains
    print("DOMAINS")
    print("-" * 70)
    domains = stats['domains']
    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / stats['total_interactions'] * 100) if stats['total_interactions'] > 0 else 0
        print(f"{domain[:40]:40s}  {count:3d}  ({percentage:5.1f}%)")
    print()

    # File Locations
    print_header("Data Files")

    template_file = Path('reports/data/rating_template.csv')
    stats_file = Path('reports/data/auto_eval_stats.json')

    print("EVALUATION FILES")
    print("-" * 70)

    if template_file.exists():
        # Count rows in template
        try:
            df = pd.read_csv(template_file)
            print(f"[OK] Rating Template:     {template_file}")
            print(f"     Rows: {len(df)} interactions")
            print(f"     Columns: {', '.join(df.columns.tolist()[:5])}...")
            print()
        except Exception as e:
            print(f"[WARNING] Could not read template: {e}")
    else:
        print(f"[NOT FOUND] Rating Template: {template_file}")
        print("            Run the app to generate it automatically")
        print()

    if stats_file.exists():
        print(f"[OK] Statistics JSON:     {stats_file}")
        print()
    else:
        print(f"[NOT FOUND] Statistics: {stats_file}")
        print()

    # Sample Data Preview
    if template_file.exists():
        print_header("Sample Data Preview (First 3 Interactions)")

        try:
            df = pd.read_csv(template_file)

            for idx in range(min(3, len(df))):
                row = df.iloc[idx]
                print(f"Interaction #{idx + 1}")
                print("-" * 70)
                print(f"Plot:      {row['plot_path']}")
                print(f"Category:  {row['category']}")
                print(f"Question:  {row['question'][:80]}...")
                print(f"Response:  {str(row['ai_response'])[:80]}...")
                print(f"Ratings:   AI ({row['ai_clarity']}, {row['ai_helpfulness']}, {row['ai_accuracy']}) "
                      f"Human ({row['human_clarity']}, {row['human_helpfulness']}, {row['human_accuracy']})")
                print()
        except Exception as e:
            print(f"[ERROR] Could not preview data: {e}")

    # Next Steps
    print_header("Next Steps")

    print("DATA COLLECTION STATUS: [OK] Active")
    print()
    print("To use this data for evaluation:")
    print()
    print("1. Open the rating template:")
    print(f"   start {template_file.absolute()}")
    print()
    print("2. Have human raters fill in the rating columns (0.0 -> actual scores)")
    print()
    print("3. Generate final report:")
    print(f"   python generate_report.py {template_file}")
    print()
    print("Or generate a demo report with current data:")
    print("   python create_real_evaluation.py")
    print()

    print("="*70)


if __name__ == "__main__":
    check_data()
