# WhatsApp Chat Analyzer 🖊️

A **Streamlit-based web app** for visualizing and analyzing WhatsApp chat exports. Upload your `.txt` chat file and explore rich insights like user activity, sentiment, word usage, and more.

---

## 📷 App Preview

> **Add a screenshot or GIF of your app UI here**
>
> ![App Screenshot](https://github.com/suraj5424/Whatsapp-Chat-analyser/blob/main/whatsaap_ui.jpeg)

---

## 📚 Features

* Chat statistics: total messages, words, media, links
* Most active users and their contributions
* Word cloud and most common words (with Hinglish stopword filtering)
* Emoji usage analysis
* Daily, monthly, and hourly activity trends
* Heatmaps, timelines, and period-based message analysis
* Sentiment analysis (positive/negative/neutral)
* Lexical richness and message length distribution

---

## 👨‍💻 How It Works

### 1. **Preprocessing (`processor.py`)**

* Parses raw WhatsApp chat exports (`.txt`)
* Extracts:

  * Date & time
  * Usernames
  * Messages
* Enriches data with:

  * Year, month, day, weekday, hour
  * Period bins (e.g. "14-15")

### 2. **Analysis Helpers (`helper.py`)**

* Calculates statistics (messages, words, links, etc.)
* Builds visual insights:

  * WordClouds (filtered with `stop_hinglish.txt`)
  * Activity heatmaps & timelines
  * Emoji and sentiment analysis
  * Lexical richness and message length

### 3. **App Interface (`app.py`)**

* Streamlit UI to upload `.txt` files and interact with analysis tools
* User selector: Overall or individual chat participants
* Displays visualizations and tables interactively

---

## 📂 File Structure

```
├── app.py                  # Streamlit app interface
├── helper.py               # Analysis and visualization logic
├── processor.py            # Chat preprocessing logic
├── stop_hinglish.txt       # Stopwords list (Hinglish)
├── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.7+

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Export WhatsApp chat

1. Go to the WhatsApp chat
2. Tap **Export Chat** (without media)
3. Upload the `.txt` file to the app

---

## 🌐 Deployment

You can deploy this app on **Streamlit Cloud**:

1. Push this repository to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo and select `app.py` as the entry point

---

## 📊 Tech Stack

* Python
* Streamlit
* Pandas
* WordCloud
* VADER Sentiment
* Pillow
* Emoji

---

## 🎓 Credits

Built with love by \[Your Name or GitHub Username]

---

## ⚖️ License

[MIT License](LICENSE)
