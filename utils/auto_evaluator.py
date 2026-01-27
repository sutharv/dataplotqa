"""
Automatic Evaluation Data Collector
Automatically extracts and updates evaluation data whenever users interact with the app
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from .database import Database


class AutoEvaluator:
    """
    Automatically collects and updates evaluation data from user interactions
    """

    def __init__(self, output_dir: str = "reports/data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.db = Database()

        # Category classification keywords
        self.category_keywords = {
            'visualization_purpose': ['purpose', 'goal', 'why', 'show', 'main'],
            'axis_interpretation': ['axis', 'axes', 'scale', 'label', 'unit', 'x-axis', 'y-axis'],
            'trend_identification': ['trend', 'pattern', 'increase', 'decrease', 'change', 'growth'],
            'statistical_indicators': ['error', 'confidence', 'significance', 'p-value', 'statistical'],
            'research_conclusions': ['conclusion', 'finding', 'result', 'implication', 'suggest']
        }

    def categorize_question(self, question: str) -> str:
        """Categorize question based on keywords"""
        question_lower = question.lower()
        for category, keywords in self.category_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        return 'general'

    def extract_current_data(self) -> pd.DataFrame:
        """
        Extract all current interactions from database with ratings

        Returns:
            DataFrame with all interactions and metadata
        """
        # Get all plots
        plots = self.db.get_plot_history(limit=10000)

        if not plots:
            return pd.DataFrame()

        # Collect all interactions
        all_data = []

        for plot in plots:
            plot_id = plot['id']
            interactions = self.db.get_interactions_for_plot(plot_id)

            for interaction in interactions:
                category = self.categorize_question(interaction['question'])
                interaction_id = interaction['id']

                # Get ratings from feedback table
                self.db.cursor.execute("""
                    SELECT clarity_rating, helpfulness_rating, accuracy_rating
                    FROM feedback
                    WHERE interaction_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 1
                """, (interaction_id,))

                rating_result = self.db.cursor.fetchone()

                if rating_result:
                    ai_clarity = float(rating_result[0]) if rating_result[0] else 0.0
                    ai_helpfulness = float(rating_result[1]) if rating_result[1] else 0.0
                    ai_accuracy = float(rating_result[2]) if rating_result[2] else 0.0
                else:
                    ai_clarity = 0.0
                    ai_helpfulness = 0.0
                    ai_accuracy = 0.0

                all_data.append({
                    'interaction_id': interaction_id,
                    'plot_id': plot_id,
                    'plot_path': plot['image_path'],
                    'category': category,
                    'question': interaction['question'],
                    'ai_response': interaction['response'],
                    'timestamp': interaction['timestamp'],
                    'plot_type': plot.get('plot_type', 'unknown'),
                    'domain': plot.get('domain', 'unknown'),
                    # User ratings (from feedback table)
                    'ai_clarity': ai_clarity,
                    'ai_helpfulness': ai_helpfulness,
                    'ai_accuracy': ai_accuracy,
                    # Placeholder for human TA ratings (need to be added manually)
                    'human_clarity': 0.0,
                    'human_helpfulness': 0.0,
                    'human_accuracy': 0.0
                })

        return pd.DataFrame(all_data)

    def update_evaluation_template(self) -> str:
        """
        Update the evaluation template with latest interactions

        Returns:
            Path to updated template file
        """
        df = self.extract_current_data()

        if df.empty:
            return None

        # Save template
        template_path = self.output_dir / 'rating_template.csv'
        df.to_csv(template_path, index=False)

        return str(template_path)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get current statistics about collected data

        Returns:
            Dictionary with statistics
        """
        df = self.extract_current_data()

        if df.empty:
            return {
                'total_interactions': 0,
                'total_plots': 0,
                'categories': {},
                'last_updated': None
            }

        return {
            'total_interactions': len(df),
            'total_plots': df['plot_id'].nunique(),
            'categories': df['category'].value_counts().to_dict(),
            'last_updated': datetime.now().isoformat(),
            'plot_types': df['plot_type'].value_counts().to_dict(),
            'domains': df['domain'].value_counts().to_dict()
        }

    def auto_update(self) -> Dict[str, Any]:
        """
        Automatically update evaluation data

        Returns:
            Dictionary with update results
        """
        # Extract current data
        df = self.extract_current_data()

        if df.empty:
            return {
                'success': False,
                'message': 'No interactions found in database',
                'stats': None
            }

        # Update template
        template_path = self.update_evaluation_template()

        # Get statistics
        stats = self.get_statistics()

        # Save statistics
        stats_file = self.output_dir / 'auto_eval_stats.json'
        import json
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

        return {
            'success': True,
            'message': f'Updated evaluation data: {stats["total_interactions"]} interactions from {stats["total_plots"]} plots',
            'template_path': template_path,
            'stats_path': str(stats_file),
            'stats': stats
        }


def update_evaluation_data():
    """
    Convenience function to update evaluation data
    Can be called from anywhere in the app
    """
    evaluator = AutoEvaluator()
    return evaluator.auto_update()


def get_current_stats():
    """
    Get current evaluation statistics
    """
    evaluator = AutoEvaluator()
    return evaluator.get_statistics()
