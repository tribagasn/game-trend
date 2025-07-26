from flask import Flask, render_template, request, jsonify
from pytrends.request import TrendReq
from datetime import datetime
import pandas as pd
import time
from pytrends.exceptions import ResponseError  
import random
import requests
import os

app = Flask(_name_)

# Konfigurasi untuk production
if os.environ.get('VERCEL'):
    app.config['TEMPLATES_AUTO_RELOAD'] = False
else:
    app.config['TEMPLATES_AUTO_RELOAD'] = True

# API Keys - gunakan environment variables untuk production
API_KEY = os.environ.get('DEEPSEEK_API_KEY', "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")
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', "AIzaSyDrwRrCYfhev87uSzwDxR3LRq1I0rQtwIw")
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

GAMES = ["Mobile Legends", "PUBG", "Free Fire", "Resident Evil", "League of Legends", "Valorant"]

@app.route('/')
def dashboard():
    """Renders the dashboard page."""
    return render_template('index.html')

@app.route('/analytic')
def analytic():
    """Renders the analytic page."""
    return render_template('analytic.html')

@app.route("/ml")
def mobile_legends():
    """Renders the Mobile Legends detail page."""
    return render_template("ml.html")

@app.route("/pubg")
def pubg():
    """Renders the PUBG detail page."""
    return render_template("pubg.html")

@app.route("/re")
def resident_evil():
    """Renders the Resident Evil detail page."""
    return render_template("re.html")

@app.route('/lol')
def lol_detail():
    """Renders the League of Legends detail page."""
    return render_template('lol.html')

@app.route('/freefire')
def freefire_detail():
    """Renders the Free Fire detail page."""
    return render_template('freefire.html')

@app.route('/valorant')
def valorant_detail():
    """Renders the Valorant detail page."""
    return render_template('valorant.html')

@app.route('/get_trend_data')
def get_trend_data():
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)

        keywords_batch1 = ["Mobile Legends", "PUBG", "Free Fire", "Resident Evil", "League Of Legends"]
        keywords_batch2 = ["Valorant"]

        range_days = int(request.args.get('range', 1))

        if range_days == 1:
            timeframe = 'now 1-d'
        elif range_days == 7:
            timeframe = 'now 7-d'
        elif range_days == 30:
            timeframe = 'today 1-m'
        else:
            timeframe = 'today 3-m'

        # Batch pertama
        pytrends.build_payload(keywords_batch1, timeframe=timeframe, geo='ID')
        df1 = pytrends.interest_over_time()

        # Batch kedua
        if keywords_batch2:
            pytrends.build_payload(keywords_batch2, timeframe=timeframe, geo='ID')
            df2 = pytrends.interest_over_time()
            df = pd.concat([df1[keywords_batch1], df2[keywords_batch2]], axis=1)
            df["date"] = df1.index
        else:
            df = df1
            df["date"] = df.index

        df.reset_index(drop=True, inplace=True)

        results = {}
        for keyword in keywords_batch1 + keywords_batch2:
            results[keyword] = [
                {"time": row["date"].isoformat(), "score": row[keyword]}
                for _, row in df.iterrows()
            ]
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rekomendasi-judul", methods=["GET", "POST"])
def rekomendasi_judul():
    if request.method == "POST":
        game_name = request.form["game"]
        prompt = f"Buatkan 5 judul YouTube yang menarik, SEO-friendly, dan click-worthy untuk video tentang game {game_name}, seolah-olah dibuat oleh YouTuber gaming yang ingin viral."

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Kamu adalah ahli strategi YouTube untuk konten game."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            hasil = response.json()
            generated_text = hasil['choices'][0]['message']['content']
            return render_template("rekomendasi_judul.html", judul_list=generated_text.split("\n"), game=game_name)
        except Exception as e:
            return render_template("rekomendasi_judul.html", error=str(e))

    return render_template("rekomendasi_judul.html")

@app.route('/title')
def judul_video():
    return render_template('title.html')

@app.route("/trending_games")
def get_trending_games():
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": "ID",
        "videoCategoryId": "20",
        "maxResults": 9,
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if "items" not in data:
            return jsonify({"videos": []})

        videos = []
        for item in data["items"]:
            videos.append({
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "channel": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={item['id']}"
            })

        return jsonify({"videos": videos})
    except Exception as e:
        print("Error:", e)
        return jsonify({"videos": []})

@app.route('/trending')
def trending_page():
    return render_template('trending.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route("/search_game")
def search_game():
    game = request.args.get("game")
    if not game:
        return jsonify({"error": "No game provided"}), 400

    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        pytrends.build_payload([game], cat=0, timeframe='today 3-m')
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({"labels": [], "scores": [], "game": game})

        labels = [dt.strftime('%Y-%m-%d') for dt in data.index]
        scores = data[game].tolist()

        return jsonify({
            "labels": labels,
            "scores": scores,
            "game": game
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Untuk Vercel
def handler(event, context):
    return app(event, context)

if _name_ == '_main_':
    app.run(debug=True)