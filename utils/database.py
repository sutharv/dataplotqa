"""
Database Module
Handles storage of plot analyses, questions, and responses
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class Database:
    """SQLite database for storing DataPlotQA interactions"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection and create tables"""
        # If no path provided, use project's data folder (cross-platform)
        if db_path is None:
            # Get the directory where this file is located
            current_dir = Path(__file__).parent.parent
            db_path = current_dir / "data" / "dataplotqa.db"
        
        self.db_path = str(db_path)
        
        # Create data directory if it doesn't exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        
        # Plots table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS plots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                plot_type TEXT,
                domain TEXT,
                analysis_json TEXT,
                upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Interactions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plot_id INTEGER,
                question TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plot_id) REFERENCES plots (id)
            )
        """)
        
        # Feedback table for evaluation
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_id INTEGER,
                clarity_rating INTEGER CHECK(clarity_rating BETWEEN 1 AND 5),
                helpfulness_rating INTEGER CHECK(helpfulness_rating BETWEEN 1 AND 5),
                accuracy_rating INTEGER CHECK(accuracy_rating BETWEEN 1 AND 5),
                comments TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (interaction_id) REFERENCES interactions (id)
            )
        """)
        
        # Evaluation dataset table (for comparing with human TAs)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_dataset (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plot_path TEXT NOT NULL,
                question TEXT NOT NULL,
                ai_response TEXT,
                human_response TEXT,
                question_category TEXT,
                created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def save_plot(self, image_path: str, analysis: Dict[str, Any]) -> int:
        """
        Save plot analysis to database
        
        Args:
            image_path: Path to the plot image
            analysis: Structured analysis from VisionProcessor
            
        Returns:
            Plot ID
        """
        self.cursor.execute("""
            INSERT INTO plots (image_path, plot_type, domain, analysis_json)
            VALUES (?, ?, ?, ?)
        """, (
            image_path,
            analysis.get('plot_type', 'unknown'),
            analysis.get('domain', 'unknown'),
            json.dumps(analysis)
        ))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def save_interaction(
        self,
        image_path: str,
        question: str,
        response: str,
        plot_analysis: Dict[str, Any]
    ) -> int:
        """
        Save a question-response interaction
        
        Args:
            image_path: Path to the plot image
            question: Student's question
            response: AI's response
            plot_analysis: Plot analysis dict
            
        Returns:
            Interaction ID
        """
        # Check if plot exists, if not create it
        self.cursor.execute(
            "SELECT id FROM plots WHERE image_path = ?",
            (image_path,)
        )
        result = self.cursor.fetchone()
        
        if result:
            plot_id = result[0]
        else:
            plot_id = self.save_plot(image_path, plot_analysis)
        
        # Save interaction
        self.cursor.execute("""
            INSERT INTO interactions (plot_id, question, response)
            VALUES (?, ?, ?)
        """, (plot_id, question, response))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def save_feedback(
        self,
        interaction_id: Optional[int] = None,
        image_path: Optional[str] = None,
        question: Optional[str] = None,
        response: Optional[str] = None,
        rating: Optional[Dict[str, int]] = None,
        clarity: Optional[int] = None,
        helpfulness: Optional[int] = None,
        accuracy: Optional[int] = None,
        comments: Optional[str] = None
    ):
        """
        Save user feedback for an interaction

        Args:
            interaction_id: ID of the interaction (if known)
            image_path: Path to image (if interaction_id not known)
            question: Question text (if interaction_id not known)
            response: Response text (if interaction_id not known)
            rating: Dictionary with clarity, helpfulness, accuracy (alternative to separate params)
            clarity: Clarity rating (1-5)
            helpfulness: Helpfulness rating (1-5)
            accuracy: Accuracy rating (1-5)
            comments: Optional text comments
        """
        # Handle rating dict
        if rating:
            clarity = rating.get('clarity', clarity)
            helpfulness = rating.get('helpfulness', helpfulness)
            accuracy = rating.get('accuracy', accuracy)

        # If interaction_id not provided, find it
        if not interaction_id and image_path and question:
            self.cursor.execute("""
                SELECT id FROM interactions
                WHERE image_path = ? AND question = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (image_path, question))
            result = self.cursor.fetchone()
            if result:
                interaction_id = result[0]
            else:
                # No matching interaction found, cannot save feedback
                return

        if interaction_id:
            self.cursor.execute("""
                INSERT INTO feedback (
                    interaction_id, clarity_rating, helpfulness_rating,
                    accuracy_rating, comments
                )
                VALUES (?, ?, ?, ?, ?)
            """, (interaction_id, clarity, helpfulness, accuracy, comments))

            self.conn.commit()
    
    def get_plot_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent plot analysis history
        
        Args:
            limit: Number of recent plots to retrieve
            
        Returns:
            List of plot dictionaries
        """
        self.cursor.execute("""
            SELECT id, image_path, plot_type, domain, upload_timestamp
            FROM plots
            ORDER BY upload_timestamp DESC
            LIMIT ?
        """, (limit,))
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                'id': row[0],
                'image_path': row[1],
                'plot_type': row[2],
                'domain': row[3],
                'timestamp': row[4]
            })
        
        return results
    
    def get_interactions_for_plot(self, plot_id: int) -> List[Dict[str, Any]]:
        """
        Get all interactions for a specific plot
        
        Args:
            plot_id: Plot ID
            
        Returns:
            List of interaction dictionaries
        """
        self.cursor.execute("""
            SELECT id, question, response, timestamp
            FROM interactions
            WHERE plot_id = ?
            ORDER BY timestamp ASC
        """, (plot_id,))
        
        results = []
        for row in self.cursor.fetchall():
            results.append({
                'id': row[0],
                'question': row[1],
                'response': row[2],
                'timestamp': row[3]
            })
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dictionary with statistics
        """
        stats = {}
        
        # Total plots
        self.cursor.execute("SELECT COUNT(*) FROM plots")
        stats['total_plots'] = self.cursor.fetchone()[0]
        
        # Total interactions
        self.cursor.execute("SELECT COUNT(*) FROM interactions")
        stats['total_interactions'] = self.cursor.fetchone()[0]
        
        # Average feedback ratings
        self.cursor.execute("""
            SELECT 
                AVG(clarity_rating) as avg_clarity,
                AVG(helpfulness_rating) as avg_helpfulness,
                AVG(accuracy_rating) as avg_accuracy
            FROM feedback
        """)
        row = self.cursor.fetchone()
        stats['avg_clarity'] = round(row[0], 2) if row[0] else None
        stats['avg_helpfulness'] = round(row[1], 2) if row[1] else None
        stats['avg_accuracy'] = round(row[2], 2) if row[2] else None
        
        # Plots by domain
        self.cursor.execute("""
            SELECT domain, COUNT(*) as count
            FROM plots
            GROUP BY domain
            ORDER BY count DESC
        """)
        stats['plots_by_domain'] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        return stats
    
    def add_evaluation_entry(
        self,
        plot_path: str,
        question: str,
        ai_response: str,
        human_response: str,
        category: str
    ) -> int:
        """
        Add an entry to the evaluation dataset
        
        Args:
            plot_path: Path to plot image
            question: Question asked
            ai_response: AI-generated response
            human_response: Human TA response
            category: Question category
            
        Returns:
            Entry ID
        """
        self.cursor.execute("""
            INSERT INTO evaluation_dataset (
                plot_path, question, ai_response, human_response, question_category
            )
            VALUES (?, ?, ?, ?, ?)
        """, (plot_path, question, ai_response, human_response, category))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def close(self):
        """Close database connection"""
        self.conn.close()