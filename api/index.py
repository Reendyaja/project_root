from flask import Flask, jsonify
import cloudscraper

app = Flask(__name__)
scraper = cloudscraper.create_scraper()

@app.route('/api/wingo')
def get_wingo():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        cur = scraper.get("https://didihub.one/api/main/lottery/curRound?type=2", headers=headers).json()
        rounds = scraper.get("https://didihub.one/api/main/lottery/rounds?page=1&count=120&type=2", headers=headers).json()
        
        return jsonify({
            "period": cur.get('data', {}).get('period', "-"),
            "endTime": cur.get('data', {}).get('endTime', "-"),
            "items": rounds.get('data', {}).get('items', [])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Penting untuk Vercel
def handler(request):
    return app(request)
