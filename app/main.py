"""
DataPlotQA: Multimodal Agent for Interpreting Academic Visualizations
Enhanced Professional UI - Final Version (No Warnings)
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime
import time
import re
import html

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.vision_processor import VisionProcessor
from utils.explanation_generator import ExplanationGenerator
from utils.database import Database
from utils.auto_evaluator import AutoEvaluator

# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="DataPlotQA - AI Teaching Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# ENHANCED MODERN CSS
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main Header - Minimal & Clean */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .main-header p {
        margin: 0.25rem 0 0 0;
        font-size: 0.8rem;
        opacity: 0.85;
        font-weight: 300;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Chat Messages - ChatGPT Style */
    .chat-message {
        display: flex;
        gap: 0.65rem;
        margin-bottom: 1rem;
        animation: messageSlide 0.25s ease-out;
    }

    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .message-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        flex-shrink: 0;
        margin-top: 4px;
    }

    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .assistant-avatar {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    .message-bubble {
        flex: 1;
        min-width: 0;
    }

    .message-role {
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: #6b7280;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .message-content {
        font-size: 0.875rem;
        color: #1f2937;
        line-height: 1.65;
        word-wrap: break-word;
    }

    .user-message .message-content {
        background: #eff6ff;
        padding: 0.65rem 0.9rem;
        border-radius: 16px;
        border-bottom-left-radius: 4px;
        border: 1px solid #dbeafe;
    }

    .assistant-message .message-content {
        background: transparent;
        padding: 0.4rem 0;
    }

    /* Section Headers */
    .section-header {
        font-size: 0.8rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }


    .message-time {
        font-size: 0.625rem;
        color: #9ca3af;
        font-weight: 300;
    }

    /* Metric Cards - Compact */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
        transition: all 0.2s ease;
        border: 1px solid #e0e0e0;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* Upload Box - Compact */
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        background: #f5f7fa;
        transition: all 0.3s ease;
    }
    .upload-box:hover {
        border-color: #764ba2;
        background: #e3f2fd;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    .upload-box h2 {
        font-size: 1.2rem;
        margin: 0.5rem 0;
    }
    .upload-box p {
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }

    /* Button Enhancements */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }

    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {
        background: #fafbfc;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    /* Sidebar Section Cards */
    .sidebar-card {
        background: white;
        padding: 0.875rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 0.75rem;
        border: 1px solid #e8eaed;
    }

    /* Status Container */
    [data-testid="stStatusWidget"] {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        border-radius: 10px;
        font-weight: 600;
    }

    /* Chat Input Enhancement */
    .stChatInput {
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Image Container */
    .element-container img {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    .element-container img:hover {
        transform: scale(1.01);
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* Info Box Styling */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }

    /* Divider Enhancement */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }

    /* Chat Container Styling */
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }

    /* Empty State */
    .empty-chat {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 1.5rem;
        text-align: center;
        color: #6b7280;
    }

    .empty-chat-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }

    /* Copy Button */
    .copy-button {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.5rem;
        background: transparent;
        border: 1px solid transparent;
        border-radius: 5px;
        font-size: 0.65rem;
        color: #9ca3af;
        cursor: pointer;
        transition: all 0.15s;
        margin-left: 0.5rem;
    }

    .copy-button:hover {
        background: #f3f4f6;
        border-color: #e5e7eb;
        color: #4b5563;
    }

    /* Markdown Formatting in Messages */
    .message-content p {
        margin: 0.5rem 0;
    }

    .message-content ul, .message-content ol {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }

    .message-content li {
        margin: 0.25rem 0;
    }

    .message-content code {
        background: #f3f4f6;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
        color: #e11d48;
    }

    .message-content pre {
        background: #1f2937;
        color: #f3f4f6;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
        margin: 0.75rem 0;
    }

    .message-content pre code {
        background: transparent;
        color: #f3f4f6;
        padding: 0;
    }

    .message-content strong {
        font-weight: 600;
        color: #111827;
    }

    .message-content em {
        font-style: italic;
        color: #4b5563;
    }

    .message-content blockquote {
        border-left: 3px solid #667eea;
        padding-left: 1rem;
        margin: 0.75rem 0;
        color: #6b7280;
        font-style: italic;
    }

    /* Typing Indicator */
    .typing-indicator {
        display: flex;
        gap: 0.3rem;
        padding: 0.75rem 1rem;
    }

    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #9ca3af;
        animation: typingBounce 1.4s infinite;
    }

    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typingBounce {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-10px);
        }
    }

    /* Message Actions */
    .message-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
        opacity: 0.7;
    }

    .message-actions:hover {
        opacity: 1;
    }

    .action-btn {
        padding: 0.25rem 0.5rem;
        background: transparent;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        font-size: 0.75rem;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.2s;
    }

    .action-btn:hover {
        background: #f3f4f6;
        border-color: #667eea;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# MARKDOWN FORMATTER
# -------------------------------------------------------------
def format_markdown(text):
    """Convert markdown-like text to HTML with proper formatting"""
    # Escape HTML first
    text = html.escape(text)

    # Code blocks (```code```)
    text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)

    # Inline code (`code`)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Bold (**text** or __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # Italic (*text* or _text_)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)

    # Line breaks
    text = text.replace('\n', '<br>')

    # Bullet points (lines starting with - or *)
    text = re.sub(r'<br>[-\*]\s+(.+?)(?=<br>|$)', r'<br>• \1', text)

    # Numbered lists
    text = re.sub(r'<br>(\d+)\.\s+(.+?)(?=<br>|$)', r'<br>\1. \2', text)

    return text

# -------------------------------------------------------------
# SESSION INITIALIZATION
# -------------------------------------------------------------
def initialize_session_state():
    """Initialize all session state variables"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_image" not in st.session_state:
        st.session_state.current_image = None
    if "plot_analysis" not in st.session_state:
        st.session_state.plot_analysis = None
    if "db" not in st.session_state:
        st.session_state.db = Database()
    if "vision_processor" not in st.session_state:
        st.session_state.vision_processor = VisionProcessor()
    if "explanation_generator" not in st.session_state:
        st.session_state.explanation_generator = ExplanationGenerator()
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "message_feedback" not in st.session_state:
        st.session_state.message_feedback = {}

    # Ensure uploads folder exists
    uploads_dir = Path(__file__).parent.parent / "data" / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# MAIN APP
