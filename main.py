import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import time
from datetime import datetime
warnings.filterwarnings('ignore')

# Set page config with chess theme
st.set_page_config(
    page_title="♛ Lichess Chess Analytics Pro",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chess.com inspired green and black theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Dark Theme - Chess.com Style */
    .stApp {
        background: linear-gradient(135deg, #181818 0%, #1c2c1c 25%, #2c3e2c 50%, #1a2e1a 75%, #0f1f0f 100%);
        color: #ffffff;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Premium Styling - Chess.com Green */
    .css-1d391kg, .css-1cypcdb {
        background: linear-gradient(180deg, #0f1f0f 0%, #1a2e1a 50%, #2c3e2c 100%);
        border-right: 2px solid #81b64c;
    }
    
    .css-1cypcdb .stSelectbox > div > div {
        background-color: #1a2e1a;
        color: #ffffff;
        border: 1px solid #81b64c;
    }
    
    /* Premium Header with Chess.com Theme */
    .chess-master-header {
        background: linear-gradient(135deg, #0f1f0f 0%, #1a2e1a 25%, #2c3e2c 50%, #1a2e1a 75%, #0f1f0f 100%);
        color: #ffffff;
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 
            0 20px 40px rgba(129, 182, 76, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 1px 3px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(129, 182, 76, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .chess-master-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(129, 182, 76, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .chess-master-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 
            0 0 10px rgba(129, 182, 76, 0.5),
            0 0 20px rgba(129, 182, 76, 0.3),
            0 0 30px rgba(129, 182, 76, 0.1);
        background: linear-gradient(45deg, #81b64c, #9fcc5c, #81b64c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chess-master-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        margin-top: 1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Premium Metrics Cards - Chess.com Theme */
    .metric-card {
        background: linear-gradient(135deg, rgba(26, 46, 26, 0.8) 0%, rgba(44, 62, 44, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(129, 182, 76, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #81b64c, #9fcc5c, #81b64c);
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 25px 50px rgba(129, 182, 76, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: #81b64c;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #81b64c;
        text-shadow: 0 0 10px rgba(129, 182, 76, 0.5);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #cccccc;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Premium Analysis Cards */
    .analysis-mastercard {
        background: linear-gradient(135deg, rgba(26, 46, 26, 0.9) 0%, rgba(44, 62, 44, 0.9) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(129, 182, 76, 0.3);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .analysis-mastercard::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #81b64c, #9fcc5c, #81b64c);
    }
    
    .analysis-mastercard h2 {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        color: #81b64c;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 10px rgba(129, 182, 76, 0.3);
    }
    
    /* Upload Area Premium */
    .upload-masterzone {
        background: linear-gradient(135deg, rgba(26, 46, 26, 0.9) 0%, rgba(44, 62, 44, 0.9) 100%);
        backdrop-filter: blur(15px);
        border: 3px dashed rgba(129, 182, 76, 0.6);
        border-radius: 25px;
        padding: 4rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .upload-masterzone::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(129, 182, 76, 0.1) 0%, transparent 70%);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    
    .upload-masterzone:hover {
        border-color: #81b64c;
        box-shadow: 0 0 30px rgba(129, 182, 76, 0.4);
        transform: scale(1.02);
    }
    
    .upload-masterzone h2 {
        font-family: 'Orbitron', monospace;
        color: #81b64c;
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }
    
    /* Success Message */
    .success-master {
        background: linear-gradient(135deg, rgba(129, 182, 76, 0.2) 0%, rgba(159, 204, 92, 0.3) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(129, 182, 76, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        color: #81b64c;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(129, 182, 76, 0.2);
    }
    
    /* Button Premium Styling - Chess.com Green */
    .stButton > button {
        background: linear-gradient(135deg, #81b64c 0%, #9fcc5c 100%);
        color: #000000;
        border: none;
        border-radius: 15px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        padding: 0.75rem 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(129, 182, 76, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #9fcc5c 0%, #81b64c 100%);
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(129, 182, 76, 0.4);
    }
    
    /* Checkbox Styling */
    .stCheckbox > div {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* File Uploader Styling */
    .stFileUploader > div {
        border: 2px dashed rgba(129, 182, 76, 0.5);
        border-radius: 15px;
        background: rgba(26, 46, 26, 0.5);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    /* Plotly Chart Containers */
    .js-plotly-plot {
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Headers */
    .css-1cypcdb h1, .css-1cypcdb h2, .css-1cypcdb h3 {
        color: #81b64c;
        font-family: 'Orbitron', monospace;
    }
    
    /* Footer */
    .footer-master {
        background: linear-gradient(135deg, rgba(15, 31, 15, 0.9) 0%, rgba(26, 46, 26, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-top: 2px solid #81b64c;
        border-radius: 25px 25px 0 0;
        padding: 3rem 2rem;
        text-align: center;
        margin-top: 4rem;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Spinning Animation for Loading */
    .loading-spinner {
        display: inline-block;
        width: 2rem;
        height: 2rem;
        border: 3px solid rgba(129, 182, 76, 0.3);
        border-radius: 50%;
        border-top-color: #81b64c;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Additional Premium Touches */
    .stSelectbox > div > div {
        background-color: rgba(26, 46, 26, 0.8);
        border: 1px solid rgba(129, 182, 76, 0.3);
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(26, 46, 26, 0.8);
        border: 1px solid rgba(129, 182, 76, 0.3);
        border-radius: 10px;
        color: #ffffff;
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(26, 46, 26, 0.8);
        border: 1px solid rgba(129, 182, 76, 0.3);
        border-radius: 10px;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
@st.cache_data
def load_and_process_data(uploaded_file):
    """Load and process the chess dataset with enhanced error handling"""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Clean column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Parse result column into winner
        def get_winner(result):
            if result == '1-0':
                return 'White'
            elif result == '0-1':
                return 'Black'
            else:
                return 'Draw'
        
        df['winner'] = df['result'].apply(get_winner)
        df['utcdate'] = pd.to_datetime(df['utcdate'], errors='coerce')
        
        # Convert Elo columns to numeric
        df['whiteelo'] = pd.to_numeric(df['whiteelo'], errors='coerce')
        df['blackelo'] = pd.to_numeric(df['blackelo'], errors='coerce')
        
        # Add computed columns
        df['avg_elo'] = (df['whiteelo'] + df['blackelo']) / 2
        df['num_moves'] = df['moves'].apply(lambda x: len(str(x).strip().split()) if pd.notna(x) else 0)
        
        # Add month column
        df['month'] = df['utcdate'].dt.to_period('M')
        
        return df
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        return None

def create_premium_plotly_chart(chart_type, data=None, x=None, y=None, title="", **kwargs):
    """Create premium dark-themed Plotly charts with Chess.com colors"""
    
    # Chess.com inspired color palette
    colors = {
        'primary': '#81b64c',
        'secondary': '#9fcc5c', 
        'accent': '#6ea03c',
        'gradient': ['#81b64c', '#9fcc5c', '#6ea03c', '#5a8c30', '#4a7224']
    }
    
    # Common layout settings
    layout_settings = {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': dict(family="Inter", size=14, color="#ffffff"),
        'title': dict(
            text=title,
            font=dict(family="Orbitron", size=20, color="#81b64c", weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        'xaxis': dict(
            showgrid=True, 
            gridcolor='rgba(129, 182, 76, 0.1)',
            linecolor='rgba(129, 182, 76, 0.3)',
            color='#ffffff'
        ),
        'yaxis': dict(
            showgrid=True, 
            gridcolor='rgba(129, 182, 76, 0.1)',
            linecolor='rgba(129, 182, 76, 0.3)',
            color='#ffffff'
        ),
        'showlegend': True,
        'legend': dict(
            bgcolor='rgba(26, 46, 26, 0.8)',
            bordercolor='rgba(129, 182, 76, 0.3)',
            borderwidth=1,
            font=dict(color='#ffffff')
        )
    }
    
    if chart_type == 'bar':
        fig = px.bar(x=x, y=y, title=title, color_discrete_sequence=colors['gradient'])
    elif chart_type == 'line':
        fig = px.line(data, x=x, y=y, title=title, color_discrete_sequence=[colors['primary']])
        # Fixed: Use valid shape parameter and line_shape instead
        fig.update_traces(line=dict(width=4), marker=dict(size=8))
        fig.update_layout(xaxis=dict(type='category'))  # This helps with smoother line rendering
    elif chart_type == 'pie':
        fig = px.pie(values=y, names=x, title=title, color_discrete_sequence=colors['gradient'])
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='#000000', width=2))
        )
    elif chart_type == 'histogram':
        fig = px.histogram(data, x=x, title=title, color_discrete_sequence=[colors['primary']])
    elif chart_type == 'scatter':
        fig = px.scatter(data, x=x, y=y, title=title, color_discrete_sequence=[colors['primary']])
        fig.update_traces(marker=dict(size=10, opacity=0.7))
    elif chart_type == 'heatmap':
        fig = px.imshow(data, title=title, color_continuous_scale='Greens', aspect='auto')
    
    fig.update_layout(**layout_settings)
    return fig

def create_animated_metric_card(title, value, icon, trend=None):
    """Create animated metric cards with Chess.com theme"""
    trend_indicator = ""
    if trend:
        if trend > 0:
            trend_indicator = f"<span style='color: #81b64c;'>↗️ +{trend:.1f}%</span>"
        else:
            trend_indicator = f"<span style='color: #dc3545;'>↘️ {trend:.1f}%</span>"
    
    return f"""
    <div class="metric-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        {trend_indicator}
    </div>
    """

def show_loading_animation(text="Processing chess data"):
    """Show premium loading animation"""
    return st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div class="loading-spinner"></div>
        <p style="margin-top: 1rem; color: #81b64c; font-family: 'Inter', sans-serif;">
            ♟️ {text}...
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main app
def main():
    # Premium Header
    st.markdown("""
    <div class="chess-master-header">
        <h1>♛ LICHESS CHESS ANALYTICS PRO ♛</h1>
        <p>🏆 Professional Chess Performance Analysis & Strategic Insights 🏆</p>
        <div style="margin-top: 1rem; font-size: 1rem; opacity: 0.7;">
            Powered by Advanced AI Analytics • Real-time Visualizations • Professional Grade
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; border-bottom: 2px solid #81b64c; margin-bottom: 2rem;">
            <h2 style="color: #81b64c; font-family: 'Orbitron', monospace;">♟️ CONTROL PANEL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # File upload with premium styling
        st.markdown("### 📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload Chess Games CSV",
            type=['csv'],
            help="Upload your Lichess games CSV file for professional analysis",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.markdown('<div class="success-master">✅ File loaded successfully!</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Loading animation
        loading_placeholder = st.empty()
        with loading_placeholder:
            show_loading_animation("Analyzing your chess mastery")
        
        # Simulate processing time for better UX
        time.sleep(1)
        
        # Load and process data
        df = load_and_process_data(uploaded_file)
        loading_placeholder.empty()
        
        if df is not None:
            # Sidebar Analysis Controls
            with st.sidebar:
                st.markdown("### 🎯 Analysis Modules")
                
                modules = {
                    "📊 Performance Overview": st.checkbox("📊 Performance Overview", True),
                    "🎯 Game Outcomes": st.checkbox("🎯 Game Outcomes Analysis", True),
                    "⭐ Rating Analytics": st.checkbox("⭐ Rating Analytics", True),
                    "🏁 Game Termination": st.checkbox("🏁 Termination Analysis", True),
                    "♟️ Opening Mastery": st.checkbox("♟️ Opening Analysis", True),
                    "👑 Player Insights": st.checkbox("👑 Player Performance", True),
                    "⏱️ Time Controls": st.checkbox("⏱️ Time Control Analysis", True),
                    "📈 Trend Analysis": st.checkbox("📈 Trend Analysis", True),
                    "🔬 Advanced Stats": st.checkbox("🔬 Advanced Statistics", True)
                }
                
                st.markdown("### ⚙️ Customization")
                chart_style = st.selectbox("Chart Style", ["Professional", "Minimal", "Vibrant"])
                show_animations = st.checkbox("Enable Animations", True)
            
            # Performance Overview
            if modules["📊 Performance Overview"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>📊 PERFORMANCE OVERVIEW</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Key metrics with animations
                col1, col2, col3, col4 = st.columns(4)
                
                total_games = len(df)
                unique_players = len(set(df['white'].tolist() + df['black'].tolist()))
                avg_rating = df['avg_elo'].mean()
                avg_moves = df['num_moves'].mean()
                
                with col1:
                    st.markdown(create_animated_metric_card(
                        "Total Games", f"{total_games:,}", "🎮"
                    ), unsafe_allow_html=True)
                
                with col2:
                    st.markdown(create_animated_metric_card(
                        "Unique Players", f"{unique_players:,}", "👥"
                    ), unsafe_allow_html=True)
                
                with col3:
                    st.markdown(create_animated_metric_card(
                        "Average Rating", f"{avg_rating:.0f}", "⭐", 
                    ), unsafe_allow_html=True)
                
                with col4:
                    st.markdown(create_animated_metric_card(
                        "Avg Game Length", f"{avg_moves:.0f}", "♟️"
                    ), unsafe_allow_html=True)
                
                # Enhanced data preview
                st.markdown("### 📋 Data Preview")
                st.dataframe(
                    df.head(10).style.format({
                        'avg_elo': '{:.0f}',
                        'whiteelo': '{:.0f}',
                        'blackelo': '{:.0f}',
                        'num_moves': '{:.0f}'
                    }),
                    use_container_width=True
                )
            
            # Game Outcomes Analysis
            if modules["🎯 Game Outcomes"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>🎯 GAME OUTCOMES ANALYSIS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    outcomes = df['winner'].value_counts()
                    fig_pie = create_premium_plotly_chart(
                        'pie', x=outcomes.index, y=outcomes.values,
                        title="🎯 Game Outcome Distribution"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    win_stats = df['winner'].value_counts()
                    percentages = (win_stats / len(df) * 100).round(1)
                    fig_bar = create_premium_plotly_chart(
                        'bar', x=percentages.index, y=percentages.values,
                        title="📊 Win Rate Percentages"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # Rating Analytics
            if modules["⭐ Rating Analytics"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>⭐ RATING ANALYTICS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_hist = create_premium_plotly_chart(
                        'histogram', data=df, x='avg_elo',
                        title="📈 Rating Distribution Analysis"
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    df_sorted = df.dropna(subset=['utcdate', 'avg_elo']).sort_values('utcdate')
                    if len(df_sorted) > 0:
                        fig_trend = create_premium_plotly_chart(
                            'line', data=df_sorted, x='utcdate', y='avg_elo',
                            title="📊 Rating Progression Over Time"
                        )
                        st.plotly_chart(fig_trend, use_container_width=True)
            
            # Game Termination Analysis
            if modules["🏁 Game Termination"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>🏁 GAME TERMINATION ANALYSIS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                termination_counts = df['termination'].value_counts().head(8)
                fig_term = create_premium_plotly_chart(
                    'bar', x=termination_counts.values, y=termination_counts.index,
                    title="🏁 How Games End - Termination Analysis"
                )
                fig_term.update_layout(yaxis=dict(categoryorder='total ascending'))
                st.plotly_chart(fig_term, use_container_width=True)
            
            # Opening Analysis
            if modules["♟️ Opening Mastery"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>♟️ OPENING MASTERY ANALYSIS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    eco_counts = df['eco'].value_counts().head(15)
                    fig_eco = create_premium_plotly_chart(
                        'bar', x=eco_counts.values, y=eco_counts.index,
                        title="♟️ Most Popular Opening ECO Codes"
                    )
                    fig_eco.update_layout(yaxis=dict(categoryorder='total ascending'))
                    st.plotly_chart(fig_eco, use_container_width=True)
                
                with col2:
                    fig_moves = create_premium_plotly_chart(
                        'histogram', data=df, x='num_moves',
                        title="📊 Game Length Distribution"
                    )
                    st.plotly_chart(fig_moves, use_container_width=True)
            
            # Player Analysis
            if modules["👑 Player Insights"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>👑 PLAYER PERFORMANCE INSIGHTS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    top_white = df['white'].value_counts().head(10)
                    fig_white = create_premium_plotly_chart(
                        'bar', x=top_white.values, y=top_white.index,
                        title="🤍 Most Active White Players"
                    )
                    fig_white.update_layout(yaxis=dict(categoryorder='total ascending'))
                    st.plotly_chart(fig_white, use_container_width=True)
                
                with col2:
                    top_black = df['black'].value_counts().head(10)
                    fig_black = create_premium_plotly_chart(
                        'bar', x=top_black.values, y=top_black.index,
                        title="⚫ Most Active Black Players"
                    )
                    fig_black.update_layout(yaxis=dict(categoryorder='total ascending'))
                    st.plotly_chart(fig_black, use_container_width=True)
            
            # Time Controls Analysis
            if modules["⏱️ Time Controls"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>⏱️ TIME CONTROL ANALYSIS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                time_controls = df['timecontrol'].value_counts().head(12)
                fig_time = create_premium_plotly_chart(
                    'bar', x=time_controls.values, y=time_controls.index,
                    title="⏱️ Most Popular Time Control Formats"
                )
                fig_time.update_layout(yaxis=dict(categoryorder='total ascending'))
                st.plotly_chart(fig_time, use_container_width=True)
            
            # Trend Analysis
            if modules["📈 Trend Analysis"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>📈 ADVANCED TREND ANALYSIS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Monthly game activity
                    monthly_games = df.groupby('month').size().reset_index()
                    monthly_games.columns = ['month', 'games']
                    monthly_games['month_str'] = monthly_games['month'].astype(str)
                    
                    fig_monthly = create_premium_plotly_chart(
                        'line', data=monthly_games, x='month_str', y='games',
                        title="📅 Monthly Gaming Activity Trends"
                    )
                    st.plotly_chart(fig_monthly, use_container_width=True)
                
                with col2:
                    # Rating vs Game Length scatter
                    sample_df = df.sample(min(1000, len(df))) if len(df) > 1000 else df
                    fig_scatter = create_premium_plotly_chart(
                        'scatter', data=sample_df, x='avg_elo', y='num_moves',
                        title="🎯 Rating vs Game Length Correlation"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Advanced Statistics
            if modules["🔬 Advanced Stats"]:
                st.markdown("""
                <div class="analysis-mastercard">
                    <h2>🔬 ADVANCED STATISTICAL ANALYSIS</h2>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Correlation heatmap
                    numeric_cols = ['whiteelo', 'blackelo', 'avg_elo', 'num_moves']
                    corr_matrix = df[numeric_cols].corr()
                    fig_corr = create_premium_plotly_chart(
                        'heatmap', data=corr_matrix,
                        title="🔥 Correlation Matrix - Performance Metrics"
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
                
                with col2:
                    # Event type distribution
                    event_counts = df['event'].value_counts().head(8)
                    fig_events = create_premium_plotly_chart(
                        'pie', x=event_counts.index, y=event_counts.values,
                        title="🏆 Game Event Type Distribution"
                    )
                    st.plotly_chart(fig_events, use_container_width=True)
                
                # Advanced metrics grid
                st.markdown("### 📊 Performance Metrics Deep Dive")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(create_animated_metric_card(
                        "Peak Rating", f"{df['avg_elo'].max():.0f}", "🏆"
                    ), unsafe_allow_html=True)
                
                with col2:
                    st.markdown(create_animated_metric_card(
                        "Rating Std Dev", f"{df['avg_elo'].std():.0f}", "📊"
                    ), unsafe_allow_html=True)
                
                with col3:
                    st.markdown(create_animated_metric_card(
                        "Longest Game", f"{df['num_moves'].max()}", "⏱️"
                    ), unsafe_allow_html=True)
                
                with col4:
                    st.markdown(create_animated_metric_card(
                        "Win Rate", f"{(len(df[df['winner'] != 'Draw']) / len(df) * 100):.1f}%", "🎯"
                    ), unsafe_allow_html=True)
                
                # Detailed statistics table
                st.markdown("### 📈 Comprehensive Statistics")
                
                stats_data = {
                    'Metric': [
                        'Total Games Played', 'Unique Opponents', 'Average Game Rating',
                        'Rating Standard Deviation', 'Games Won', 'Games Lost', 'Games Drawn',
                        'Shortest Game (moves)', 'Longest Game (moves)', 'Average Game Length',
                        'Most Common Opening', 'Most Common Time Control', 'Peak Performance Rating'
                    ],
                    'Value': [
                        f"{len(df):,}",
                        f"{len(set(df['white'].tolist() + df['black'].tolist())):,}",
                        f"{df['avg_elo'].mean():.1f}",
                        f"{df['avg_elo'].std():.1f}",
                        f"{len(df[df['winner'] == 'White']):,}",
                        f"{len(df[df['winner'] == 'Black']):,}",
                        f"{len(df[df['winner'] == 'Draw']):,}",
                        f"{df['num_moves'].min()}",
                        f"{df['num_moves'].max()}",
                        f"{df['num_moves'].mean():.1f}",
                        f"{df['eco'].mode().iloc[0] if len(df['eco'].mode()) > 0 else 'N/A'}",
                        f"{df['timecontrol'].mode().iloc[0] if len(df['timecontrol'].mode()) > 0 else 'N/A'}",
                        f"{df['avg_elo'].max():.0f}"
                    ]
                }
                
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    else:
        # Premium Welcome Screen
        st.markdown("""
        <div class="upload-masterzone">
            <h2>🚀 WELCOME TO THE FUTURE OF CHESS ANALYTICS</h2>
            <p style="font-size: 1.4rem; margin: 2rem 0; color: #ffffff; font-weight: 300;">
                Upload your Lichess games CSV to unlock professional-grade insights
            </p>
            
            <div style="margin: 3rem 0;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0;">
                    
                    <div style="background: rgba(129, 182, 76, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(129, 182, 76, 0.3);">
                        <h3 style="color: #81b64c; margin-bottom: 1rem;">🎯 Game Analysis</h3>
                        <p>Deep dive into win rates, game outcomes, and performance patterns</p>
                    </div>
                    
                    <div style="background: rgba(129, 182, 76, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(129, 182, 76, 0.3);">
                        <h3 style="color: #81b64c; margin-bottom: 1rem;">⭐ Rating Insights</h3>
                        <p>Track rating progression, distribution analysis, and trend identification</p>
                    </div>
                    
                    <div style="background: rgba(129, 182, 76, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(129, 182, 76, 0.3);">
                        <h3 style="color: #81b64c; margin-bottom: 1rem;">♟️ Opening Mastery</h3>
                        <p>Analyze your opening repertoire and identify improvement areas</p>
                    </div>
                    
                    <div style="background: rgba(129, 182, 76, 0.1); padding: 2rem; border-radius: 15px; border: 1px solid rgba(129, 182, 76, 0.3);">
                        <h3 style="color: #81b64c; margin-bottom: 1rem;">📊 Advanced Analytics</h3>
                        <p>Professional-grade statistics, correlations, and performance metrics</p>
                    </div>
                    
                </div>
            </div>
            
            <div style="margin: 3rem 0; padding: 2rem; background: rgba(26, 46, 26, 0.5); border-radius: 15px; border: 1px solid rgba(129, 182, 76, 0.2);">
                <h3 style="color: #81b64c; margin-bottom: 1.5rem;">📁 How to Get Your Data:</h3>
                <ol style="text-align: left; display: inline-block; color: #cccccc; font-size: 1.1rem; line-height: 1.8;">
                    <li>Visit <strong style="color: #81b64c;">lichess.org</strong> and log into your account</li>
                    <li>Navigate to your profile page</li>
                    <li>Click on <strong style="color: #81b64c;">"Download your games"</strong></li>
                    <li>Select <strong style="color: #81b64c;">CSV format</strong> for export</li>
                    <li>Upload the file using the sidebar panel ←</li>
                </ol>
            </div>
            
            <p style="color: #81b64c; font-weight: bold; font-size: 1.2rem; margin-top: 2rem;">
                ← Start by uploading your CSV file in the sidebar!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase
        st.markdown("""
        <div class="analysis-mastercard">
            <h2>🌟 PREMIUM FEATURES</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0;">
                
                <div style="padding: 1.5rem; background: rgba(129, 182, 76, 0.05); border-radius: 15px; border-left: 4px solid #81b64c;">
                    <h4 style="color: #81b64c; margin-bottom: 1rem;">🎨 Chess.com Theme</h4>
                    <p>Professional green and black interface inspired by chess.com design</p>
                </div>
                
                <div style="padding: 1.5rem; background: rgba(129, 182, 76, 0.05); border-radius: 15px; border-left: 4px solid #81b64c;">
                    <h4 style="color: #81b64c; margin-bottom: 1rem;">📊 Interactive Charts</h4>
                    <p>Premium Plotly visualizations with hover effects and smooth animations</p>
                </div>
                
                <div style="padding: 1.5rem; background: rgba(129, 182, 76, 0.05); border-radius: 15px; border-left: 4px solid #81b64c;">
                    <h4 style="color: #81b64c; margin-bottom: 1rem;">⚡ Real-time Analysis</h4>
                    <p>Instant processing and visualization of your chess game data</p>
                </div>
                
                <div style="padding: 1.5rem; background: rgba(129, 182, 76, 0.05); border-radius: 15px; border-left: 4px solid #81b64c;">
                    <h4 style="color: #81b64c; margin-bottom: 1rem;">🔍 Deep Insights</h4>
                    <p>Advanced statistical analysis and performance correlation studies</p>
                </div>
                
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Premium Footer
    st.markdown("""
    <div class="footer-master">
        <h3 style="color: #81b64c; font-family: 'Orbitron', monospace; margin-bottom: 1rem;">
            ♛ LICHESS CHESS ANALYTICS PRO ♛
        </h3>
        <p style="font-size: 1.1rem; margin-bottom: 1rem; color: #cccccc;">
            Elevate your chess game with professional-grade analytics
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap;">
            <span style="color: #81b64c;">🚀 Powered by AI</span>
            <span style="color: #81b64c;">📊 Real-time Analytics</span>
            <span style="color: #81b64c;">🎨 Premium Design</span>
            <span style="color: #81b64c;">⚡ Lightning Fast</span>
        </div>
        <p style="font-size: 0.9rem; opacity: 0.7; margin-top: 2rem;">
            Built with Streamlit • Plotly • Advanced Data Science
        </p>
        <div style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.5;">
            © 2024 Chess Analytics Pro - Professional Chess Performance Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()