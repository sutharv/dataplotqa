# DataPlotQA: A Multimodal Agent for Interpreting Academic Visualizations

An AI-powered teaching assistant that helps students understand scientific data visualizations through interactive dialogue and pedagogical explanations.

## 📋 Overview

DataPlotQA addresses a critical gap in STEM education: helping students interpret complex academic plots. The system combines:
- **Vision AI** (Claude Sonnet 4) for plot analysis and OCR
- **Pedagogical Explanations** structured for student learning
- **Interactive Dialogue** allowing follow-up questions
- **Multi-domain Support** across Biology, Physics, Psychology, and Computer Science

## 🎯 Key Features

### 1. Visual Analysis
- Automatic plot type detection (bar charts, line graphs, scatter plots, etc.)
- OCR for axis labels, legends, and annotations
- Statistical element identification (error bars, confidence intervals)
- Trend and pattern recognition

### 2. Pedagogical Explanations
- Structured teaching approach (Context → Components → Patterns → Statistics → Interpretation)
- Clear, accessible language for undergraduate students
- Progressive complexity building
- Analogies and examples when helpful

### 3. Interactive Learning
- Natural language question answering
- Contextual follow-up questions
- Quick question templates for common queries
- Conversation history tracking

### 4. Evaluation Framework
- Comparison with human teaching assistant responses
- Likert scale ratings (Clarity, Helpfulness, Accuracy)
- Statistical analysis (paired t-tests, Wilcoxon tests)
- Inter-rater reliability metrics

## 🏗️ Architecture

```
DataPlotQA/
├── app/
│   └── main.py                 # Streamlit interface
├── utils/
│   ├── vision_processor.py     # Claude Vision integration
│   ├── explanation_generator.py # Pedagogical response generation
│   ├── database.py             # SQLite storage
│   └── evaluator.py            # Evaluation metrics
├── data/
│   └── dataplotqa.db           # SQLite database
└── requirements.txt
```

## 🚀 Installation

### Prerequisites
- Python 3.9+
- Anthropic API key

### Setup

1. **Clone or navigate to the project directory**
```bash
cd /home/claude/dataplotqa
```

2. **Install dependencies**
```bash
pip install -r requirements.txt --break-system-packages
```

3. **Set up environment variables**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

4. **Run the application**
```bash
streamlit run app/main.py
```

## 💻 Usage

### Basic Workflow

1. **Upload a Plot**
   - Use the sidebar to upload a scientific visualization (PNG, JPG, PDF)
   - Click "Analyze Plot" to process the image

2. **Review Initial Analysis**
   - DataPlotQA provides an overview of the plot
   - View detected plot type, axes, and key features

3. **Ask Questions**
   - Use quick question templates or type custom questions
   - Engage in dialogue to deepen understanding
   - Ask follow-up questions based on previous responses

4. **Provide Feedback** (optional)
   - Rate responses for clarity, helpfulness, and accuracy
   - Help improve the system through feedback

### Example Questions

**Visualization Purpose:**
- "What is the main purpose of this visualization?"
- "What research question does this plot address?"

**Axis Interpretation:**
- "Explain how to interpret the axes and scales"
- "What do the axis labels and units tell us?"

**Trend Identification:**
- "What are the main trends visible in this data?"
- "How would you characterize the patterns shown?"

**Statistical Indicators:**
- "What do the error bars indicate?"
- "How should we interpret the uncertainty shown?"

**Research Conclusions:**
- "What conclusions can be drawn from this visualization?"
- "Based on this plot, what did the researchers likely find?"

## 🔬 Evaluation Methodology

DataPlotQA implements a rigorous evaluation framework comparing AI responses with human teaching assistants:

### Dataset Construction
- 50 diverse academic plots from multiple scientific domains
- 5 standardized questions per plot (one per category)
- Domain expert validation

### Evaluation Metrics
- **Clarity** (1-5): Comprehensibility and coherence
- **Helpfulness** (1-5): Utility for understanding
- **Accuracy** (1-5): Factual correctness (expert-rated)

### Statistical Analysis
- Paired t-tests for normally distributed data
- Wilcoxon signed-rank tests for non-parametric comparisons
- Inter-rater reliability analysis
- Qualitative thematic analysis

