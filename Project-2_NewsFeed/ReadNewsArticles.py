from flask import Flask, request
import boto3, requests

app = Flask(__name__)

@app.route('/readnewsarticles', methods = ['GET'])
def read_news_articles():
    ddb = boto3.client('dynamodb', 'ap-south-1')
    data = dict()
    channel_id = request.args.get('channel_id')
    news_date = request.args.get('news_date')

    if news_date:
        if channel_id:
            if len(channel_id) > 0 and len(news_date) > 0:
                resp = ddb.get_item(
                    TableName = '3aayaam_news_articles',
                    Key={
                        'article_published_at' : {'S' : news_date},
                        'article_channel_id' : {'S' : channel_id}
                    }
                )
                data = resp
        else:
            if len(news_date) > 0:
                resp = ddb.query(
                    TableName = '3aayaam_news_articles',
                    ExpressionAttributeValues={
                        ':news_date': {
                            'S': news_date,
                        },
                    },
                    KeyConditionExpression='article_published_at = :news_date',
                )
                data = resp

    else:
        data['msg'] = "Error!!! Manadatory parameter: news_date. Optional parameter: channel_id"

    return data


@app.route('/newsapi.org')
def news_api_org():
    api_key = request.args.get('apiKey')
    data = dict()

    parm = {"q" : "tesla", "from" : "2025-03-12", "sortBy" : "publishedAt", "apiKey" : api_key}

    resp = requests.get('https://newsapi.org/v2/everything',params=parm)

    if resp.status_code == 200:
        data = resp.json()
    else:
        data['error_msg'] = 'error calling external api'

    return data





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10001, debug=True)