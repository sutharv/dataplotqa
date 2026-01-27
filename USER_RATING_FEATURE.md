# User Rating Feature

## Overview

Users can now **rate AI responses directly in the app**! This automatically collects evaluation data without needing external raters.

---

## How It Works

### For Users:

1. **User asks a question** → AI responds
2. **User clicks ⭐ Rate button** under the response
3. **Rating form appears** with 3 categories:
   - **Clarity** (1-5): How clear and understandable?
   - **Helpful** (1-5): How helpful for learning?
   - **Accurate** (1-5): Is the information correct?
4. **User selects ratings** and clicks "✅ Submit Rating"
5. **Rating saved!** Toast notification confirms

### For You (Admin):

- ✅ Ratings automatically saved to database
- ✅ Evaluation template auto-updates with ratings
- ✅ Real user feedback collected passively
- ✅ No manual data entry needed

---

## User Interface

### Rating Button
Every AI response now has:
- **⭐ Rate** - Opens rating form
- **🔄 Retry** - Regenerate response

### Rating Form
When user clicks "⭐ Rate":
```
Rate this response (1-5):
[Clarity ▼] [Helpful ▼] [Accurate ▼] [✅ Submit Rating]
```

Scale:
- 0 = Not rated (select this to start)
- 1 = Poor
- 2 = Fair
- 3 = Good
- 4 = Very Good
- 5 = Excellent

---

## Data Flow

```
User rates AI response
       ↓
Rating saved to feedback table
       ↓
AutoEvaluator extracts rating
       ↓
Updates rating_template.csv
       ↓
Ready for report generation!
```

---

## Database Schema

### Feedback Table (stores ratings):
- `interaction_id` - Links to interaction
- `clarity_rating` - 1-5 scale
- `helpfulness_rating` - 1-5 scale
- `accuracy_rating` - 1-5 scale
- `comments` - Optional text (not used yet)
- `timestamp` - When rated

### Integration:
- Ratings automatically extracted from feedback table
- Linked to interactions via `interaction_id`
- Latest rating used if multiple ratings exist

---

## Checking Ratings

### View Collected Ratings:

```bash
# Check how many ratings collected
python check_evaluation_data.py
```

This shows:
- Interactions with ratings (non-zero scores)
- Interactions without ratings (0.0 scores)
- Average ratings collected

### View Raw Data:

```bash
# Open template with ratings
start reports\data\rating_template.csv
```

Columns with ratings:
- `ai_clarity` - User rating (1-5 or 0.0 if not rated)
- `ai_helpfulness` - User rating (1-5 or 0.0 if not rated)
- `ai_accuracy` - User rating (1-5 or 0.0 if not rated)

---

## Generate Reports

### With User Ratings Only:

```bash
python generate_report.py reports\data\rating_template.csv
```

This creates a report showing:
- Average user ratings for AI responses
- Distribution of ratings
- Category breakdowns
- Interaction-level analysis

**Note:** Human TA ratings still at 0.0 (need manual entry if comparing AI vs Human)

### Adding Human TA Ratings:

1. Get human TA responses for same questions
2. Have raters evaluate human responses
3. Open `rating_template.csv`
4. Fill in `human_clarity`, `human_helpfulness`, `human_accuracy` columns
5. Run: `python generate_report.py reports\data\rating_template.csv`

---

## Benefits

### Automatic Collection:
- ✅ No need to manually collect ratings
- ✅ Users provide feedback as they use the app
- ✅ Real-world usage data
- ✅ Continuous evaluation

### User Experience:
- ✅ Simple 3-click rating process
- ✅ Optional (users can skip)
- ✅ Instant feedback confirmation
- ✅ Non-intrusive

### Data Quality:
- ✅ Real users in real scenarios
- ✅ Authentic feedback
- ✅ Context-aware ratings
- ✅ Timestamp tracked

---

## Usage Scenarios

### Scenario 1: AI-Only Evaluation
**Goal:** Understand AI performance from user perspective

**Process:**
1. Users use app and rate responses
2. Ratings automatically collect
3. Generate report with user ratings
4. Analyze: What types of questions score well? What needs improvement?

### Scenario 2: AI vs Human Comparison
**Goal:** Compare AI against human teaching assistants

**Process:**
1. Users rate AI responses (automatic)
2. Get human TA responses for same questions
3. Have raters evaluate human responses
4. Add human ratings to template manually
5. Generate comparative report

### Scenario 3: Continuous Monitoring
**Goal:** Track AI performance over time

**Process:**
1. Users rate responses continuously
2. Check ratings weekly: `python check_evaluation_data.py`
3. Generate reports monthly
4. Track trends and improvements

---

## Implementation Details

### Modified Files:

**app/main.py:**
- Added ⭐ Rate button for each AI message
- Added collapsible rating form (Clarity, Helpful, Accurate)
- Auto-saves ratings to database
- Triggers auto-evaluator update

**utils/database.py:**
- Enhanced `save_feedback()` method
- Accepts interaction_id or finds it via image_path + question
- Handles rating dictionary format

**utils/auto_evaluator.py:**
- Extracts ratings from feedback table
- Links ratings to interactions
- Updates template with real user ratings

---

## Rating Statistics

Check current rating collection:

```bash
python check_evaluation_data.py
```

Shows:
- Total interactions: X
- Rated interactions: Y (interactions with ratings > 0)
- Unrated interactions: Z (ratings still at 0.0)
- Rating coverage: Y/X percentage

---

## Tips for Encouraging User Ratings

### In-App Messaging:
- "Your feedback helps improve the AI!"
- "Rate this response to help us learn"
- "How helpful was this explanation?"

### Incentives:
- Show rating statistics to users
- "You've helped rate X responses!"
- "Join X other users improving the AI"

### Strategic Placement:
- Rate button on every response ✓
- Clear labels (Clarity, Helpful, Accurate) ✓
- Quick dropdown selection (1-5) ✓
- One-click submit ✓

---

## Privacy & Ethics

### User Data:
- Ratings are anonymous (user not tracked)
- Only interaction + rating stored
- No personally identifiable information
- Local storage only

### Transparency:
- Users know they're rating AI
- Clear what ratings are used for
- Optional participation
- Can see their ratings impact

---

## FAQ

**Q: Do all users need to rate?**
A: No, it's optional. Ratings help but aren't required to use the app.

**Q: Can users rate multiple times?**
A: Yes, latest rating overwrites previous ones.

**Q: What if no one rates?**
A: Template still updates, just with 0.0 ratings. You can add ratings manually.

**Q: Can users see others' ratings?**
A: No, ratings are aggregated for admin analysis only.

**Q: How many ratings needed for valid evaluation?**
A: Minimum 30 rated interactions recommended for statistical significance.

---

## Troubleshooting

### Ratings not saving?
1. Check database connection
2. Check feedback table exists
3. Verify interaction_id lookup works

### Ratings not appearing in template?
1. Run: `python check_evaluation_data.py`
2. Verify ratings > 0.0 in database
3. Manual update: `python create_real_evaluation.py`

### Users can't see rating form?
1. Check Streamlit version
2. Verify UI elements render correctly
3. Check browser console for errors

---

## Summary

**Before:** Need external raters to evaluate AI responses manually.

**After:** Users rate AI responses as they use the app - automatic evaluation data collection!

**Result:** Continuous, real-world feedback with zero manual work.

---

**Status: ✅ ACTIVE** - Users can now rate responses in the app!
