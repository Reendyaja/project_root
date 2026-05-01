from flask import Flask, jsonify
import cloudscraper
import json

app = Flask(__name__)
# Inisialisasi scraper dengan browser yang lebih modern
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})

@app.route('/api/wingo')
def get_wingo():
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://didihub.one/",
            "Origin": "https://didihub.one"
        }
        
        # Ambil data curRound
        response_cur = scraper.get("https://didihub.one/api/main/lottery/curRound?type=2", headers=headers, timeout=15)
        
        # Ambil data rounds
        response_rounds = scraper.get("https://didihub.one/api/main/lottery/rounds?page=1&count=120&type=2", headers=headers, timeout=15)

        # Cek apakah respon kosong atau kena blokir
        if response_cur.status_code != 200:
            return jsonify({"error": f"Didihub Error {response_cur.status_code}", "raw": response_cur.text[:100]}), 500

        try:
            cur_data = response_cur.json()
            rounds_data = response_rounds.json()
        except json.JSONDecodeError:
            return jsonify({"error": "Cloudflare Challenge detected. Respon bukan JSON.", "raw": response_cur.text[:100]}), 503

        return jsonify({
            "period": cur_data.get('data', {}).get('period', "-") or cur_data.get('period', "-"),
            "endTime": cur_data.get('data', {}).get('endTime', "-") or cur_data.get('endTime', "-"),
            "items": rounds_data.get('data', {}).get('items', []) or rounds_data.get('items', [])
        })

    except Exception as e:
        return jsonify({"error": "Internal Python Error", "details": str(e)}), 500
