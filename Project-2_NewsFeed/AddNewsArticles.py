from flask import Flask, request
import boto3, redis, json

app = Flask(__name__)

def upload_breaking_news(data):
    breaking_news_key = data['article_channel_id'] + ':' + data['article_published_at']
    resp = redis.Redis(host='redis-news-feed-db-ii48qi.serverless.aps1.cache.amazonaws.com', port=6379,ssl=True)
    # redis_data = str(data)
    add_record_in_redis = resp.json().set(breaking_news_key, "$", data)

    if add_record_in_redis == 1:
        msg['redis_msg'] = 'Record inserted in Redis'
    else:
        msg['redis_msg'] = 'Record insert failed in Redis'


@app.route('/addnewsarticles', methods = ['PUT'])
def report_news():
    ddb = boto3.client('dynamodb', 'ap-south-1')

    news_data = json.loads(request.data)

    data['article_id'] = str(news_data['article_id'])
    data['article_text'] = news_data['article_text']
    data['article_title'] = news_data['article_title']
    data['article_author_id'] = str(news_data['article_author_id'])
    data['article_channel_id'] = news_data['article_channel_id']
    data['article_category_name'] = news_data['article_category_name']
    data['article_published_at'] = news_data['article_published_at']
    data['is_breakingnews_flag'] = news_data['is_breakingnews_flag']

    response = ddb.put_item(
        TableName = '3aayaam_news_articles',
        Item ={
            'article_id' : {'N': data['article_id']} ,
            'article_text' : {'S': data['article_text']},
            'article_title' : {'S': data['article_title']},
            'article_author_id' : {'N': data['article_author_id']},
            'article_channel_id': {'S': data['article_channel_id']},
            'article_category_name': {'S': data['article_category_name']},
            'article_published_at': {'S': data['article_published_at']},
            'is_breakingnews_flag': {'S': data['is_breakingnews_flag']}
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg['dynamodb_msg'] = 'Record inserted in DynamoDB'

        # insert into in-memory database if breaking news flag is YES
        if data['is_breakingnews_flag'].upper() == 'Y':
            upload_breaking_news(data)

    else:
        msg['dynamodb_msg'] = 'Record insert failed in DynamoDB'

    return data


if __name__ == "__main__":
    global data, msg
    data = dict()
    msg = dict()
    app.run(host='0.0.0.0', port=10002, debug=True)