"""
Simple Evaluation Report Generator (No Unicode Issues)
Generates professional HTML reports with visualizations
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
from utils.report_generator import EvaluationReportGenerator


def create_sample_data(n_samples=30):
    """Create sample evaluation data"""
    print("\n" + "="*70)
    print("Creating Sample Evaluation Data")
    print("="*70 + "\n")

    np.random.seed(42)

    categories = [
        'visualization_purpose',
        'axis_interpretation',
        'trend_identification',
        'statistical_indicators',
        'research_conclusions'
    ]

    data = {
        'sample_id': range(1, n_samples + 1),
        'category': np.random.choice(categories, n_samples),
        'plot_path': [f'data/plots/plot_{i}.png' for i in range(1, n_samples + 1)],
        'question': [f'Sample question {i}' for i in range(1, n_samples + 1)],
        'ai_clarity': np.clip(np.random.normal(4.2, 0.6, n_samples), 1, 5).round(1),
        'ai_helpfulness': np.clip(np.random.normal(4.1, 0.7, n_samples), 1, 5).round(1),
        'ai_accuracy': np.clip(np.random.normal(4.0, 0.5, n_samples), 1, 5).round(1),
        'human_clarity': np.clip(np.random.normal(3.8, 0.8, n_samples), 1, 5).round(1),
        'human_helpfulness': np.clip(np.random.normal(3.7, 0.9, n_samples), 1, 5).round(1),
        'human_accuracy': np.clip(np.random.normal(3.6, 0.7, n_samples), 1, 5).round(1)
    }

    df = pd.DataFrame(data)

    # Save sample data
    output_dir = Path('reports/data')
    output_dir.mkdir(parents=True, exist_ok=True)
    data_path = output_dir / 'sample_evaluation_data.csv'
    df.to_csv(data_path, index=False)

    print(f"[OK] Created {len(df)} evaluation samples")
    print(f"[OK] Data saved to: {data_path}\n")

    return str(data_path)


def generate_report(data_path, title="DataPlotQA Evaluation Report"):
    """Generate HTML report with visualizations"""
    print("="*70)
    print("Generating Evaluation Report")
    print("="*70 + "\n")

    # Initialize generator
    print("Step 1: Initializing report generator...")
    generator = EvaluationReportGenerator(output_dir='reports')
    print("[OK] Generator initialized\n")

    # Generate complete report
    print("Step 2: Calculating statistics and creating visualizations...")
    results = generator.generate_complete_report(
        evaluation_data_path=data_path,
        title=title
    )
    print("[OK] Report generation complete\n")

    # Display results
    print("="*70)
    print("REPORT GENERATED SUCCESSFULLY")
    print("="*70 + "\n")

    print(f"[FILE] HTML Report: {results['html_report']}")
    print(f"[FILE] Statistics JSON: {results['statistics_json']}")
    print(f"[FILE] Visualizations: {len(results['plots'])} plots created\n")

    print("="*70)
    print("HOW TO VIEW THE REPORT")
    print("="*70 + "\n")

    report_path = Path(results['html_report']).absolute()
    print(f"Open this file in your browser:")
    print(f"  {report_path}\n")

    print("Or run one of these commands:")
    print(f"  start {report_path}  (Windows)")
    print(f"  open {report_path}   (Mac)")
    print(f"  xdg-open {report_path}  (Linux)\n")

    return results


def main():
    """Main function"""
    print("\n" + "="*70)
    print("DataPlotQA Evaluation Report Generator")
    print("="*70)

    # Check command line arguments
    if len(sys.argv) > 1:
        # User provided data file
        data_path = sys.argv[1]
        if not Path(data_path).exists():
            print(f"\n[ERROR] File not found: {data_path}")
            print("\nUsage:")
            print("  python generate_report.py [data_file.csv]")
            print("  python generate_report.py  (generates sample data)")
            return

        print(f"\n[OK] Using data file: {data_path}\n")
    else:
        # Generate sample data
        data_path = create_sample_data(n_samples=30)

    # Generate report
    generate_report(data_path)

    print("="*70)
    print("[SUCCESS] All done!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
