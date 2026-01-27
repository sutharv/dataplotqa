"""
Evaluation Module
Tools for evaluating DataPlotQA against human teaching assistants
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from scipy import stats
from pathlib import Path
import json

class Evaluator:
    """Evaluate DataPlotQA responses against human baselines"""
    
    def __init__(self, db=None):
        """Initialize evaluator"""
        self.db = db
        
        # Question categories for the evaluation
        self.question_categories = [
            'visualization_purpose',
            'axis_interpretation',
            'trend_identification',
            'statistical_indicators',
            'research_conclusions'
        ]
    
    def create_evaluation_dataset(
        self,
        plot_paths: List[str],
        questions_per_category: int = 1
    ) -> pd.DataFrame:
        """
        Create evaluation dataset structure
        
        Args:
            plot_paths: List of paths to academic plots
            questions_per_category: Number of questions per category per plot
            
        Returns:
            DataFrame with evaluation structure
        """
        
        # Standard questions for each category
        standard_questions = {
            'visualization_purpose': [
                "What is the main purpose of this visualization?",
                "What research question does this plot address?"
            ],
            'axis_interpretation': [
                "Explain how to interpret the axes and scales in this plot.",
                "What do the axis labels and units tell us?"
            ],
            'trend_identification': [
                "What are the main trends visible in this data?",
                "How would you characterize the patterns shown?"
            ],
            'statistical_indicators': [
                "What do the error bars (or confidence intervals) indicate?",
                "How should we interpret the uncertainty shown in this plot?"
            ],
            'research_conclusions': [
                "What conclusions can be drawn from this visualization?",
                "Based on this plot, what did the researchers likely find?"
            ]
        }
        
        # Create dataset
        records = []
        for plot_path in plot_paths:
            for category in self.question_categories:
                questions = standard_questions[category][:questions_per_category]
                for question in questions:
                    records.append({
                        'plot_path': plot_path,
                        'question': question,
                        'category': category,
                        'ai_response': None,
                        'human_response': None,
                        'clarity_ratings': [],
                        'helpfulness_ratings': [],
                        'accuracy_ratings': []
                    })
        
        return pd.DataFrame(records)
    
    def collect_ratings(
        self,
        response: str,
        response_type: str,
        question: str
    ) -> Dict[str, int]:
        """
        Collect Likert scale ratings for a response
        (In practice, this would be done via a user interface)
        
        Args:
            response: The response to rate
            response_type: 'ai' or 'human'
            question: The question that was asked
            
        Returns:
            Dictionary with ratings
        """
        print(f"\n{'='*60}")
        print(f"Rate this {response_type.upper()} response:")
        print(f"Question: {question}")
        print(f"\nResponse:\n{response}")
        print(f"\n{'='*60}")
        
        # In production, this would be replaced with UI elements
        clarity = int(input("Clarity (1-5): "))
        helpfulness = int(input("Helpfulness (1-5): "))
        accuracy = int(input("Accuracy (1-5): "))
        
        return {
            'clarity': clarity,
            'helpfulness': helpfulness,
            'accuracy': accuracy
        }
    
    def analyze_results(
        self,
        evaluation_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze evaluation results with statistical tests
        
        Args:
            evaluation_df: DataFrame with completed evaluations
            
        Returns:
            Dictionary with analysis results
        """
        
        results = {
            'summary_statistics': {},
            'hypothesis_tests': {},
            'category_breakdown': {}
        }
        
        # Extract ratings into arrays
        ai_clarity = []
        human_clarity = []
        ai_helpfulness = []
        human_helpfulness = []
        ai_accuracy = []
        human_accuracy = []
        
        for _, row in evaluation_df.iterrows():
            if row['clarity_ratings'] and len(row['clarity_ratings']) >= 2:
                ai_clarity.append(row['clarity_ratings'][0])  # AI rating
                human_clarity.append(row['clarity_ratings'][1])  # Human rating
            
            if row['helpfulness_ratings'] and len(row['helpfulness_ratings']) >= 2:
                ai_helpfulness.append(row['helpfulness_ratings'][0])
                human_helpfulness.append(row['helpfulness_ratings'][1])
            
            if row['accuracy_ratings'] and len(row['accuracy_ratings']) >= 2:
                ai_accuracy.append(row['accuracy_ratings'][0])
                human_accuracy.append(row['accuracy_ratings'][1])
        
        # Summary statistics
        if ai_clarity:
            results['summary_statistics']['ai'] = {
                'clarity_mean': np.mean(ai_clarity),
                'clarity_std': np.std(ai_clarity),
                'helpfulness_mean': np.mean(ai_helpfulness),
                'helpfulness_std': np.std(ai_helpfulness),
                'accuracy_mean': np.mean(ai_accuracy),
                'accuracy_std': np.std(ai_accuracy)
            }
        
        if human_clarity:
            results['summary_statistics']['human'] = {
                'clarity_mean': np.mean(human_clarity),
                'clarity_std': np.std(human_clarity),
                'helpfulness_mean': np.mean(human_helpfulness),
                'helpfulness_std': np.std(human_helpfulness),
                'accuracy_mean': np.mean(human_accuracy),
                'accuracy_std': np.std(human_accuracy)
            }
        
        # Paired statistical tests
        if len(ai_clarity) > 5:  # Need sufficient sample size
            # Check normality
            _, p_normal_ai = stats.shapiro(ai_clarity)
            _, p_normal_human = stats.shapiro(human_clarity)
            
            if p_normal_ai > 0.05 and p_normal_human > 0.05:
                # Use paired t-test for normally distributed data
                t_stat, p_val = stats.ttest_rel(ai_clarity, human_clarity)
                results['hypothesis_tests']['clarity'] = {
                    'test': 'paired_t_test',
                    't_statistic': t_stat,
                    'p_value': p_val,
                    'significant': p_val < 0.05
                }
            else:
                # Use Wilcoxon signed-rank test for non-normal data
                w_stat, p_val = stats.wilcoxon(ai_clarity, human_clarity)
                results['hypothesis_tests']['clarity'] = {
                    'test': 'wilcoxon_signed_rank',
                    'w_statistic': w_stat,
                    'p_value': p_val,
                    'significant': p_val < 0.05
                }
            
            # Similar tests for helpfulness and accuracy
            # (code abbreviated for brevity)
        
        # Category-level breakdown
        for category in self.question_categories:
            category_data = evaluation_df[evaluation_df['category'] == category]
            
            if len(category_data) > 0:
                results['category_breakdown'][category] = {
                    'n_questions': len(category_data),
                    # Add category-specific analysis here
                }
        
        return results
    
    def generate_evaluation_report(
        self,
        analysis_results: Dict[str, Any],
        output_path: str = None
    ) -> str:
        """
        Generate a formatted evaluation report
        
        Args:
            analysis_results: Results from analyze_results()
            output_path: Optional path to save report
            
        Returns:
            Report text
        """
        
        report_lines = [
            "DataPlotQA Evaluation Report",
            "=" * 60,
            "",
            "SUMMARY STATISTICS",
            "-" * 60
        ]
        
        # AI statistics
        if 'ai' in analysis_results['summary_statistics']:
            ai_stats = analysis_results['summary_statistics']['ai']
            report_lines.extend([
                "",
                "AI (DataPlotQA) Performance:",
                f"  Clarity:      {ai_stats['clarity_mean']:.2f} ± {ai_stats['clarity_std']:.2f}",
                f"  Helpfulness:  {ai_stats['helpfulness_mean']:.2f} ± {ai_stats['helpfulness_std']:.2f}",
                f"  Accuracy:     {ai_stats['accuracy_mean']:.2f} ± {ai_stats['accuracy_std']:.2f}"
            ])
        
        # Human statistics
        if 'human' in analysis_results['summary_statistics']:
            human_stats = analysis_results['summary_statistics']['human']
            report_lines.extend([
                "",
                "Human Teaching Assistant Performance:",
                f"  Clarity:      {human_stats['clarity_mean']:.2f} ± {human_stats['clarity_std']:.2f}",
                f"  Helpfulness:  {human_stats['helpfulness_mean']:.2f} ± {human_stats['helpfulness_std']:.2f}",
                f"  Accuracy:     {human_stats['accuracy_mean']:.2f} ± {human_stats['accuracy_std']:.2f}"
            ])
        
        # Hypothesis tests
        if analysis_results['hypothesis_tests']:
            report_lines.extend([
                "",
                "",
                "STATISTICAL COMPARISONS",
                "-" * 60
            ])
            
            for metric, test_result in analysis_results['hypothesis_tests'].items():
                report_lines.extend([
                    "",
                    f"{metric.upper()}:",
                    f"  Test: {test_result['test']}",
                    f"  p-value: {test_result['p_value']:.4f}",
                    f"  Significant difference: {'Yes' if test_result['significant'] else 'No'}"
                ])
        
        report_text = "\n".join(report_lines)
        
        # Save if output path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
        
        return report_text
    
    def calculate_inter_rater_reliability(
        self,
        ratings_matrix: np.ndarray
    ) -> Dict[str, float]:
        """
        Calculate inter-rater reliability metrics
        
        Args:
            ratings_matrix: Matrix where rows are items and columns are raters
            
        Returns:
            Dictionary with reliability metrics
        """
        
        # Fleiss' kappa for multiple raters
        # Implementation would go here
        
        # For now, return Cronbach's alpha as a simpler alternative
        if ratings_matrix.shape[0] < 2:
            return {'cronbach_alpha': None}
        
        item_variances = np.var(ratings_matrix, axis=1, ddof=1)
        total_variance = np.var(ratings_matrix.sum(axis=1), ddof=1)
        
        k = ratings_matrix.shape[1]  # number of raters
        alpha = (k / (k - 1)) * (1 - item_variances.sum() / total_variance)
        
        return {
            'cronbach_alpha': alpha,
            'interpretation': 'Good' if alpha > 0.7 else 'Fair' if alpha > 0.5 else 'Poor'
        }
