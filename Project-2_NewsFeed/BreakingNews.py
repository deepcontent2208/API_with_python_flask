from flask import Flask, request
import redis

app = Flask(__name__)

@app.route('/readbreakingnews', methods = ['GET'])
def read_breaking_news():
    article_channel_id = request.args.get('channel_id')
    article_date = request.args.get('article_date')
    breaking_news_key = str(article_channel_id) + ':' + str(article_date)
    resp = redis.Redis(host='redis-news-feed-db-ii48qi.serverless.aps1.cache.amazonaws.com', port=6379, ssl=True)
    breaking_news_record = resp.json().get(breaking_news_key, "$")

    if len(breaking_news_record) > 0:
        pass
    else:
        breaking_news_record = "No Breaking news for this Channel!!"

    return breaking_news_record


if __name__ == "__main__":
    global data
    data = dict()
    app.run(host='0.0.0.0',port=10003,debug=True)