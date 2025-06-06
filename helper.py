from urlextract import URLExtract
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from PIL import Image, ImageDraw
import emoji

extractor = URLExtract()
analyzer = SentimentIntensityAnalyzer()

def fetch_stats(df, selected_user):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = [word for message in df['message'] for word in message.split()]
    media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    links = [url for message in df['message'] for url in extractor.find_urls(message)]

    return num_messages, len(words), media_messages, len(links)

def most_busy_users(df):
    top_users = df['user'].value_counts().head()
    user_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2)
    user_percent_df = user_percent.reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return top_users, user_percent_df

def create_wordcloud(selected_user, df):
    # Load stop words
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    # Remove system messages and media
    df = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]

    # Remove stop words
    def remove_stop_words(message):
        words = message.lower().split()
        return " ".join([word for word in words if word not in stop_words])

    df['cleaned_message'] = df['message'].apply(remove_stop_words)

    # First check before user filter
    all_text = " ".join(df['cleaned_message'])
    if len(all_text.split()) < 5:
        return create_placeholder_image("Not enough total words")

    # Filter by user if needed
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        all_text = " ".join(df['cleaned_message'])
        if len(all_text.split()) < 5:
            return create_placeholder_image(f"No significant words used by {selected_user}")

    # Generate word cloud
    try:
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        img = wc.generate(all_text).to_image()
        return img
    except ValueError:
        return create_placeholder_image("Error: No valid words")

# Helper function to create a placeholder image
def create_placeholder_image(text):
    img = Image.new('RGB', (500, 500), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((30, 230), text, fill='black')
    return img

def most_common_words(selected_user, df):
    stop_words = open('stop_hinglish.txt', 'r').read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]
    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words]

    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = [char for message in df['message'] for char in message if char in emoji.EMOJI_DATA]

    if len(emojis) == 0:
        text = f"{selected_user} didn't send any emojis."
        return text

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('date').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

def average_messages_per_day(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    daily_count = df.groupby('date').count()['message']
    return daily_count.mean()

def hourly_activity(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    return df['hour'].value_counts().sort_index()

def message_length_distribution(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    df['message_length'] = df['message'].apply(len)
    return df['message_length']

def day_of_month_activity(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    return df['date'].dt.day.value_counts().sort_index()

def lexical_richness(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    total_words = df['message'].apply(lambda x: len(x.split())).sum()
    unique_words = df['message'].apply(lambda x: len(set(x.split()))).sum()
    return unique_words / total_words if total_words else 0

def day_of_month_activity(user, df):
    if user != "Overall":
        df = df[df['user'] == user]
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])
    return df['date'].dt.day.value_counts().sort_index()

def sentiment_analysis(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    def get_sentiment(text):
        score = analyzer.polarity_scores(text)
        if score['compound'] >= 0.05:
            return 'Positive'
        elif score['compound'] <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    df['Sentiment'] = df['message'].apply(get_sentiment)
    sentiment_counts = df['Sentiment'].value_counts()
    return sentiment_counts, df[['user', 'message', 'Sentiment']]


