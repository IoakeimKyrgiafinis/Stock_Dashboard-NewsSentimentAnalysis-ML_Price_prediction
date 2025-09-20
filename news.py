from flask import Blueprint,Flask, render_template, request,jsonify
import requests
import feedparser

from textblob import TextBlob




def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1..1
    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"
    return {"score": polarity, "label": label}





news_bp = Blueprint('news_board', __name__)

GOOGLE_NEWS_RSS = (
    lambda q, hl="en-US", gl="US", ceid="US:en":
    f"https://news.google.com/rss/search?q={q}&hl={hl}&gl={gl}&ceid={ceid}"
)

@news_bp.route("/news")
def news():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    rss_url = GOOGLE_NEWS_RSS(query)
    try:
        resp = requests.get(rss_url, headers={"User-Agent": "stock-news-sentiment/1.0"})
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": "Failed to fetch feed", "details": str(e)}), 502

    feed = feedparser.parse(resp.text)
    entries = feed.entries[:10]

    results = []
    for e in entries:
        title = e.get("title", "")
        summary = e.get("summary", "")
        link = e.get("link", "")
        published = e.get("published", "")
        source = e.get("source", {}).get("title") if "source" in e else ""

        text = f"{title}\n\n{summary}"
        sentiment = analyze_sentiment(text)

        results.append({
            "title": title,
            "link": link,
            "published": published,
            "source": source,
            "summary": summary,
            "sentiment": sentiment
        })

    return jsonify({
        "query": query,
        "count": len(results),
        "results": results
    })

