import boto3

ddb = boto3.client('dynamodb', 'ap-south-1')

with (open('newsfeed_articles_data.csv') as data_record_file):
    lines = data_record_file.readlines()
    data = dict()
    item_list = list()
    record_count = 0

    for line in lines:
        article_id, article_text, article_title, article_author_id, article_channel_id,\
        article_category_name, article_published_at, is_breakingnews_flag = line.split('#')
        record_count = record_count + 1

        response = ddb.put_item(
            TableName='3aayaam_news_articles',
            Item={
                'article_id': {'S': str(article_id)},
                'article_text': {'S': article_text},
                'article_title': {'S': article_title},
                'article_author_id': {'S': str(article_author_id)},
                'article_channel_id': {'S': article_channel_id},
                'article_category_name': {'S': article_category_name},
                'article_published_at': {'S': article_published_at},
                'is_breakingnews_flag': {'S': is_breakingnews_flag}
            }
        )
