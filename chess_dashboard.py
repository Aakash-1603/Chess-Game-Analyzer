import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

# Page config
st.set_page_config(
    page_title="♔ Chess Analytics Dashboard",
    page_icon="♔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #6c63ff;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        color: #262730;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Load and process data function
@st.cache_data
def load_and_process_data():
    """Load and process chess data. In real app, replace with actual file loading."""
    # Generate sample data for demonstration
    np.random.seed(42)
    n_games = 1000
    
    data = {
        'result': np.random.choice(['1-0', '0-1', '1/2-1/2'], n_games, p=[0.45, 0.38, 0.17]),
        'whiteelo': np.random.normal(1500, 200, n_games).astype(int),
        'blackelo': np.random.normal(1500, 200, n_games).astype(int),
        'termination': np.random.choice(['Normal', 'Time forfeit', 'Abandoned', 'Resignation'], 
                                       n_games, p=[0.45, 0.25, 0.15, 0.15]),
        'eco': np.random.choice(['B06', 'C20', 'A40', 'D00', 'E00', 'B07', 'C21'], n_games),
        'white': [f'Player{i}' for i in np.random.randint(1, 200, n_games)],
        'black': [f'Player{i}' for i in np.random.randint(1, 200, n_games)],
        'timecontrol': np.random.choice(['600+0', '300+3', '180+0', '900+10'], n_games),
        'utcdate': pd.date_range('2024-01-01', '2024-12-01', periods=n_games),
        'moves': [' '.join([f'{i}.' for i in range(1, np.random.randint(20, 80))]) for _ in range(n_games)]
    }
    
    df = pd.DataFrame(data)
    
    # Process data same as original code
    def get_winner(result):
        if result == '1-0':
            return 'white'
        elif result == '0-1':
            return 'black'
        else:
            return 'draw'
    
    df['winner'] = df['result'].apply(get_winner)
    df['avg_elo'] = (df['whiteelo'] + df['blackelo']) // 2
    df['num_moves'] = df['moves'].apply(lambda x: len(str(x).strip().split()))
    df['month'] = df['utcdate'].dt.to_period('M')
    
    return df

def main():
    # Header
    st.markdown('<h1 class="main-header">♔ Chess Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Comprehensive analysis of your chess game data</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading chess data...'):
        df = load_and_process_data()
    
    # Sidebar filters
    st.sidebar.header("🎛️ Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['utcdate'].min().date(), df['utcdate'].max().date()),
        min_value=df['utcdate'].min().date(),
        max_value=df['utcdate'].max().date()
    )
    
    # ELO range filter
    elo_range = st.sidebar.slider(
        "Average ELO Range",
        min_value=int(df['avg_elo'].min()),
        max_value=int(df['avg_elo'].max()),
        value=(int(df['avg_elo'].min()), int(df['avg_elo'].max()))
    )
    
    # Filter data
    mask = (
        (df['utcdate'].dt.date >= date_range[0]) & 
        (df['utcdate'].dt.date <= date_range[1]) &
        (df['avg_elo'] >= elo_range[0]) & 
        (df['avg_elo'] <= elo_range[1])
    )
    filtered_df = df[mask]
    
    # Key metrics
    st.subheader("📊 Key Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Games", len(filtered_df))
    with col2:
        st.metric("Average ELO", f"{filtered_df['avg_elo'].mean():.0f}")
    with col3:
        st.metric("Avg Moves", f"{filtered_df['num_moves'].mean():.0f}")
    with col4:
        white_wins = (filtered_df['winner'] == 'white').sum()
        win_rate = white_wins / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric("White Win %", f"{win_rate:.1f}%")
    with col5:
        unique_openings = filtered_df['eco'].nunique()
        st.metric("Unique Openings", unique_openings)
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Game Outcomes", "📈 Trends", "♟️ Openings", "⏱️ Time & Performance"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Game outcomes pie chart
            outcomes = filtered_df['winner'].value_counts()
            colors = {'white': '#91C788', 'black': '#F3722C', 'draw': '#6C757D'}
            
            fig = px.pie(
                values=outcomes.values,
                names=outcomes.index.str.title(),
                title="Game Outcome Distribution",
                color_discrete_map={'White': colors['white'], 'Black': colors['black'], 'Draw': colors['draw']}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=True, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Win rate by color bar chart
            win_white = len(filtered_df[filtered_df['winner'] == 'white'])
            win_black = len(filtered_df[filtered_df['winner'] == 'black'])
            draws = len(filtered_df[filtered_df['winner'] == 'draw'])
            total = len(filtered_df)
            
            if total > 0:
                percentages = [win_white/total*100, win_black/total*100, draws/total*100]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=['White Wins', 'Black Wins', 'Draws'],
                        y=percentages,
                        marker_color=[colors['white'], colors['black'], colors['draw']],
                        text=[f'{p:.1f}%' for p in percentages],
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    title="Win Rate by Color",
                    yaxis_title="Percentage (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Termination analysis
        st.subheader("🏁 Game Termination Analysis")
        termination_counts = filtered_df['termination'].value_counts()
        
        fig = px.pie(
            values=termination_counts.values,
            names=termination_counts.index,
            title="Game Termination Types"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # ELO trend over time
            df_sorted = filtered_df.sort_values('utcdate')
            fig = px.line(
                df_sorted, x='utcdate', y='avg_elo',
                title='Average ELO Over Time',
                labels={'utcdate': 'Date', 'avg_elo': 'Average ELO'}
            )
            fig.update_traces(line_color='#6c63ff', line_width=3)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Monthly game activity
            monthly_games = filtered_df.groupby('month').size()
            
            fig = px.bar(
                x=monthly_games.index.astype(str),
                y=monthly_games.values,
                title='Monthly Game Activity',
                labels={'x': 'Month', 'y': 'Games Played'}
            )
            fig.update_traces(marker_color='rgba(108, 99, 255, 0.7)')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Game length distribution
        st.subheader("📏 Game Length Analysis")
        fig = px.histogram(
            filtered_df, x='num_moves',
            title='Game Length Distribution (by Moves)',
            nbins=30,
            labels={'num_moves': 'Number of Moves', 'count': 'Games'}
        )
        fig.update_traces(marker_color='rgba(147, 51, 234, 0.7)')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Most used openings
            eco_counts = filtered_df['eco'].value_counts().head(10)
            
            fig = px.bar(
                x=eco_counts.index,
                y=eco_counts.values,
                title='Most Frequent Openings (ECO Codes)',
                labels={'x': 'ECO Code', 'y': 'Games'}
            )
            fig.update_traces(marker_color='orange')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Win rate by opening
            opening_stats = filtered_df.groupby('eco').agg({
                'winner': lambda x: (x == 'white').sum() / len(x) * 100 if len(x) > 0 else 0,
                'eco': 'count'
            }).rename(columns={'winner': 'white_win_rate', 'eco': 'game_count'})
            
            # Filter openings with at least 10 games
            popular_openings = opening_stats[opening_stats['game_count'] >= 10].head(10)
            
            if not popular_openings.empty:
                fig = px.scatter(
                    popular_openings,
                    x='game_count',
                    y='white_win_rate',
                    hover_name=popular_openings.index,
                    title='Opening Performance (Min 10 Games)',
                    labels={'game_count': 'Games Played', 'white_win_rate': 'White Win Rate (%)'}
                )
                fig.update_traces(marker_size=12, marker_color='teal')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Time controls
            time_controls = filtered_df['timecontrol'].value_counts().head(8)
            
            fig = px.bar(
                x=time_controls.values,
                y=time_controls.index,
                orientation='h',
                title='Most Used Time Controls',
                labels={'x': 'Games', 'y': 'Time Control'}
            )
            fig.update_traces(marker_color='teal')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ELO distribution
            fig = px.histogram(
                filtered_df, x='avg_elo',
                title='Average ELO Distribution',
                nbins=30,
                labels={'avg_elo': 'Average ELO', 'count': 'Games'}
            )
            fig.update_traces(marker_color='rgba(52, 152, 219, 0.7)')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("📊 Correlation Matrix")
        numeric_cols = ['whiteelo', 'blackelo', 'avg_elo', 'num_moves']
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Between Numeric Variables",
            color_continuous_scale='RdBu_r'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
            <p>♔ Chess Analytics Dashboard | Built with Streamlit & Plotly</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

# Page config
st.set_page_config(
    page_title="♔ Chess Analytics Dashboard",
    page_icon="♔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #6c63ff;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        color: #262730;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Load and process data function
@st.cache_data
def load_and_process_data():
    """Load and process chess data. In real app, replace with actual file loading."""
    # Generate sample data for demonstration
    np.random.seed(42)
    n_games = 1000
    
    data = {
        'result': np.random.choice(['1-0', '0-1', '1/2-1/2'], n_games, p=[0.45, 0.38, 0.17]),
        'whiteelo': np.random.normal(1500, 200, n_games).astype(int),
        'blackelo': np.random.normal(1500, 200, n_games).astype(int),
        'termination': np.random.choice(['Normal', 'Time forfeit', 'Abandoned', 'Resignation'], 
                                       n_games, p=[0.45, 0.25, 0.15, 0.15]),
        'eco': np.random.choice(['B06', 'C20', 'A40', 'D00', 'E00', 'B07', 'C21'], n_games),
        'white': [f'Player{i}' for i in np.random.randint(1, 200, n_games)],
        'black': [f'Player{i}' for i in np.random.randint(1, 200, n_games)],
        'timecontrol': np.random.choice(['600+0', '300+3', '180+0', '900+10'], n_games),
        'utcdate': pd.date_range('2024-01-01', '2024-12-01', periods=n_games),
        'moves': [' '.join([f'{i}.' for i in range(1, np.random.randint(20, 80))]) for _ in range(n_games)]
    }
    
    df = pd.DataFrame(data)
    
    # Process data same as original code
    def get_winner(result):
        if result == '1-0':
            return 'white'
        elif result == '0-1':
            return 'black'
        else:
            return 'draw'
    
    df['winner'] = df['result'].apply(get_winner)
    df['avg_elo'] = (df['whiteelo'] + df['blackelo']) // 2
    df['num_moves'] = df['moves'].apply(lambda x: len(str(x).strip().split()))
    df['month'] = df['utcdate'].dt.to_period('M')
    
    return df

def main():
    # Header
    st.markdown('<h1 class="main-header">♔ Chess Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Comprehensive analysis of your chess game data</p>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading chess data...'):
        df = load_and_process_data()
    
    # Sidebar filters
    st.sidebar.header("🎛️ Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['utcdate'].min().date(), df['utcdate'].max().date()),
        min_value=df['utcdate'].min().date(),
        max_value=df['utcdate'].max().date()
    )
    
    # ELO range filter
    elo_range = st.sidebar.slider(
        "Average ELO Range",
        min_value=int(df['avg_elo'].min()),
        max_value=int(df['avg_elo'].max()),
        value=(int(df['avg_elo'].min()), int(df['avg_elo'].max()))
    )
    
    # Filter data
    mask = (
        (df['utcdate'].dt.date >= date_range[0]) & 
        (df['utcdate'].dt.date <= date_range[1]) &
        (df['avg_elo'] >= elo_range[0]) & 
        (df['avg_elo'] <= elo_range[1])
    )
    filtered_df = df[mask]
    
    # Key metrics
    st.subheader("📊 Key Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Games", len(filtered_df))
    with col2:
        st.metric("Average ELO", f"{filtered_df['avg_elo'].mean():.0f}")
    with col3:
        st.metric("Avg Moves", f"{filtered_df['num_moves'].mean():.0f}")
    with col4:
        white_wins = (filtered_df['winner'] == 'white').sum()
        win_rate = white_wins / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric("White Win %", f"{win_rate:.1f}%")
    with col5:
        unique_openings = filtered_df['eco'].nunique()
        st.metric("Unique Openings", unique_openings)
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Game Outcomes", "📈 Trends", "♟️ Openings", "⏱️ Time & Performance"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Game outcomes pie chart
            outcomes = filtered_df['winner'].value_counts()
            colors = {'white': '#91C788', 'black': '#F3722C', 'draw': '#6C757D'}
            
            fig = px.pie(
                values=outcomes.values,
                names=outcomes.index.str.title(),
                title="Game Outcome Distribution",
                color_discrete_map={'White': colors['white'], 'Black': colors['black'], 'Draw': colors['draw']}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=True, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Win rate by color bar chart
            win_white = len(filtered_df[filtered_df['winner'] == 'white'])
            win_black = len(filtered_df[filtered_df['winner'] == 'black'])
            draws = len(filtered_df[filtered_df['winner'] == 'draw'])
            total = len(filtered_df)
            
            if total > 0:
                percentages = [win_white/total*100, win_black/total*100, draws/total*100]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=['White Wins', 'Black Wins', 'Draws'],
                        y=percentages,
                        marker_color=[colors['white'], colors['black'], colors['draw']],
                        text=[f'{p:.1f}%' for p in percentages],
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    title="Win Rate by Color",
                    yaxis_title="Percentage (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Termination analysis
        st.subheader("🏁 Game Termination Analysis")
        termination_counts = filtered_df['termination'].value_counts()
        
        fig = px.pie(
            values=termination_counts.values,
            names=termination_counts.index,
            title="Game Termination Types"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # ELO trend over time
            df_sorted = filtered_df.sort_values('utcdate')
            fig = px.line(
                df_sorted, x='utcdate', y='avg_elo',
                title='Average ELO Over Time',
                labels={'utcdate': 'Date', 'avg_elo': 'Average ELO'}
            )
            fig.update_traces(line_color='#6c63ff', line_width=3)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Monthly game activity
            monthly_games = filtered_df.groupby('month').size()
            
            fig = px.bar(
                x=monthly_games.index.astype(str),
                y=monthly_games.values,
                title='Monthly Game Activity',
                labels={'x': 'Month', 'y': 'Games Played'}
            )
            fig.update_traces(marker_color='rgba(108, 99, 255, 0.7)')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Game length distribution
        st.subheader("📏 Game Length Analysis")
        fig = px.histogram(
            filtered_df, x='num_moves',
            title='Game Length Distribution (by Moves)',
            nbins=30,
            labels={'num_moves': 'Number of Moves', 'count': 'Games'}
        )
        fig.update_traces(marker_color='rgba(147, 51, 234, 0.7)')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Most used openings
            eco_counts = filtered_df['eco'].value_counts().head(10)
            
            fig = px.bar(
                x=eco_counts.index,
                y=eco_counts.values,
                title='Most Frequent Openings (ECO Codes)',
                labels={'x': 'ECO Code', 'y': 'Games'}
            )
            fig.update_traces(marker_color='orange')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Win rate by opening
            opening_stats = filtered_df.groupby('eco').agg({
                'winner': lambda x: (x == 'white').sum() / len(x) * 100 if len(x) > 0 else 0,
                'eco': 'count'
            }).rename(columns={'winner': 'white_win_rate', 'eco': 'game_count'})
            
            # Filter openings with at least 10 games
            popular_openings = opening_stats[opening_stats['game_count'] >= 10].head(10)
            
            if not popular_openings.empty:
                fig = px.scatter(
                    popular_openings,
                    x='game_count',
                    y='white_win_rate',
                    hover_name=popular_openings.index,
                    title='Opening Performance (Min 10 Games)',
                    labels={'game_count': 'Games Played', 'white_win_rate': 'White Win Rate (%)'}
                )
                fig.update_traces(marker_size=12, marker_color='teal')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Time controls
            time_controls = filtered_df['timecontrol'].value_counts().head(8)
            
            fig = px.bar(
                x=time_controls.values,
                y=time_controls.index,
                orientation='h',
                title='Most Used Time Controls',
                labels={'x': 'Games', 'y': 'Time Control'}
            )
            fig.update_traces(marker_color='teal')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ELO distribution
            fig = px.histogram(
                filtered_df, x='avg_elo',
                title='Average ELO Distribution',
                nbins=30,
                labels={'avg_elo': 'Average ELO', 'count': 'Games'}
            )
            fig.update_traces(marker_color='rgba(52, 152, 219, 0.7)')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("📊 Correlation Matrix")
        numeric_cols = ['whiteelo', 'blackelo', 'avg_elo', 'num_moves']
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Between Numeric Variables",
            color_continuous_scale='RdBu_r'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
            <p>♔ Chess Analytics Dashboard | Built with Streamlit & Plotly</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()