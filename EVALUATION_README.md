# DataPlotQA Evaluation System

## Overview

Your DataPlotQA app **automatically collects evaluation data** every time users interact with it. This data is used to compare AI performance against human teaching assistants.

---

## How It Works

### Automatic Collection (No Manual Work)

Every time a user:
1. Uploads a plot
2. Asks a question
3. Gets an AI response

The system automatically:
- ✅ Saves interaction to database
- ✅ Updates evaluation template
- ✅ Categorizes question type
- ✅ Maintains statistics

**User Experience:** Completely invisible - no impact on app performance.

---

## Current Status

Check your current data anytime:

```bash
python check_evaluation_data.py
```

This shows:
- Total interactions collected
- Question categories breakdown
- Plot types and domains
- Sample data preview

---

## Quick Commands

### 1. Check Data Status
```bash
python check_evaluation_data.py
```

### 2. View Rating Template
```bash
# Windows
start reports\data\rating_template.csv

# Mac/Linux
open reports/data/rating_template.csv
```

### 3. Generate Demo Report (with simulated ratings)
```bash
python create_real_evaluation.py
```

### 4. Generate Final Report (after adding real ratings)
```bash
python generate_report.py reports\data\rating_template.csv
```

---

## Files

### Essential Files (Keep These)

**Scripts:**
- `check_evaluation_data.py` - Check data status
- `create_real_evaluation.py` - Extract data + demo report
- `generate_report.py` - Generate final report
- `utils/auto_evaluator.py` - Automatic collection system
- `utils/report_generator.py` - Report generation engine

**Data:**
- `reports/data/rating_template.csv` - Auto-updated with all interactions
- `reports/data/auto_eval_stats.json` - Auto-updated statistics

**Documentation:**
- `EVALUATION_README.md` - This file
- `AUTO_EVALUATION_SYSTEM.md` - Technical details
- `EVALUATION_SUMMARY.md` - Complete summary
- `HOW_TO_CREATE_REAL_EVALUATION.md` - Step-by-step guide

---

## Creating Real Evaluation

### Current Status:
- ✅ Data collection: AUTOMATIC
- ✅ Real interactions: Being collected
- ⏳ Human ratings: Need to be added

### Steps:

1. **Let Data Collect**
   - Users interact with app normally
   - Data collects automatically in background
   - Check progress: `python check_evaluation_data.py`

2. **Get Human Responses** (when ready)
   - Show same plots to human TAs
   - Have them answer same questions
   - Save their responses

3. **Get Ratings** (2-3 independent raters)
   - Blind rating (raters don't know which is AI/human)
   - Rate on 1-5 scale:
     - Clarity (how clear?)
     - Helpfulness (helps learning?)
     - Accuracy (correct information?)

4. **Fill Template**
   - Open: `reports/data/rating_template.csv`
   - Replace 0.0 with actual ratings
   - Save file

5. **Generate Report**
   ```bash
   python generate_report.py reports\data\rating_template.csv
   ```

---

## Data Format

### Rating Template Columns:

- `interaction_id` - Database ID
- `plot_path` - Path to plot image
- `category` - Auto-categorized question type
- `question` - User's question
- `ai_response` - DataPlotQA's answer
- `ai_clarity` - AI clarity rating (1-5)
- `ai_helpfulness` - AI helpfulness rating (1-5)
- `ai_accuracy` - AI accuracy rating (1-5)
- `human_clarity` - Human TA clarity rating (1-5)
- `human_helpfulness` - Human TA helpfulness rating (1-5)
- `human_accuracy` - Human TA accuracy rating (1-5)

### Rating Scale (1-5):

**1 = Poor** | **2 = Fair** | **3 = Good** | **4 = Very Good** | **5 = Excellent**

---

## Report Features

Generated reports include:

### Statistical Analysis:
- Mean, median, standard deviation
- Paired t-tests (AI vs Human)
- Effect sizes (Cohen's d)
- Win rates
- P-values

### Visualizations:
1. Bar charts (AI vs Human comparison)
2. Box plots (distribution analysis)
3. Heatmaps (category performance)
4. Distribution plots (score histograms)
5. Scatter plots (direct comparison)
6. Radar charts (multi-metric overview)

### Outputs:
- Professional HTML report
- JSON statistics file
- High-resolution PNG charts (300 DPI)

---

## Troubleshooting

### Template not updating?
```bash
# Manually trigger update
python create_real_evaluation.py
```

### Want to verify data accuracy?
```bash
# Check all details
python check_evaluation_data.py

# View raw template
start reports\data\rating_template.csv
```

### Need fresh start?
```bash
# Backup current data
copy reports\data\rating_template.csv reports\data\rating_template_backup.csv

# Delete to regenerate
del reports\data\rating_template.csv

# Use app - will regenerate automatically
```

---

## Technical Details

### Integration Points:
- `app/main.py` - Auto-update after interactions
- `utils/auto_evaluator.py` - Collection logic
- `utils/report_generator.py` - Report generation
- `utils/database.py` - Data storage

### Performance:
- Update time: < 100ms
- Storage: ~2KB per 100 interactions
- No API calls
- Local storage only

### Privacy:
- All data stored locally
- No external transmission
- Admin access only

---

## FAQ

**Q: Is collection really automatic?**
A: Yes! Every interaction updates the template automatically.

**Q: Do I need to run scripts?**
A: Only to check status or generate reports. Collection is automatic.

**Q: Will users see this?**
A: No, it's completely invisible to users.

**Q: How do I verify it's working?**
A: Run `python check_evaluation_data.py` anytime.

**Q: Can I disable collection?**
A: Yes, remove auto-update calls from `app/main.py`.

---

## Status

✅ **ACTIVE** - System is collecting data automatically

Check anytime: `python check_evaluation_data.py`