### Running Evaluations

```python
from utils.evaluator import Evaluator
from utils.database import Database

# Initialize
db = Database()
evaluator = Evaluator(db)

# Create evaluation dataset
plot_paths = ['path/to/plot1.png', 'path/to/plot2.png', ...]
eval_df = evaluator.create_evaluation_dataset(plot_paths)

# Collect responses and ratings
# (This would be done via the UI in practice)

# Analyze results
results = evaluator.analyze_results(eval_df)

# Generate report
report = evaluator.generate_evaluation_report(results, 'evaluation_report.txt')
print(report)
```

## 📊 Database Schema

### Tables

**plots**
- `id`: Primary key
- `image_path`: Path to uploaded image
- `plot_type`: Detected plot type
- `domain`: Scientific domain
- `analysis_json`: Full analysis results
- `upload_timestamp`: When uploaded

**interactions**
- `id`: Primary key
- `plot_id`: Foreign key to plots
- `question`: Student question
- `response`: AI response
- `timestamp`: When asked

**feedback**
- `id`: Primary key
- `interaction_id`: Foreign key to interactions
- `clarity_rating`: 1-5 scale
- `helpfulness_rating`: 1-5 scale
- `accuracy_rating`: 1-5 scale
- `comments`: Optional text feedback
- `timestamp`: When provided

**evaluation_dataset**
- `id`: Primary key
- `plot_path`: Path to plot
- `question`: Evaluation question
- `ai_response`: DataPlotQA response
- `human_response`: Human TA response
- `question_category`: Category of question

## 🎓 Pedagogical Approach

DataPlotQA follows established principles from intelligent tutoring systems research:

### Core Principles
1. **Clarity First**: Use simple, accessible language
2. **Structured Teaching**: Break down complexity progressively
3. **Build Understanding**: Develop analytical skills, not just answer questions
4. **Precision**: Be accurate about scales, units, and statistical indicators
5. **Encourage Reasoning**: Help students think independently

### Explanation Framework
1. **Context**: What is being shown and why
2. **Components**: Axes, scales, units, visual elements
3. **Patterns**: Trends, relationships, observations
4. **Statistics**: Error bars, confidence intervals, significance
5. **Interpretation**: Conclusions and implications
6. **Connections**: Links to broader concepts

## 🔍 Technical Details

### Vision Processing
- Uses Claude Sonnet 4 for multimodal reasoning
- Structured JSON extraction for consistent analysis
- OCR for text elements
- Numeric value extraction

### Explanation Generation
- GPT-4 level language model for natural explanations
- Pedagogical system prompt engineering
- Context-aware responses using conversation history
- Temperature tuning for consistency

### Performance Optimization
- Image compression for faster processing
- Response caching for repeated questions
- Conversation history pruning (last 6 messages)
- Asynchronous database operations

## 🚧 Limitations and Future Work

### Current Limitations
- Numeric precision challenges with very small values
- Limited support for highly specialized domain visualizations
- No real-time collaboration features
- English language only

### Future Enhancements
1. **Multi-plot Reasoning**: Compare across multiple visualizations
2. **Domain Adaptation**: Fine-tuning for specific fields
3. **Learning Analytics**: Track student progress over time
4. **Integration**: LMS integration (Canvas, Moodle)
5. **Multilingual Support**: Explanations in multiple languages
6. **Accessibility**: Screen reader support, alternative formats

## 📚 Citation

If you use DataPlotQA in your research, please cite:

```
Suthar et al. (2025). DataPlotQA: A Multimodal Agent for Interpreting
and Explaining Data Visualizations from Academic Papers. 
Department of Computer Science, Vistula University.
```

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- Additional plot type support
- Improved pedagogical templates
- Evaluation dataset expansion
- Bug fixes and performance improvements

## 📧 Contact

For questions or feedback, please open an issue in the repository.

## 🙏 Acknowledgments

This project builds on research in:
- Multimodal large language models (GPT-4V, Claude)
- Chart understanding systems (PlotQA, ChartQA, UniChart)
- Intelligent tutoring systems
- Graph literacy research
- Explainable AI