# -------------------------------------------------------------
def main():
    initialize_session_state()
    
    # ---------------------------------------------------------
    # COMPACT HEADER
    # ---------------------------------------------------------
    st.markdown("""
        <div class="main-header">
            <h1>📊 DataPlotQA</h1>
            <p>AI-Powered Scientific Visualization Assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------------
    with st.sidebar:
        # Upload Section - Top Priority
        st.markdown('<p class="section-header">📁 Upload Plot</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["png", "jpg", "jpeg", "pdf"],
            help="Upload a scientific visualization",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            # Show thumbnail
            st.image(uploaded_file, caption="Preview", width="stretch")
            
            if st.button("🔍 Analyze Plot", type="primary", width="stretch"):
                with st.status("🤖 Analyzing your plot...", expanded=True) as status:
                    try:
                        st.write("📸 Reading image...")
                        time.sleep(0.3)
                        
                        # Save file
                        uploads_dir = Path(__file__).parent.parent / "data" / "uploads"
                        file_path = uploads_dir / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        st.write("🔍 Detecting plot elements...")
                        time.sleep(0.3)
                        
                        # Analyze
                        st.session_state.current_image = str(file_path)
                        analysis = st.session_state.vision_processor.analyze_plot(str(file_path))
                        st.session_state.plot_analysis = analysis
                        
                        st.write("🤖 Generating explanation...")
                        time.sleep(0.3)
                        
                        # Generate initial explanation
                        initial_explanation = st.session_state.explanation_generator.generate_initial_explanation(analysis)
                        
                        st.session_state.chat_history = [
                            {
                                "role": "assistant", 
                                "content": initial_explanation,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            }
                        ]
                        
                        # Save to database
                        st.session_state.db.save_interaction(
                            image_path=str(file_path),
                            question="[Initial Analysis]",
                            response=initial_explanation,
                            plot_analysis=analysis
                        )
                        
                        st.write("✅ Analysis complete!")
                        status.update(label="✅ Ready to answer questions!", state="complete")
                        time.sleep(0.5)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("💡 Tip: Check your ANTHROPIC_API_KEY in .env file")
                        status.update(label="❌ Analysis failed", state="error")
        
        st.divider()

        # Statistics Dashboard - Compact
        st.markdown('<p class="section-header">📊 Statistics</p>', unsafe_allow_html=True)
        stats = st.session_state.db.get_statistics()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats['total_plots']}</div>
                    <div class="metric-label">Plots</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stats['total_interactions']}</div>
                    <div class="metric-label">Questions</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()

        # Actions
        st.markdown('<p class="section-header">⚙️ Actions</p>', unsafe_allow_html=True)
        
        if st.button("📥 Export", use_container_width=True):
            if st.session_state.chat_history:
                # Generate export text
                export_text = "DataPlotQA Conversation Export\n"
                export_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                export_text += "=" * 60 + "\n\n"

                for msg in st.session_state.chat_history:
                    role = "You" if msg['role'] == 'user' else "DataPlotQA"
                    timestamp = msg.get('timestamp', '')
                    export_text += f"{role} [{timestamp}]:\n"
                    export_text += f"{msg['content']}\n\n"
                    export_text += "-" * 60 + "\n\n"

                st.download_button(
                    "💾 Download",
                    export_text,
                    file_name=f"dataplotqa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.info("No conversation yet!")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        with col2:
            if st.button("🔄 New", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.current_image = None
                st.session_state.plot_analysis = None
                st.rerun()

        st.divider()

        # About Section - Bottom
        st.markdown('<p class="section-header">🎯 About</p>', unsafe_allow_html=True)
        st.markdown("""
            <div class="sidebar-card">
                <p style='margin: 0.2rem 0; font-size: 0.8rem; color: #555;'>🔍 Visual Analysis</p>
                <p style='margin: 0.2rem 0; font-size: 0.8rem; color: #555;'>📚 Pedagogical Explanations</p>
                <p style='margin: 0.2rem 0; font-size: 0.8rem; color: #555;'>💬 Interactive Dialogue</p>
                <p style='margin: 0.2rem 0; font-size: 0.8rem; color: #555;'>🌐 Multi-domain Support</p>
            </div>
        """, unsafe_allow_html=True)

        st.caption(f"DataPlotQA v2.0 | {datetime.now().strftime('%Y-%m-%d')}")
    
    # ---------------------------------------------------------
    # MAIN CONTENT AREA (TWO COLUMNS)
    # ---------------------------------------------------------
    col1, col2 = st.columns([1, 1.6], gap="large")

    # ---------------------------------------------------------
    # LEFT COLUMN — IMAGE & ANALYSIS
    # ---------------------------------------------------------
    with col1:
        st.markdown('<p class="section-header">📷 Current Plot</p>', unsafe_allow_html=True)
        
        if st.session_state.current_image:
            st.image(st.session_state.current_image)
            
            if st.session_state.plot_analysis:
                with st.expander("📊 Detailed Analysis", expanded=False):
                    analysis = st.session_state.plot_analysis
                    
                    # Metrics
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Plot Type", analysis.get("plot_type", "Unknown"))
                    metric_col2.metric("Domain", analysis.get("domain", "Unknown"))
                    
                    # Axes Information
                    if analysis.get("axes"):
                        st.markdown("**Axes Information:**")
                        axes = analysis["axes"]
                        if "x_axis" in axes:
                            st.write(f"• **X-axis:** {axes['x_axis'].get('label', 'N/A')}")
                        if "y_axis" in axes:
                            st.write(f"• **Y-axis:** {axes['y_axis'].get('label', 'N/A')}")
                    
                    # Data Series
                    if analysis.get("data_series"):
                        st.markdown("**Data Series:**")
                        for series in analysis["data_series"][:3]:
                            st.write(f"• {series.get('name', 'Unnamed')}")
        else:
            st.markdown("""
                <div class="upload-box">
                    <h2>📊 No Plot Selected</h2>
                    <p style='color: #666;'>
                        Upload a plot using the sidebar
                    </p>
                    <p style='color: #999;'>
                        Supports: PNG, JPG, JPEG, PDF
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # RIGHT COLUMN — CONVERSATION
    # ---------------------------------------------------------
    with col2:
        st.markdown('<p class="section-header">💬 Conversation</p>', unsafe_allow_html=True)

        # Chat messages - full height
        if not st.session_state.chat_history:
            st.markdown("""
                <div class="empty-chat">
                    <div class="empty-chat-icon">💬</div>
                    <h3 style='margin: 0; font-size: 1.1rem; color: #374151;'>Start a Conversation</h3>
                    <p style='margin: 0.5rem 0 0 0; font-size: 0.875rem;'>Upload a plot and click 'Analyze' to begin</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for idx, msg in enumerate(st.session_state.chat_history):
                timestamp = msg.get('timestamp', '')
                msg_id = f"msg_{idx}"

                if msg["role"] == "user":
                    user_content = html.escape(msg["content"])
                    st.markdown(f"""
                        <div class="chat-message user-message">
                            <div class="message-avatar user-avatar">👤</div>
                            <div class="message-bubble">
                                <div class="message-role">
                                    You
                                    <span class="message-time">{timestamp}</span>
                                </div>
                                <div class="message-content">{user_content}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Format assistant message with markdown
                    formatted_content = format_markdown(msg["content"])
                    # Prepare copy text (escape for JavaScript)
                    copy_text = msg["content"].replace("'", "&#39;").replace('"', '&quot;').replace('\n', ' ')

                    st.markdown(f"""
                        <div class="chat-message assistant-message">
                            <div class="message-avatar assistant-avatar">🤖</div>
                            <div class="message-bubble">
                                <div class="message-role">
                                    DataPlotQA
                                    <span class="message-time">{timestamp}</span>
                                    <button class="copy-button" onclick="navigator.clipboard.writeText('{copy_text}')">
                                        📋 Copy
                                    </button>
                                </div>
                                <div class="message-content">{formatted_content}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Message actions - Rating System
                    action_col1, action_col2, action_col3 = st.columns([1, 1, 8])

                    with action_col1:
                        if st.button("⭐", key=f"rate_{msg_id}", help="Rate this response", use_container_width=True):
                            # Toggle rating form visibility
                            rating_key = f"show_rating_{msg_id}"
                            if rating_key not in st.session_state:
                                st.session_state[rating_key] = False
                            st.session_state[rating_key] = not st.session_state[rating_key]
                            st.rerun()

                    with action_col2:
                        if st.button("🔄 Retry", key=f"regen_{msg_id}", help="Generate new response", use_container_width=True):
                            # Find the corresponding user question
                            if idx > 0 and st.session_state.chat_history[idx-1]["role"] == "user":
                                question = st.session_state.chat_history[idx-1]["content"]

                                with st.spinner("Regenerating..."):
                                    new_response = st.session_state.explanation_generator.generate_response(
                                        question,
                                        st.session_state.plot_analysis,
                                        st.session_state.chat_history[:idx-1]
                                    )

                                # Update the message
                                st.session_state.chat_history[idx]["content"] = new_response
                                st.session_state.chat_history[idx]["timestamp"] = datetime.now().strftime("%H:%M:%S")
                                st.rerun()

                    # Rating Form (shown when Rate button clicked)
                    rating_key = f"show_rating_{msg_id}"
                    if st.session_state.get(rating_key, False):
                        st.markdown("---")

                        # Friendly rating interface
                        st.markdown("""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                        padding: 15px; border-radius: 10px; margin: 10px 0; color: white;">
                                <h4 style="margin: 0 0 10px 0;">How was this response?</h4>
                                <p style="margin: 0; opacity: 0.9; font-size: 0.9em;">
                                    Your feedback helps improve the AI! Rate from 1 (poor) to 5 (excellent)
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

                        # Star rating with sliders
                        rate_col1, rate_col2, rate_col3 = st.columns(3)

                        with rate_col1:
                            st.markdown("**Clarity**")
                            st.caption("How clear?")
                            clarity = st.radio(
                                "Clarity rating",
                                options=[1, 2, 3, 4, 5],
                                format_func=lambda x: "★" * x,
                                key=f"clarity_{msg_id}",
                                horizontal=True,
                                label_visibility="collapsed"
                            )

                        with rate_col2:
                            st.markdown("**Helpfulness**")
                            st.caption("How helpful?")
                            helpfulness = st.radio(
                                "Helpfulness rating",
                                options=[1, 2, 3, 4, 5],
                                format_func=lambda x: "★" * x,
                                key=f"helpful_{msg_id}",
                                horizontal=True,
                                label_visibility="collapsed"
                            )

                        with rate_col3:
                            st.markdown("**Accuracy**")
                            st.caption("How accurate?")
                            accuracy = st.radio(
                                "Accuracy rating",
                                options=[1, 2, 3, 4, 5],
                                format_func=lambda x: "★" * x,
                                key=f"accurate_{msg_id}",
                                horizontal=True,
                                label_visibility="collapsed"
                            )

                        # Submit button
                        col1, col2, col3 = st.columns([3, 2, 3])
                        with col2:
                            if st.button("Submit Rating", key=f"submit_rating_{msg_id}",
                                       type="primary", use_container_width=True):
                                # Save rating to database
                                try:
                                    # Get interaction ID from chat history
                                    if idx > 0 and st.session_state.chat_history[idx-1]["role"] == "user":
                                        question = st.session_state.chat_history[idx-1]["content"]
                                        response = msg["content"]

                                        # Save rating
                                        st.session_state.db.save_feedback(
                                            image_path=st.session_state.current_image,
                                            question=question,
                                            response=response,
                                            rating={
                                                'clarity': clarity,
                                                'helpfulness': helpfulness,
                                                'accuracy': accuracy
                                            }
                                        )

                                        # Update evaluation data
                                        try:
                                            auto_eval = AutoEvaluator()
                                            auto_eval.auto_update()
                                        except Exception:
                                            pass

                                        st.session_state[rating_key] = False
                                        st.success("Thank you! Your rating has been saved.")
                                        st.balloons()
                                        time.sleep(1)
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error saving rating: {str(e)}")

                        st.markdown("---")

            # Show typing indicator if generating
            if st.session_state.is_generating:
                st.markdown("""
                    <div class="chat-message assistant-message">
                        <div class="message-avatar assistant-avatar">🤖</div>
                        <div class="message-bubble">
                            <div class="message-role">DataPlotQA</div>
                            <div class="typing-indicator">
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                                <div class="typing-dot"></div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # CHAT INPUT (TOP-LEVEL, OUTSIDE COLUMNS)
    # ---------------------------------------------------------
    if st.session_state.plot_analysis:
        user_input = st.chat_input("💭 Ask a question about the plot...")

        # Quick Questions - Below Chat Input
        st.markdown('<p class="section-header" style="margin-top: 1rem;">💡 Quick Questions</p>', unsafe_allow_html=True)

        quick_questions = [
            ("🎯", "Purpose of visualization"),
            ("📐", "Explain axes and scales"),
            ("📈", "Trends and patterns"),
            ("📊", "Error bars meaning"),
            ("💡", "Key conclusions")
        ]

        full_questions = [
            "What is the purpose of this visualization?",
            "Explain the axes and scales used",
            "What trends or patterns do you observe?",
            "What do the error bars indicate?",
            "What conclusions can be drawn from this?"
        ]

        # Display as inline buttons
        cols = st.columns(5)
        for i, ((emoji, label), full_q) in enumerate(zip(quick_questions, full_questions)):
            with cols[i]:
                if st.button(f"{emoji}\n{label}", key=f"q_{i}", use_container_width=True):
                    # Add question to history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": full_q,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

                    # Generate response with typing indicator
                    st.session_state.is_generating = True
                    st.rerun()

                    response = st.session_state.explanation_generator.generate_response(
                        full_q,
                        st.session_state.plot_analysis,
                        st.session_state.chat_history
                    )

                    st.session_state.is_generating = False

                    # Add response to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

                    # Save to database
                    st.session_state.db.save_interaction(
                        image_path=st.session_state.current_image,
                        question=full_q,
                        response=response,
                        plot_analysis=st.session_state.plot_analysis
                    )

                    # Auto-update evaluation data
                    try:
                        auto_eval = AutoEvaluator()
                        auto_eval.auto_update()
                    except Exception:
                        pass  # Silent fail - don't interrupt user experience

                    st.rerun()
        
        if user_input:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Generate response with typing indicator
            st.session_state.is_generating = True
            st.rerun()

            try:
                response = st.session_state.explanation_generator.generate_response(
                    user_input,
                    st.session_state.plot_analysis,
                    st.session_state.chat_history
                )

                st.session_state.is_generating = False

                # Add assistant message
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })

                # Save to database
                st.session_state.db.save_interaction(
                    image_path=st.session_state.current_image,
                    question=user_input,
                    response=response,
                    plot_analysis=st.session_state.plot_analysis
                )

                # Auto-update evaluation data
                try:
                    auto_eval = AutoEvaluator()
                    auto_eval.auto_update()
                except Exception:
                    pass  # Silent fail - don't interrupt user experience

            except Exception as e:
                st.session_state.is_generating = False
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"⚠️ Error generating response: {str(e)}\n\nPlease check your API key configuration.",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })

            st.rerun()

# -------------------------------------------------------------
# RUN APP
# -------------------------------------------------------------
if __name__ == "__main__":
    main()