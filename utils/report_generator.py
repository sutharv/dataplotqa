"""
Advanced Evaluation Report Generator for DataPlotQA
Generates comprehensive evaluation reports with visualizations and statistical analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']


class EvaluationReportGenerator:
    """Generate comprehensive evaluation reports with visualizations"""

    def __init__(self, output_dir: str = "reports"):
        """
        Initialize report generator

        Args:
            output_dir: Directory to save reports and visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.plots_dir = self.output_dir / "plots"
        self.plots_dir.mkdir(exist_ok=True)

        self.data_dir = self.output_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

    def load_evaluation_data(self, data_path: str) -> pd.DataFrame:
        """Load evaluation data from CSV or JSON"""
        data_path = Path(data_path)

        if data_path.suffix == '.csv':
            return pd.read_csv(data_path)
        elif data_path.suffix == '.json':
            return pd.read_json(data_path)
        else:
            raise ValueError(f"Unsupported file format: {data_path.suffix}")

    def calculate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics

        Args:
            df: DataFrame with evaluation results

        Returns:
            Dictionary with statistical results
        """
        stats_dict = {
            'ai_metrics': {},
            'human_metrics': {},
            'comparative_metrics': {},
            'category_analysis': {},
            'timestamp': datetime.now().isoformat()
        }

        # Define metrics
        metrics = ['clarity', 'helpfulness', 'accuracy']

        # AI metrics
        for metric in metrics:
            ai_col = f'ai_{metric}'
            if ai_col in df.columns:
                stats_dict['ai_metrics'][metric] = {
                    'mean': float(df[ai_col].mean()),
                    'median': float(df[ai_col].median()),
                    'std': float(df[ai_col].std()),
                    'min': float(df[ai_col].min()),
                    'max': float(df[ai_col].max()),
                    'q25': float(df[ai_col].quantile(0.25)),
                    'q75': float(df[ai_col].quantile(0.75))
                }

        # Human metrics
        for metric in metrics:
            human_col = f'human_{metric}'
            if human_col in df.columns:
                stats_dict['human_metrics'][metric] = {
                    'mean': float(df[human_col].mean()),
                    'median': float(df[human_col].median()),
                    'std': float(df[human_col].std()),
                    'min': float(df[human_col].min()),
                    'max': float(df[human_col].max()),
                    'q25': float(df[human_col].quantile(0.25)),
                    'q75': float(df[human_col].quantile(0.75))
                }

        # Comparative analysis
        for metric in metrics:
            ai_col = f'ai_{metric}'
            human_col = f'human_{metric}'

            if ai_col in df.columns and human_col in df.columns:
                # Paired t-test
                t_stat, p_value = stats.ttest_rel(df[ai_col], df[human_col])

                # Effect size (Cohen's d)
                diff = df[ai_col] - df[human_col]
                cohen_d = diff.mean() / diff.std()

                # Win rate (how often AI >= Human)
                win_rate = (df[ai_col] >= df[human_col]).mean()

                stats_dict['comparative_metrics'][metric] = {
                    't_statistic': float(t_stat),
                    'p_value': float(p_value),
                    'significant': bool(p_value < 0.05),
                    'cohen_d': float(cohen_d),
                    'effect_size': self._interpret_cohen_d(cohen_d),
                    'win_rate': float(win_rate),
                    'ai_better': bool(df[ai_col].mean() > df[human_col].mean())
                }

        # Category-level analysis
        if 'category' in df.columns:
            for category in df['category'].unique():
                category_df = df[df['category'] == category]
                stats_dict['category_analysis'][category] = {
                    'n_samples': len(category_df),
                    'ai_mean': {},
                    'human_mean': {}
                }

                for metric in metrics:
                    ai_col = f'ai_{metric}'
                    human_col = f'human_{metric}'

                    if ai_col in category_df.columns:
                        stats_dict['category_analysis'][category]['ai_mean'][metric] = float(
                            category_df[ai_col].mean()
                        )

                    if human_col in category_df.columns:
                        stats_dict['category_analysis'][category]['human_mean'][metric] = float(
                            category_df[human_col].mean()
                        )

        return stats_dict

    def _interpret_cohen_d(self, d: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"

    def create_visualizations(self, df: pd.DataFrame) -> List[str]:
        """
        Create all evaluation visualizations

        Args:
            df: DataFrame with evaluation results

        Returns:
            List of paths to saved plots
        """
        plot_paths = []

        # 1. Overall comparison bar chart
        plot_paths.append(self._create_comparison_bar_chart(df))

        # 2. Box plots for each metric
        plot_paths.append(self._create_box_plots(df))

        # 3. Category breakdown
        if 'category' in df.columns:
            plot_paths.append(self._create_category_heatmap(df))

        # 4. Distribution plots
        plot_paths.append(self._create_distribution_plots(df))

        # 5. Scatter comparison
        plot_paths.append(self._create_scatter_comparison(df))

        # 6. Radar chart
        plot_paths.append(self._create_radar_chart(df))

        return plot_paths

    def _create_comparison_bar_chart(self, df: pd.DataFrame) -> str:
        """Create bar chart comparing AI vs Human performance"""
        fig, ax = plt.subplots(figsize=(10, 6))

        metrics = []
        ai_scores = []
        human_scores = []

        for metric in ['clarity', 'helpfulness', 'accuracy']:
            ai_col = f'ai_{metric}'
            human_col = f'human_{metric}'

            if ai_col in df.columns and human_col in df.columns:
                metrics.append(metric.capitalize())
                ai_scores.append(df[ai_col].mean())
                human_scores.append(df[human_col].mean())

        x = np.arange(len(metrics))
        width = 0.35

        bars1 = ax.bar(x - width/2, ai_scores, width, label='AI (DataPlotQA)',
                       color='#667eea', alpha=0.8)
        bars2 = ax.bar(x + width/2, human_scores, width, label='Human TA',
                       color='#f093fb', alpha=0.8)

        ax.set_xlabel('Metric', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Score (1-5)', fontsize=12, fontweight='bold')
        ax.set_title('AI vs Human Teaching Assistant Performance',
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend(frameon=True, shadow=True)
        ax.set_ylim(0, 5.5)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        output_path = self.plots_dir / "comparison_bar_chart.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def _create_box_plots(self, df: pd.DataFrame) -> str:
        """Create box plots for score distributions"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        metrics = ['clarity', 'helpfulness', 'accuracy']

        for idx, metric in enumerate(metrics):
            ai_col = f'ai_{metric}'
            human_col = f'human_{metric}'

            if ai_col in df.columns and human_col in df.columns:
                data = pd.DataFrame({
                    'AI': df[ai_col],
                    'Human': df[human_col]
                })

                bp = axes[idx].boxplot([data['AI'], data['Human']],
                                      labels=['AI', 'Human'],
                                      patch_artist=True,
                                      widths=0.6)

                # Color the boxes
                colors = ['#667eea', '#f093fb']
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)

                axes[idx].set_title(metric.capitalize(), fontsize=12, fontweight='bold')
                axes[idx].set_ylabel('Score (1-5)', fontsize=10)
                axes[idx].grid(axis='y', alpha=0.3)
                axes[idx].set_ylim(0, 5.5)

        plt.suptitle('Score Distributions by Metric', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()

        output_path = self.plots_dir / "box_plots.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def _create_category_heatmap(self, df: pd.DataFrame) -> str:
        """Create heatmap showing performance by category"""
        categories = df['category'].unique()
        metrics = ['clarity', 'helpfulness', 'accuracy']

        # Prepare data for heatmap
        ai_data = []
        human_data = []

        for category in categories:
            category_df = df[df['category'] == category]

            ai_row = []
            human_row = []

            for metric in metrics:
                ai_col = f'ai_{metric}'
                human_col = f'human_{metric}'

                if ai_col in category_df.columns:
                    ai_row.append(category_df[ai_col].mean())
                if human_col in category_df.columns:
                    human_row.append(category_df[human_col].mean())

            ai_data.append(ai_row)
            human_data.append(human_row)

        # Create figure with two heatmaps
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # AI heatmap
        sns.heatmap(ai_data, annot=True, fmt='.2f', cmap='Blues',
                    xticklabels=[m.capitalize() for m in metrics],
                    yticklabels=categories, ax=ax1, vmin=1, vmax=5,
                    cbar_kws={'label': 'Score (1-5)'})
        ax1.set_title('AI (DataPlotQA) Performance by Category',
                     fontsize=12, fontweight='bold', pad=15)

        # Human heatmap
        sns.heatmap(human_data, annot=True, fmt='.2f', cmap='Purples',
                    xticklabels=[m.capitalize() for m in metrics],
                    yticklabels=categories, ax=ax2, vmin=1, vmax=5,
                    cbar_kws={'label': 'Score (1-5)'})
        ax2.set_title('Human TA Performance by Category',
                     fontsize=12, fontweight='bold', pad=15)

        plt.tight_layout()

        output_path = self.plots_dir / "category_heatmap.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def _create_distribution_plots(self, df: pd.DataFrame) -> str:
        """Create distribution plots with KDE"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        metrics = ['clarity', 'helpfulness', 'accuracy']

        for idx, metric in enumerate(metrics):
            ai_col = f'ai_{metric}'
            human_col = f'human_{metric}'

            if ai_col in df.columns and human_col in df.columns:
                # Plot histograms with KDE
                axes[idx].hist(df[ai_col], bins=5, alpha=0.5, label='AI',
                              color='#667eea', density=True, edgecolor='black')
                axes[idx].hist(df[human_col], bins=5, alpha=0.5, label='Human',
                              color='#f093fb', density=True, edgecolor='black')

                axes[idx].set_xlabel('Score', fontsize=10)
                axes[idx].set_ylabel('Density', fontsize=10)
                axes[idx].set_title(metric.capitalize(), fontsize=12, fontweight='bold')
                axes[idx].legend(frameon=True)
                axes[idx].grid(alpha=0.3)

        plt.suptitle('Score Distributions', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()

        output_path = self.plots_dir / "distributions.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def _create_scatter_comparison(self, df: pd.DataFrame) -> str:
        """Create scatter plots comparing AI vs Human scores"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        metrics = ['clarity', 'helpfulness', 'accuracy']

        for idx, metric in enumerate(metrics):
            ai_col = f'ai_{metric}'
            human_col = f'human_{metric}'

            if ai_col in df.columns and human_col in df.columns:
                # Check if human data has variance (not all zeros)
                human_has_variance = df[human_col].std() > 0.01
                ai_has_variance = df[ai_col].std() > 0.01

                if human_has_variance and ai_has_variance:
                    # Scatter plot
                    axes[idx].scatter(df[human_col], df[ai_col],
                                     alpha=0.6, s=80, color='#667eea', edgecolors='black')

                    # Add diagonal line (perfect agreement)
                    axes[idx].plot([1, 5], [1, 5], 'r--', alpha=0.5, linewidth=2,
                                  label='Perfect Agreement')

                    # Add regression line (only if both have variance)
                    try:
                        z = np.polyfit(df[human_col], df[ai_col], 1)
                        p = np.poly1d(z)
                        axes[idx].plot(df[human_col].sort_values(),
                                      p(df[human_col].sort_values()),
                                      "g-", alpha=0.5, linewidth=2, label='Regression')
                    except (np.linalg.LinAlgError, ValueError):
                        pass  # Skip regression line if it fails

                    axes[idx].set_xlim(0.5, 5.5)
                    axes[idx].set_ylim(0.5, 5.5)
                    axes[idx].legend(frameon=True, fontsize=8)
                else:
                    # Show bar chart instead when human data is all zeros
                    if ai_has_variance:
                        # Show AI scores only
                        ai_mean = df[ai_col].mean()
                        axes[idx].bar(['AI'], [ai_mean], color='#667eea', alpha=0.7)
                        axes[idx].set_ylim(0, 5.5)
                        axes[idx].axhline(y=ai_mean, color='red', linestyle='--', alpha=0.5)
                        axes[idx].text(0, ai_mean + 0.2, f'{ai_mean:.2f}', ha='center', fontsize=10)
                    else:
                        axes[idx].text(0.5, 0.5, 'No ratings yet',
                                      ha='center', va='center', transform=axes[idx].transAxes,
                                      fontsize=12, color='gray')

                axes[idx].set_xlabel('Human Score', fontsize=10)
                axes[idx].set_ylabel('AI Score', fontsize=10)
                axes[idx].set_title(metric.capitalize(), fontsize=12, fontweight='bold')
                axes[idx].grid(alpha=0.3)

        plt.suptitle('AI vs Human Score Comparison', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()

        output_path = self.plots_dir / "scatter_comparison.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def _create_radar_chart(self, df: pd.DataFrame) -> str:
        """Create radar chart comparing overall performance"""
        metrics = ['clarity', 'helpfulness', 'accuracy']

        ai_scores = []
        human_scores = []

        for metric in metrics:
            ai_col = f'ai_{metric}'
            human_col = f'human_{metric}'

            if ai_col in df.columns:
                ai_scores.append(df[ai_col].mean())
            if human_col in df.columns:
                human_scores.append(df[human_col].mean())

        # Create radar chart
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False)
        ai_scores_plot = ai_scores + [ai_scores[0]]
        human_scores_plot = human_scores + [human_scores[0]]
        angles_plot = np.concatenate((angles, [angles[0]]))

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

        ax.plot(angles_plot, ai_scores_plot, 'o-', linewidth=2,
                label='AI (DataPlotQA)', color='#667eea')
        ax.fill(angles_plot, ai_scores_plot, alpha=0.25, color='#667eea')

        ax.plot(angles_plot, human_scores_plot, 'o-', linewidth=2,
                label='Human TA', color='#f093fb')
        ax.fill(angles_plot, human_scores_plot, alpha=0.25, color='#f093fb')

        ax.set_xticks(angles)
        ax.set_xticklabels([m.capitalize() for m in metrics], fontsize=12)
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'])
        ax.grid(True)

        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=True, fontsize=11)
        plt.title('Overall Performance Comparison', fontsize=14,
                 fontweight='bold', pad=20)

        output_path = self.plots_dir / "radar_chart.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return str(output_path)

    def generate_html_report(
        self,
        df: pd.DataFrame,
        stats: Dict[str, Any],
        plot_paths: List[str],
        title: str = "DataPlotQA Evaluation Report"
    ) -> str:
        """
        Generate comprehensive HTML report

        Args:
            df: Evaluation DataFrame
            stats: Statistical results
            plot_paths: List of plot file paths
            title: Report title

        Returns:
            Path to generated HTML report
        """

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 40px;
            text-align: center;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .section {{
            margin: 40px 0;
        }}

        h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}

        h3 {{
            color: #764ba2;
            margin: 25px 0 15px 0;
            font-size: 1.4em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .stat-card h4 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }}

        .metric-row:last-child {{
            border-bottom: none;
        }}

        .metric-label {{
            font-weight: 600;
            color: #555;
        }}

        .metric-value {{
            color: #667eea;
            font-weight: bold;
        }}

        .plot-container {{
            margin: 30px 0;
            text-align: center;
        }}

        .plot-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}

        .highlight {{
            background: #fffbea;
            border-left: 4px solid #f093fb;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}

        .highlight strong {{
            color: #f093fb;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}

        tr:hover {{
            background: #f5f5f5;
        }}

        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            color: #888;
            font-size: 0.9em;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 0 5px;
        }}

        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}

        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}

        .badge-info {{
            background: #d1ecf1;
            color: #0c5460;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 {title}</h1>
            <p class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
        </header>

        <div class="section">
            <h2>Executive Summary</h2>
            <div class="highlight">
                <p><strong>Dataset:</strong> {len(df)} evaluation samples</p>
                <p><strong>Metrics Evaluated:</strong> Clarity, Helpfulness, Accuracy</p>
                <p><strong>Comparison:</strong> AI (DataPlotQA) vs Human Teaching Assistants</p>
            </div>
        </div>
"""

        # Add AI Statistics
        if 'ai_metrics' in stats and stats['ai_metrics']:
            html_content += """
        <div class="section">
            <h2>AI (DataPlotQA) Performance</h2>
            <div class="stats-grid">
"""
            for metric, values in stats['ai_metrics'].items():
                html_content += f"""
                <div class="stat-card">
                    <h4>{metric.capitalize()}</h4>
                    <div class="metric-row">
                        <span class="metric-label">Mean:</span>
                        <span class="metric-value">{values['mean']:.3f}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Median:</span>
                        <span class="metric-value">{values['median']:.3f}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Std Dev:</span>
                        <span class="metric-value">{values['std']:.3f}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Range:</span>
                        <span class="metric-value">{values['min']:.1f} - {values['max']:.1f}</span>
                    </div>
                </div>
"""
            html_content += """
            </div>
        </div>
"""

        # Add Human Statistics
        if 'human_metrics' in stats and stats['human_metrics']:
            html_content += """
        <div class="section">
            <h2>Human Teaching Assistant Performance</h2>
            <div class="stats-grid">
"""
            for metric, values in stats['human_metrics'].items():
                html_content += f"""
                <div class="stat-card">
                    <h4>{metric.capitalize()}</h4>
                    <div class="metric-row">
                        <span class="metric-label">Mean:</span>
                        <span class="metric-value">{values['mean']:.3f}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Median:</span>
                        <span class="metric-value">{values['median']:.3f}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Std Dev:</span>
                        <span class="metric-value">{values['std']:.3f}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Range:</span>
                        <span class="metric-value">{values['min']:.1f} - {values['max']:.1f}</span>
                    </div>
                </div>
"""
            html_content += """
            </div>
        </div>
"""

        # Add comparative analysis
        if 'comparative_metrics' in stats and stats['comparative_metrics']:
            html_content += """
        <div class="section">
            <h2>Statistical Comparison</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>p-value</th>
                        <th>Significant?</th>
                        <th>Effect Size</th>
                        <th>AI Win Rate</th>
                        <th>Winner</th>
                    </tr>
                </thead>
                <tbody>
"""
            for metric, values in stats['comparative_metrics'].items():
                significant = "Yes ✓" if values['significant'] else "No ✗"
                sig_badge = "badge-success" if values['significant'] else "badge-warning"
                winner = "AI" if values['ai_better'] else "Human"

                html_content += f"""
                    <tr>
                        <td><strong>{metric.capitalize()}</strong></td>
                        <td>{values['p_value']:.4f}</td>
                        <td><span class="badge {sig_badge}">{significant}</span></td>
                        <td>{values['effect_size'].capitalize()} ({values['cohen_d']:.2f})</td>
                        <td>{values['win_rate']*100:.1f}%</td>
                        <td><span class="badge badge-info">{winner}</span></td>
                    </tr>
"""
            html_content += """
                </tbody>
            </table>
        </div>
"""

        # Add visualizations
        html_content += """
        <div class="section">
            <h2>Visualizations</h2>
"""
        for plot_path in plot_paths:
            plot_name = Path(plot_path).stem.replace('_', ' ').title()
            html_content += f"""
            <div class="plot-container">
                <h3>{plot_name}</h3>
                <img src="plots/{Path(plot_path).name}" alt="{plot_name}">
            </div>
"""
        html_content += """
        </div>
"""

        # Add footer
        html_content += f"""
        <div class="footer">
            <p>DataPlotQA Evaluation Report | Generated by EvaluationReportGenerator</p>
            <p>© {datetime.now().year} DataPlotQA Project</p>
        </div>
    </div>
</body>
</html>
"""

        # Save HTML report
        output_path = self.output_dir / f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(output_path)

    def save_statistics_json(self, stats: Dict[str, Any]) -> str:
        """Save statistics to JSON file"""
        output_path = self.data_dir / f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        return str(output_path)

    def generate_complete_report(
        self,
        evaluation_data_path: str,
        title: str = "DataPlotQA Evaluation Report"
    ) -> Dict[str, str]:
        """
        Generate complete evaluation report with all components

        Args:
            evaluation_data_path: Path to evaluation data CSV/JSON
            title: Report title

        Returns:
            Dictionary with paths to all generated files
        """
        print("🔍 Loading evaluation data...")
        df = self.load_evaluation_data(evaluation_data_path)

        print("📊 Calculating statistics...")
        stats = self.calculate_statistics(df)

        print("📈 Creating visualizations...")
        plot_paths = self.create_visualizations(df)

        print("💾 Saving statistics...")
        stats_path = self.save_statistics_json(stats)

        print("📄 Generating HTML report...")
        html_path = self.generate_html_report(df, stats, plot_paths, title)

        print(f"\n✅ Report generation complete!")
        print(f"📂 Output directory: {self.output_dir}")

        return {
            'html_report': html_path,
            'statistics_json': stats_path,
            'plots': plot_paths,
            'output_dir': str(self.output_dir)
        }
