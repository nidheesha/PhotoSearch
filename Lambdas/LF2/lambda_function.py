from elasticsearch import Elasticsearch, RequestsHttpConnection
import json
import boto3


def lambda_handler(event, context):
    # TODO implement

    # dismbiguate search query using lex bot
    print(event)
    client = boto3.client('lex-runtime')
    # query_txt = event['queryStringParameters']['query']
    # print("Debug: ", query_txt)

    print("Was here")
    response = client.post_text(
        botName='SearchQuery',
        botAlias='search',
        userId='test',
        inputText=event['query']
    )
    print(response)

    print(response["slots"]["keyWordOne"])

    # for i in range(len(query_txt)):
    #     inpTxt = query_txt[i].lower()
    #     response = client.post_text(
    #         botName='SearchQuery',
    #         botAlias ='search',
    #         userId='test',
    #         inpuText=inpTxt
    #         )
    #     print(response)

    # extract keyword from lexbot using slots in sample utterances
    labels = []
    labels.append(response["slots"]["keyWordOne"])
    if (response['slots']['keyWordTwo']):
        labels.append(response["slots"]["keyWordTwo"])
    # keywords = response['slots']['obj1']
    # labels = re.split(',and|', keywords)

    es = Elasticsearch(
        hosts=[{'host': 'search-photosindex-kasqwzvxzvwhduhwz6wswjeif4.us-east-1.es.amazonaws.com', 'port': 443}],
        # http_auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es'),
        http_auth=('master', 'Nidheesha@97'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    print(labels)
    es_query = ' '.join(labels)
    print(es_query)

    response_es = es.search(
        index="photos",
        body={
            "query": {
                "match": {
                    "labels": es_query
                }
            }})

    # response_all = es.search(
    #     index='photos',
    #     body={
    #         "query":{
    #             "match_all":{}
    #         }
    #     })
    # print(response_all)
    print(response_es)

    results = []
    for hit in response_es['hits']['hits']:
        result = 'https://bucket2photos.s3.amazonaws.com/' + hit["_source"]["objectKey"]
        results.append(result)

    print(results)
    response_to_return = {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': list(set(results))
    }
    print(response_to_return)
    return response_to_return
