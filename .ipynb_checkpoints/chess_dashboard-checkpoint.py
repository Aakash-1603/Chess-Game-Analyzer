import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="♔ Chess Analytics Dashboard",
    page_icon="♔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chess.com Color Palette
COLORS = {
    'white': '#FFFFFF',
    'medium_green': '#69923E',
    'dark_olive': '#4E7837',
    'charcoal': '#4B4847',
    'deep_black': '#2C2B29',
    'accent_gold': '#F7B801',
    'light_gray': '#F8F9FA',
    'success': '#69923E',
    'warning': '#F7B801',
    'danger': '#DC3545'
}

# Custom CSS with Chess.com styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {{
        background: linear-gradient(135deg, {COLORS['light_gray']} 0%, {COLORS['white']} 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {COLORS['light_gray']} 0%, {COLORS['white']} 100%);
    }}
    
    .chess-header {{
        background: linear-gradient(135deg, {COLORS['deep_black']} 0%, {COLORS['charcoal']} 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
    }}
    
    .chess-title {{
        color: {COLORS['white']};
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .chess-subtitle {{
        color: {COLORS['medium_green']};
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }}
    
    .developer-badge {{
        background: linear-gradient(135deg, {COLORS['medium_green']} 0%, {COLORS['dark_olive']} 100%);
        color: {COLORS['white']};
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
        box-shadow: 0 5px 15px rgba(105, 146, 62, 0.3);
    }}
    
    .metric-container {{
        background: {COLORS['white']};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-left: 4px solid {COLORS['medium_green']};
        margin: 1rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .metric-container:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .metric-title {{
        color: {COLORS['charcoal']};
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .metric-value {{
        color: {COLORS['deep_black']};
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .section-header {{
        background: linear-gradient(135deg, {COLORS['medium_green']} 0%, {COLORS['dark_olive']} 100%);
        color: {COLORS['white']};
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 5px 15px rgba(105, 146, 62, 0.2);
    }}
    
    .chess-piece {{
        font-size: 2rem;
        margin-right: 0.5rem;
    }}
    
    .sidebar .stSelectbox > label {{
        color: {COLORS['deep_black']} !important;
        font-weight: 600 !important;
    }}
    
    .stPlotlyChart {{
        background: {COLORS['white']};
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        padding: 1rem;
        margin: 1rem 0;
    }}
    
    .upload-section {{
        background: {COLORS['white']};
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed {COLORS['medium_green']};
        text-align: center;
        margin: 2rem 0;
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['medium_green']} 0%, {COLORS['dark_olive']} 100%);
        color: {COLORS['white']};
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(105, 146, 62, 0.3);
    }}
</style>
""", unsafe_allow_html=True)

file="games.csv"
def load_and_process_data(file):
    """Load and process chess data"""
    try:
        df = pd.read_csv(file)
        # Keep original column names but create lowercase versions for processing
        df.columns = df.columns.str.strip()
        
        # Create a mapping for your specific columns
        column_mapping = {
            'White': 'white',
            'Black': 'black', 
            'Result': 'result',
            'WhiteElo': 'whiteelo',
            'BlackElo': 'blackelo',
            'UTCDate': 'utcdate',
            'ECO': 'eco',
            'Termination': 'termination',
            'TimeControl': 'timecontrol',
            'Moves': 'moves'
        }
        
        # Rename columns to match expected format
        df = df.rename(columns=column_mapping)
        
        # Parse result column into winner
        def get_winner(result):
            if result == '1-0':
                return 'white'
            elif result == '0-1':
                return 'black'
            else:
                return 'draw'
        
        df['winner'] = df['result'].apply(get_winner)
        df['utcdate'] = pd.to_datetime(df['utcdate'], errors='coerce')
        
        # Convert Elo columns to numeric
        df['whiteelo'] = pd.to_numeric(df['whiteelo'], errors='coerce')
        df['blackelo'] = pd.to_numeric(df['blackelo'], errors='coerce')
        
        # Add computed columns
        df['avg_elo'] = (df['whiteelo'] + df['blackelo']) // 2
        df['num_moves'] = df['moves'].apply(lambda x: len(str(x).strip().split()) if pd.notna(x) else 0)
        
        return df
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def create_outcome_chart(df):
    """Create game outcome visualization"""
    outcomes = df['winner'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=outcomes.index,
            y=outcomes.values,
            marker_color=[COLORS['medium_green'], COLORS['charcoal'], COLORS['accent_gold']],
            text=outcomes.values,
            textposition='auto',
            textfont=dict(size=14, color='white', family='Inter')
        )
    ])
    
    fig.update_layout(
        title={
            'text': '🎯 Game Outcomes Distribution',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Inter', 'color': COLORS['deep_black']}
        },
        xaxis_title="Winner",
        yaxis_title="Number of Games",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['charcoal']),
        showlegend=False,
        height=400
    )
    
    return fig

def create_elo_trend_chart(df):
    """Create ELO trend over time"""
    df_sorted = df.sort_values('utcdate').dropna(subset=['utcdate', 'avg_elo'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_sorted['utcdate'],
        y=df_sorted['avg_elo'],
        mode='lines+markers',
        line=dict(color=COLORS['medium_green'], width=3),
        marker=dict(color=COLORS['dark_olive'], size=6),
        name='Average ELO',
        hovertemplate='<b>Date:</b> %{x}<br><b>Average ELO:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '📈 Average ELO Rating Trend Over Time',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Inter', 'color': COLORS['deep_black']}
        },
        xaxis_title="Date",
        yaxis_title="Average ELO Rating",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['charcoal']),
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_termination_chart(df):
    """Create termination analysis pie chart"""
    termination_counts = df['termination'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=termination_counts.index,
        values=termination_counts.values,
        marker_colors=[COLORS['medium_green'], COLORS['charcoal'], COLORS['accent_gold'], COLORS['dark_olive']],
        textinfo='label+percent',
        textfont=dict(size=12, family='Inter'),
        hovertemplate='<b>%{label}</b><br>Games: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '🏁 Game Termination Types',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Inter', 'color': COLORS['deep_black']}
        },
        font=dict(family='Inter', color=COLORS['charcoal']),
        height=400
    )
    
    return fig

def create_moves_distribution(df):
    """Create game length distribution"""
    fig = go.Figure(data=[go.Histogram(
        x=df['num_moves'],
        nbinsx=30,
        marker_color=COLORS['medium_green'],
        opacity=0.8,
        name='Number of Games'
    )])
    
    fig.update_layout(
        title={
            'text': '⚡ Game Length Distribution (Number of Moves)',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Inter', 'color': COLORS['deep_black']}
        },
        xaxis_title="Number of Moves",
        yaxis_title="Number of Games",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['charcoal']),
        height=400
    )
    
    return fig

def create_opening_chart(df):
    """Create most popular openings chart"""
    eco_counts = df['eco'].value_counts().head(10)
    
    fig = go.Figure(data=[
        go.Bar(
            x=eco_counts.values,
            y=eco_counts.index,
            orientation='h',
            marker_color=COLORS['medium_green'],
            text=eco_counts.values,
            textposition='auto',
            textfont=dict(color='white', family='Inter')
        )
    ])
    
    fig.update_layout(
        title={
            'text': '♟️ Most Popular Chess Openings (ECO Codes)',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Inter', 'color': COLORS['deep_black']}
        },
        xaxis_title="Number of Games",
        yaxis_title="ECO Code",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['charcoal']),
        height=500
    )
    
    return fig

def create_time_control_chart(df):
    """Create time control analysis"""
    time_controls = df['timecontrol'].value_counts().head(8)
    
    fig = go.Figure(data=[
        go.Bar(
            x=time_controls.index,
            y=time_controls.values,
            marker_color=COLORS['dark_olive'],
            text=time_controls.values,
            textposition='auto',
            textfont=dict(color='white', family='Inter')
        )
    ])
    
    fig.update_layout(
        title={
            'text': '⏱️ Most Popular Time Controls',
            'x': 0.5,
            'font': {'size': 20, 'family': 'Inter', 'color': COLORS['deep_black']}
        },
        xaxis_title="Time Control",
        yaxis_title="Number of Games",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['charcoal']),
        xaxis={'tickangle': 45},
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown("""
    <div class="chess-header">
        <h1 class="chess-title">♔ Chess Analytics Dashboard</h1>
        <p class="chess-subtitle">Professional Chess Game Analysis & Statistics</p>
        <div class="developer-badge">👨‍💻 Developed by: aaksh1234</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="background: {COLORS['deep_black']}; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h3 style="color: {COLORS['white']}; text-align: center; margin: 0;">
                ♔ Chess Analytics
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📁 Upload Your Chess Data")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload your chess games CSV file for analysis"
        )
        
        if uploaded_file:
            st.success("✅ File uploaded successfully!")
        
        st.markdown("---")
        st.markdown("### 🎮 Analysis Features")
        st.markdown("""
        - 🎯 Game Outcomes Analysis
        - 📈 ELO Rating Trends
        - 🏁 Termination Types
        - ⚡ Game Length Distribution
        - ♟️ Opening Popularity
        - ⏱️ Time Control Analysis
        - 📊 Statistical Overview
        """)
    
    # Main content
    if uploaded_file is not None:
        with st.spinner('🔄 Processing your chess data...'):
            df = load_and_process_data(uploaded_file)
        
        if df is not None:
            # Key Metrics Row
            st.markdown('<div class="section-header">📊 Key Statistics Overview</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">🎮 Total Games</div>
                    <div class="metric-value">{len(df):,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                avg_elo = df['avg_elo'].mean()
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">📈 Average ELO</div>
                    <div class="metric-value">{avg_elo:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg_moves = df['num_moves'].mean()
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">⚡ Avg Moves</div>
                    <div class="metric-value">{avg_moves:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                unique_players = len(set(df['white'].unique()) | set(df['black'].unique()))
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">👥 Unique Players</div>
                    <div class="metric-value">{unique_players:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Charts Section
            st.markdown('<div class="section-header">📊 Detailed Analysis</div>', unsafe_allow_html=True)
            
            # Row 1: Outcomes and ELO Trend
            col1, col2 = st.columns(2)
            with col1:
                fig_outcomes = create_outcome_chart(df)
                st.plotly_chart(fig_outcomes, use_container_width=True)
            
            with col2:
                fig_elo = create_elo_trend_chart(df)
                st.plotly_chart(fig_elo, use_container_width=True)
            
            # Row 2: Termination and Game Length
            col1, col2 = st.columns(2)
            with col1:
                fig_termination = create_termination_chart(df)
                st.plotly_chart(fig_termination, use_container_width=True)
            
            with col2:
                fig_moves = create_moves_distribution(df)
                st.plotly_chart(fig_moves, use_container_width=True)
            
            # Row 3: Openings and Time Controls
            col1, col2 = st.columns(2)
            with col1:
                fig_openings = create_opening_chart(df)
                st.plotly_chart(fig_openings, use_container_width=True)
            
            with col2:
                fig_time = create_time_control_chart(df)
                st.plotly_chart(fig_time, use_container_width=True)
            
            # Advanced Analytics Section
            st.markdown('<div class="section-header">🔍 Advanced Analytics</div>', unsafe_allow_html=True)
            
            # Win Rate Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                win_rates = df['winner'].value_counts(normalize=True) * 100
                
                fig_winrate = go.Figure(data=[
                    go.Bar(
                        x=win_rates.index,
                        y=win_rates.values,
                        marker_color=[COLORS['medium_green'], COLORS['charcoal'], COLORS['accent_gold']],
                        text=[f'{rate:.1f}%' for rate in win_rates.values],
                        textposition='auto',
                        textfont=dict(size=14, color='white', family='Inter')
                    )
                ])
                
                fig_winrate.update_layout(
                    title={
                        'text': '🏆 Win Rate Distribution',
                        'x': 0.5,
                        'font': {'size': 18, 'family': 'Inter', 'color': COLORS['deep_black']}
                    },
                    xaxis_title="Result",
                    yaxis_title="Percentage (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', color=COLORS['charcoal']),
                    height=400
                )
                
                st.plotly_chart(fig_winrate, use_container_width=True)
            
            with col2:
                # Monthly activity
                if 'utcdate' in df.columns and df['utcdate'].notna().any():
                    df['month'] = df['utcdate'].dt.to_period('M')
                    monthly_games = df.groupby('month').size().reset_index(name='games')
                    monthly_games['month_str'] = monthly_games['month'].astype(str)
                    
                    fig_monthly = go.Figure(data=[
                        go.Scatter(
                            x=monthly_games['month_str'],
                            y=monthly_games['games'],
                            mode='lines+markers',
                            line=dict(color=COLORS['dark_olive'], width=3),
                            marker=dict(color=COLORS['medium_green'], size=8),
                            name='Games per Month'
                        )
                    ])
                    
                    fig_monthly.update_layout(
                        title={
                            'text': '📅 Monthly Game Activity',
                            'x': 0.5,
                            'font': {'size': 18, 'family': 'Inter', 'color': COLORS['deep_black']}
                        },
                        xaxis_title="Month",
                        yaxis_title="Games Played",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family='Inter', color=COLORS['charcoal']),
                        xaxis={'tickangle': 45},
                        height=400
                    )
                    
                    st.plotly_chart(fig_monthly, use_container_width=True)
            
            # Data Table Section
            st.markdown('<div class="section-header">📋 Raw Data Preview</div>', unsafe_allow_html=True)
            
            # Display first few rows of data
            st.dataframe(
                df.head(10),
                use_container_width=True,
                height=300
            )
            
            # Download processed data
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Processed Data",
                data=csv,
                file_name=f"chess_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        else:
            st.error("❌ Failed to process the uploaded file. Please check the file format.")
    
    else:
        # Welcome message
        st.markdown(f"""
        <div class="upload-section">
            <h2 style="color: {COLORS['deep_black']}; margin-bottom: 1rem;">
                🚀 Welcome to Chess Analytics Dashboard
            </h2>
            <p style="color: {COLORS['charcoal']}; font-size: 1.1rem; margin-bottom: 2rem;">
                Upload your chess games CSV file to start analyzing your performance and discover insights about your games.
            </p>
            <div style="background: {COLORS['light_gray']}; padding: 1rem; border-radius: 8px; margin-top: 2rem;">
                <h4 style="color: {COLORS['deep_black']}; margin-bottom: 0.5rem;">📋 Expected CSV Format:</h4>
                <p style="color: {COLORS['charcoal']}; margin: 0; text-align: left;">
                    • <strong>Required columns:</strong> white, black, result, whiteelo, blackelo, eco, termination, timecontrol, utcdate, moves<br>
                    • <strong>Result format:</strong> 1-0 (White wins), 0-1 (Black wins), 1/2-1/2 (Draw)<br>
                    • <strong>Date format:</strong> YYYY-MM-DD or similar standard format
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; color: {COLORS['charcoal']};">
        <p>♔ Chess Analytics Dashboard | Created with ❤️ by <strong>aaksh1234</strong></p>
        <p><em>Analyzing chess games to unlock strategic insights</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()