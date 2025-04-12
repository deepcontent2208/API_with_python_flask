from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/readnews', methods = ['GET'])
def read_news():
    news_date = request.args.get('news_date')
    channel_id = request.args.get('channel_id')
    data = dict()

    parm = {"news_date" : news_date, "channel_id" : channel_id}

    resp = requests.get('http://52.66.68.109:10001/readnewsarticles', params=parm)

    if resp.status_code == 200:
        data = resp.json()
    else:
        data['err_msg'] = 'could not retrieve news for this date'

    return data


@app.route('/newsapi.org', methods = ['GET'])
def news_api_org():
    api_key = request.args.get('apiKey')
    data = dict()
    parm = {'apiKey' : api_key}
    resp = requests.get('http://52.66.68.109:10001/newsapi.org',params=parm)

    if resp.status_code == 200:
        data = resp.json()
    else:
        data['error_msg'] = 'error calling external api'

    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)