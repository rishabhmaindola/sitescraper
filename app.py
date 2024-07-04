from flask import Flask, jsonify, request, render_template
from services import crawl
from services import extract_body_text
from services import extract_all_data
from services import extract_query_tag
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day","50 per hour"]
)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(status=429,error="ratelimit exceeded", message="You have exceeded your rate limit. Please try again later."),429

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get-sitemap', methods=['GET'])
@limiter.limit("10 per minute")
def get_sitemap():
    url = request.args.get('url')
    if not url:
        data = request.get_json()
        if data:
            url = data.get('url')
    if url:
        crawled_urls = crawl(url)
        return jsonify({"crawled_urls": crawled_urls})
    else:
        return jsonify({"error": "Please provide a URL parameter in the query."}), 400


@app.route('/get-data', methods=['GET'])
@limiter.limit("10 per minute")
def get_data():
    url = request.args.get('url')
    if not url:
        data = request.get_json()
        if data:
            url = data.get('url')
    if url:
        body_text = extract_body_text(url)
        return jsonify({"body_text": body_text})
    else:
        return jsonify({"error": "Please provide a URL parameter in the query."}), 400
    

@app.route('/get-all', methods=['GET'])
@limiter.limit("10 per minute")
def get_all_data():
    url = request.args.get('url')
    if not url:
        data = request.get_json()
        if data:
            url = data.get('url')
    if url:
        data = extract_all_data(url)
        return jsonify({"website_data": data})
    else:
        return jsonify({"error": "Please provide a URL parameter in the query."}),400
    
    
@app.route('/get-tag', methods=['GET'])
@limiter.limit("10 per minute")
def get_tag():
    url = request.args.url('url')
    tag = request.args.url('tag')
    if not url:
        data = request.get_json()
        if data:
            url = data.get('url')
            tag = data.get('tag')
        if url:
            if tag:
                data = extract_query_tag(url,tag)
                return jsonify({"query_tag_data": data})
            else:
                return jsonify({"error":"Please provide a query tag."}),400
        else:
            return jsonify({"error":"Please provide a website url."}),400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)