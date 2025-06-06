import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import preprocessor, helper

# —————————— GLOBAL PAGE CONFIG & CSS ——————————
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📊",
    # layout="wide",
    # layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://example.com/help',
        'Report a bug': 'https://example.com/bug',
        'About': 'This app analyzes your WhatsApp chat data.'
    }
)
# Inject a bit of custom CSS for titles, cards, and spacing
st.markdown(
    """
    <style>
    /* Title styling */
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E4053;
        margin-bottom: 0.5rem;
    }
    /* Card containers for metrics */
    .metric-card {
        background-color: #F7F9F9;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    /* Sidebar section headers */
    .sidebar-header {
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    /* Styled gradient separator */
    .separator {
        height: 2px;  /* thickness of separator */
        background: linear-gradient(to right, #25d366, #00b56a);  /* WhatsApp-style green gradient */
        border: none;
        margin: 1rem 0;
        border-radius: 2px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# —————————— SIDEBAR ——————————

def load_sidebar():
    st.sidebar.markdown(
        """
        <style>
        /* WhatsApp-themed upload card */
        .upload-card {
            background: linear-gradient(135deg, #e6f9f0, #f0fdf6);
            border-radius: 14px;
            padding: 22px 20px;
            box-shadow: 0 4px 14px rgba(37, 211, 102, 0.18);
            margin-bottom: 25px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #1c2b2d;
            border: 1px solid #c4efd2;
        }

        .upload-card h2 {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 0 12px 0;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #128C7E;
        }

        .upload-card p {
            font-size: 0.95rem;
            margin-bottom: 15px;
            color: #444;
        }
        /* Dropdown styling */
        div[data-baseweb="select"] > div {
            border-radius: 10px !important;
            border: 2px solid #25d366 !important;
            background-color: #f7fff9 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #1c2b2d !important;
            padding: 6px 9px !important;
            margin-bottom: 8px;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            height: auto !important;
        }

        div[data-baseweb="select"]:hover > div {
            border-color: #00b56a !important;
            box-shadow: 0 0 8px rgba(0, 181, 106, 0.25);
        }

        /* Show Analysis Button */
        .stButton > button {
            background: linear-gradient(135deg, #25d366, #128c7e);
            border: none;
            border-radius: 14px;
            color: white;
            font-weight: 700;
            padding: 12px 0;
            width: 100%;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(37, 211, 102, 0.4);
            transition: background 0.3s ease;
            margin-bottom: 30px;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #00b56a, #0b6e56);
            box-shadow: 0 0 12px rgba(0, 181, 106, 0.7);
        }

        /* File Uploader container */
        .stFileUploader {
            background-color: #f7fff9;
            border: 1.5px solid #25d366;  /* slightly thinner border */
            border-radius: 7px;
            padding: 6px;  /* reduced from 10px */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 0.9rem;  /* smaller font size */
            margin-bottom: 10px;  /* less spacing below */
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }

        .stFileUploader:hover {
            border-color: #00b56a;
            box-shadow: 0 0 8px rgba(0, 181, 106, 0.25);
        }

        /* Browse files button inside uploader */
        .stFileUploader [data-testid="stFileUploadDropzone"] {
            border: none !important;
            padding: 6px 12px !important;  /* reduced padding */
            border-radius: 10px !important;
            background-color: #25d366 !important;
            color: white !important;
            text-align: center !important;
            font-weight: bold !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 0.9rem !important;  /* smaller font */
            transition: background 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 14px rgba(37, 211, 102, 0.4);
            cursor: pointer !important;
        }

        .stFileUploader [data-testid="stFileUploadDropzone"]:hover {
            background-color: #00b56a !important;
            box-shadow: 0 0 12px rgba(0, 181, 106, 0.7);
        }

        </style>

        <!-- Upload Section -->
        <div class="upload-card">
            <h2>📁 Upload Chat</h2>
            <p>Export your WhatsApp chat as a <strong>.txt</strong> file and upload it here to begin analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.sidebar.file_uploader(
        "📁",
        type=["txt"],
        help="Export your chat from WhatsApp and upload the .txt file here.",
        label_visibility="collapsed",
    )

    df = None
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        bytes_data = uploaded_file.getvalue().decode("utf-8")
        df = preprocessor.preprocessor(bytes_data)

        # Assuming df has a 'user' column to select from, else adapt this
        users = df['user'].unique().tolist() if df is not None else []

        selected_user = st.sidebar.selectbox(
            "Select User",
            options=["Overall"] + users,
            index=0,
            help="Select a user to analyze specific chat data."
        )

        show_analysis = st.sidebar.button("Show Analysis")

        if show_analysis:
            # You can return a tuple (df, selected_user, show_analysis)
            return df, selected_user, show_analysis

    return df, None, False


def add_footer():
    footer_html = """
    <style>
    .footer {
        position: fixed;
        left: 70%;
        bottom: 0;
        transform: translateX(-70%);
        max-width: 850px;
        width: 100%;
        background: linear-gradient(90deg, #e6f4ea, #d0f0dc);
        color: #1c2b2d;
        text-align: center;
        padding: 8px 10px 6px 10px;  /* ↓ reduced vertical padding */
        font-size: 13px;  /* ↓ slightly smaller text */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.07);
        z-index: 9999;
        border-top: 4px solid transparent;
        border-image: linear-gradient(to right, #25d366, #00b56a);
        border-image-slice: 1;
        border-radius: 6px 6px 0 0;
    }

    .footer p {
        margin: 2px 0;  /* ↓ less vertical space between lines */
    }

    .footer a {
        color: #128C7E;
        text-decoration: none;
        margin: 0 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .footer a:hover {
        color: #075E54;
        text-shadow: 0 0 6px rgba(37, 211, 102, 0.4);
    }

    .footer .credits {
        font-weight: bold;
        font-size: 13.5px;  /* ↓ slightly reduced */
    }

    .footer .social-links {
        margin-top: 2px;  /* ↓ reduce space between blocks */
        font-size: 13px;
    }

    .footer strong {
        color: #128C7E;
    }
    </style>

    <div class="footer">
        <p class="credits">🚀 <strong>Built with passion</strong> 💚 and care by 
            <a href="https://www.linkedin.com/in/suraj5424/" target="_blank" rel="noopener noreferrer">
                <strong>Suraj Varma</strong> 👨‍💻🌐
            </a>
        </p>
        <p class="social-links">
            Connect with me:
            <a href="https://github.com/suraj5424" target="_blank" rel="noopener noreferrer">🔗 <strong>GitHub</strong></a> |
            <a href="https://github.com/suraj5424?tab=repositories" target="_blank" rel="noopener noreferrer">🔗 <strong>LinkedIn</strong></a>
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


# # —————————— USER SELECTION ——————————
def select_user(df):
    st.sidebar.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-header">👤 Select User</div>', unsafe_allow_html=True)
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("", user_list)
    return selected_user

def show_analysis_button():
    st.sidebar.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    return st.sidebar.button("🚀 Show Analysis", use_container_width=True)

# —————————— TOP METRICS ——————————
def display_stats(selected_user, df):
    num_messages, words, media_messages, links = helper.fetch_stats(df, selected_user)
    st.markdown('<div class="title">🔍 Top-Level Stats</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("Total Messages")
        st.markdown(f"#### {num_messages}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("Total Words")
        st.markdown(f"#### {words}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("Media Shared")
        st.markdown(f"#### {media_messages}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("Links Shared")
        st.markdown(f"#### {links}")
        st.markdown('</div>', unsafe_allow_html=True)

# —————————— TIMELINES (MONTHLY & DAILY) ——————————
def plot_timeline(title, timeline, x_col, y_col, marker_color):
    fig = px.line(
        timeline, x=x_col, y=y_col, 
        title=title, 
        markers=True
    )
    fig.update_traces(marker=dict(size=6, color=marker_color))
    fig.update_layout(
        title_font_size=20,
        xaxis_title=x_col.capitalize(),
        yaxis_title='Messages',
        xaxis_tickangle=-45,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# —————————— ACTIVITY MAP ——————————
def plot_activity_map(selected_user, df):
    st.markdown('<div class="title">📅 Activity Overview</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Busy Days of Week")
        busy_day = helper.week_activity_map(selected_user, df)
        fig = go.Figure([go.Bar(x=busy_day.index, y=busy_day.values, marker_color='indigo')])
        fig.update_layout(
            xaxis_title='Day of Week',
            yaxis_title='Count',
            margin=dict(t=30, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Busy Months")
        busy_month = helper.month_activity_map(selected_user, df)
        fig = go.Figure([go.Bar(x=busy_month.index, y=busy_month.values, marker_color='crimson')])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Count',
            margin=dict(t=30, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

def plot_weekly_activity_heatmap(selected_user, df):
    st.subheader("Weekly Heatmap")
    heatmap_data = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(
        heatmap_data, 
        cmap="YlGnBu", 
        linewidths=0.5, 
        linecolor="white",
        annot=False,
        cbar_kws={'shrink': 0.5}
    )
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week")
    st.pyplot(fig)

# —————————— BUSY USERS (ONLY “Overall”) ——————————

def display_busy_users(df):
    st.markdown('<div class="title">👥 Most Active Participants</div>', unsafe_allow_html=True)
    x, new_df = helper.most_busy_users(df)  # x is a Series: index = usernames, values = counts

    # Matplotlib Chart (Perfect as is)
    st.subheader("Matplotlib Chart")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(x.index, x.values, color="#E74C3C")
    plt.xticks(rotation=45)
    ax.set_ylabel("**Message Count**")
    ax.set_title("Top Active Users")
    st.pyplot(fig)

    # Dataframe (Bottom)
    st.subheader("**User Rankings**")
    second_col = new_df.columns[1]
    st.dataframe(new_df.style.background_gradient(cmap="Blues", subset=[second_col]),use_container_width=True)

# —————————— WORDCLOUD & COMMON WORDS ——————————
def display_wordcloud(selected_user, df):
    if selected_user == 'group_notification':
        st.info("Wordcloud is not available for group notifications.")
        return

    st.markdown('<div class="title">☁️ Wordcloud</div>', unsafe_allow_html=True)
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(df_wc, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout()
    st.pyplot(fig)

def display_common_words(selected_user, df):
    if selected_user == 'group_notification':
        st.info("Common words analysis is not available for group notifications.")
        return

    st.markdown('<div class="title">📝 Most Common Words</div>', unsafe_allow_html=True)
    common_words_df = helper.most_common_words(selected_user, df)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(common_words_df[0], common_words_df[1], color="#3498DB")
    ax.set_ylabel("Words")
    ax.set_xlabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)


# —————————— EMOJI ANALYSIS ——————————
def display_emoji_analysis(selected_user, df):
    st.markdown('<div class="title">😀 Emoji Analysis</div>', unsafe_allow_html=True)
    emoji_df = helper.emoji_helper(selected_user, df)

    if not isinstance(emoji_df, pd.DataFrame):
        st.write(emoji_df)
    else:
        col1, col2 = st.columns((1, 1), gap="large")
        with col1:
            st.dataframe(emoji_df.style.set_caption("Top Emojis & Counts"),use_container_width=True)
        with col2:
            pie_fig = px.pie(
                names=emoji_df[0].head(5), 
                values=emoji_df[1].head(5), 
                title='Top 5 Emojis',
                hole=0.4
            )
            pie_fig.update_layout(
                margin=dict(t=30, b=20, l=20, r=20),
                legend=dict(orientation="h", y=-0.1)
            )
            st.plotly_chart(pie_fig, use_container_width=True)

# —————————— AVERAGES & HOURLY ACTIVITY ——————————
def display_avg_messages(selected_user, df):
    avg_per_day = helper.average_messages_per_day(selected_user, df)
    st.markdown('<div class="metric-card" style="margin-top:1rem;">', unsafe_allow_html=True)
    st.subheader("📈 Avg. Messages / Day")
    st.markdown(f"### {round(avg_per_day, 2)}")
    st.markdown('</div>', unsafe_allow_html=True)

def display_hourly_activity(selected_user, df):
    st.markdown('<div class="title">⏰ Hourly Activity</div>', unsafe_allow_html=True)
    hourly_df = helper.hourly_activity(selected_user, df)
    fig = go.Figure([go.Bar(x=hourly_df.index, y=hourly_df.values, marker_color='#1ABC9C')])
    fig.update_layout(
        xaxis_title='Hour',
        yaxis_title='Messages',
        margin=dict(t=30, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# —————————— DAY-OF-MONTH & LENGTH DISTRIBUTION ——————————
def plot_day_of_month_activity(selected_user, df):
    st.markdown('<div class="title">📅 Day of Month Activity</div>', unsafe_allow_html=True)
    df_day = helper.day_of_month_activity(selected_user, df)
    fig = go.Figure([go.Bar(x=df_day.index, y=df_day.values, marker_color='#8E44AD')])
    fig.update_layout(
        xaxis_title='Day of Month',
        yaxis_title='Messages',
        margin=dict(t=30, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def display_message_length_dist(selected_user, df):
    st.markdown('<div class="title">✍️ Message Length Distribution</div>', unsafe_allow_html=True)
    msg_len_df = helper.message_length_distribution(selected_user, df)
    fig = px.histogram(
        msg_len_df, 
        nbins=30, 
        title="Message Lengths (Number of Characters)"
    )
    fig.update_layout(
        margin=dict(t=30, b=20, l=20, r=20),
        xaxis_title="Length",
        yaxis_title="Frequency"
    )
    st.plotly_chart(fig, use_container_width=True)

# —————————— LEXICAL RICHNESS & SENTIMENT ——————————
def display_lexical_richness(selected_user, df):
    richness = helper.lexical_richness(selected_user, df)
    st.markdown('<div class="metric-card" style="margin-top:1rem;">', unsafe_allow_html=True)
    st.subheader("🧠 Lexical Richness")
    st.markdown(f"### {richness:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)


def display_sentiment_analysis(selected_user, df):
    st.markdown('<div class="title">💬 Sentiment Analysis</div>', unsafe_allow_html=True)
    sentiment_counts, sentiment_df = helper.sentiment_analysis(selected_user, df)

    # Pie chart section
    pie_fig = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title="Overall Sentiments",
        color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
    )
    pie_fig.update_layout(
        margin=dict(t=30, b=20, l=20, r=20),
        legend=dict(orientation="h", y=-0.1)
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    # DataFrame section
    st.markdown("**Detailed Sentiment Data**")
    st.dataframe(sentiment_df.style.highlight_max(axis=0, color="#A3E4D7"),use_container_width=True)


# —————————— MAIN ——————————
def main():
    st.markdown(
        """
        <style>
        /* Main Title */
        .custom-title {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            color: #27ae60 !important; /* rich green */
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.25) !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            margin-bottom: 0.1rem !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.6rem !important;
        }
        /* Subheader */
        .custom-subheader {
            font-size: 1.25rem !important;
            font-weight: 500 !important;
            color: #555555 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
        }
        /* Divider line */
        hr.custom-divider {
            height: 50px;
            background: linear-gradient(to right, #25d366, #00b56a);
            margin-top: 0.5rem;
            margin-bottom: 1rem;
            border: none;
            border-radius: 2px;
        }
        </style>

        <div>
            <h1 class="custom-title">📊 WhatsApp Chat Analyzer</h1>
            <h3 class="custom-subheader">Get insights from your WhatsApp conversations</h3>
            <hr class="custom-divider" />
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write('')

    # Unpack new load_sidebar signature (df, selected_user, show_analysis)
    df, selected_user, show_analysis = load_sidebar()

    if df is None:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://cdn.pixabay.com/photo/2015/08/03/13/58/whatsapp-873316_1280.png", width=100)
        with col2:
            st.info("To export a chat, open WhatsApp > Chat > More > Export Chat (without media)")
            st.markdown("*Note: This tool is more suitable for analyzing English conversations.*")

        st.markdown(
            """
            <style>
            .upload-instructions {
                background-color: #f9f9f9;
                padding: 0.5rem;
                border-left: 3px solid #27ae60;
                border-radius: 6px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin-bottom: 0.5rem;
                box-shadow: 1px 1px 2px rgba(0,0,0,0.02);
                font-size: 0.75rem;
            }
            .upload-instructions h4 {
                margin: 0 0 0.3rem 0;
                font-size: 0.85rem;
            }
            .upload-instructions ul {
                margin: 0.3rem 0;
                padding-left: 1rem;
            }
            .upload-instructions li {
                margin-bottom: 0.2rem;
            }
            .upload-instructions code {
                background: #eefaf0;
                color: #2d8659;
                padding: 0.15em 0.3em;
                border-radius: 3px;
                font-size: 0.75em;
            }
            .sample-format {
                background-color: #f4f4f4;
                padding: 0.4rem;
                border-radius: 4px;
                font-size: 0.75rem;
                font-family: monospace;
                color: #333;
                margin-top: 0.4rem;
            }
            </style>

            <div class="upload-instructions">
                <h4>📁 Upload Instructions:</h4>
                <ul>
                    <li>The uploaded file must <b>exactly match the required sample format</b>. You can use the <b>“Download Sample”</b> button to get the correct format.</li>
                    <li>Only <b>English-language content</b> is supported.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.sidebar.markdown(
            """
            <style>
            .upload-card {
                background: linear-gradient(135deg,  #e6f9f0, #f0fdf6);  /* soft yellow */
                border-radius: 14px;
                padding: 12px 15px;           /* reduced padding */
                box-shadow: 0 4px 14px rgba(37, 211, 102, 0.18);
                margin-bottom: 15px;          /* less margin */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #1c2b2d;
                border: 1px solid #c4efd2;
                max-width: 280px;             /* optional: limit max width */
            }

            .upload-card h2 {
                font-size: 1.2rem;            /* smaller font size */
                font-weight: 700;
                margin: 0 0 8px 0;            /* smaller margin */
                display: flex;
                align-items: center;
                gap: 8px;
                color: #128C7E;
            }

            .upload-card p {
                font-size: 0.85rem;           /* smaller paragraph font */
                margin-bottom: 10px;
                color: #444;
            }
            </style>

            <div class="upload-card">
                <h2>🔒 Privacy First!</h2>
                <p>Your chat is processed <em>securely and privately</em> — we take your privacy <strong>very seriously</strong>.</p>
                <p>⚠️ We <strong>never store</strong> your data or share it with anyone, so you can <strong>chat with confidence!</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add a clean download button below the formatted block
        col_centered = st.columns([1, 2, 1])
        with col_centered[1]:
            with open("sample_chat.txt", "rb") as file:
                st.download_button(
                    label="📥 Download Sample Chat File",
                    data=file,
                    file_name="sample_chat.txt",
                    mime="text/plain",
                    help="Download a properly formatted chat sample"
                )
        return


    custom_css = """
    <style>
    /* Change font size and font family of tab labels */
    .stTabs button[role="tab"] {
        font-size: 18px !important;
        font-weight: bold;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #075E54; /* WhatsApp green */
        background-color: #ECE5DD; /* WhatsApp light background */
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        border: none;
        margin-right: 5px;
        transition: background-color 0.3s, color 0.3s;
    }

    /* Change active tab color */
    .stTabs button[role="tab"][aria-selected="true"] {
        color: white;
        background-color: #25D366; /* WhatsApp bright green */

    }

    /* Hover effect on tabs */
    .stTabs button[role="tab"]:hover:not([aria-selected="true"]) {
        background-color: #D6E8E0;
        cursor: pointer;
    }

    /* Increase font size for all markdown texts inside tabs */
    .stTabs div[data-testid="stMarkdownContainer"] {
        font-size: 16px !important;
        font-family: 'Arial', sans-serif;
        color: #202C33; /* WhatsApp dark text */
    }

    /* Separator styling */
    .separator {
        margin: 20px 0;
        border-bottom: 2px solid #DDDCDC;
    }
    </style>
    """


    # Only show analysis if button clicked
    if show_analysis:
        st.markdown(custom_css, unsafe_allow_html=True)        
        display_stats(selected_user, df)

        tab1, tab2, tab3 = st.tabs(["Timeline & Activity", "Text Overview", "Extra Insights"])

        with tab1:
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
            plot_timeline(
                "Monthly Timeline",
                helper.monthly_timeline(selected_user, df),
                x_col='time', y_col='message',
                marker_color='#E74C3C'
            )
            plot_timeline(
                "Daily Timeline",
                helper.daily_timeline(selected_user, df),
                x_col='date', y_col='message',
                marker_color='#27AE60'
            )

            plot_activity_map(selected_user, df)
            plot_weekly_activity_heatmap(selected_user, df)           
            
            # Additional info for 'Overall' selection
            if selected_user == 'Overall':
                st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
                display_busy_users(df)

            # Optionally show message or skip logic for group notifications
            elif selected_user == 'group_notification':
                st.info("Group notifications are excluded from user-specific analysis.")

        with tab2:
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
            display_wordcloud(selected_user, df)
            display_common_words(selected_user, df)
            display_emoji_analysis(selected_user, df)

        with tab3:
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
            display_avg_messages(selected_user, df)
            display_hourly_activity(selected_user, df)
            plot_day_of_month_activity(selected_user, df)
            display_message_length_dist(selected_user, df)
            display_lexical_richness(selected_user, df)
            display_sentiment_analysis(selected_user, df)

    else:
        st.info("Upload a chat file and click 'Show Analysis' to view insights.")



if __name__ == "__main__":
    main()
    add_footer()

