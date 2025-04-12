from flask import Flask, request
import requests, json

app = Flask(__name__)

@app.route('/reportnews', methods = ['PUT'])
def report_news():
    news_data = request.json

    r = requests.request('PUT', 'http://65.0.61.79:10002/addnewsarticles', data=json.dumps(news_data) )

    if r.status_code == 200:
        data['msg'] = 'News reported'
    else:
        data['msg'] = 'News reporting failed'

    return data


if __name__ == "__main__":
    global data
    data = dict()
    app.run(host='0.0.0.0', port=8002, debug=True)