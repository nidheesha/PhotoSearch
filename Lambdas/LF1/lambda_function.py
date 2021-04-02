import json
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
import time


def getESbody(photo_name, bucket_name, labels):
    timestamp = time.time()
    return {'objectKey': photo_name, 'bucket': bucket_name, 'createdTimestamp': timestamp, 'labels': labels}


def insertElasticSearchData(photo_name, bucket_name, labels):
    host = 'search-photosindex-zp5yu5u4n5tfnqci5ryptmieqq.us-east-2.es.amazonaws.com'
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        # http_auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es'),
        http_auth=('master', 'Nidheesha@97'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    es_body = getESbody(photo_name, bucket_name, labels)

    rep = es.index(
        index="photos",
        doc_type="Photos",
        id=es_body['createdTimestamp'],
        body=es_body,
        refresh=True)

    return rep


def elasticSearch(cuisine=''):
    es = Elasticsearch(
        hosts=[{'host': 'search-photosindex-zp5yu5u4n5tfnqci5ryptmieqq.us-east-2.es.amazonaws.com', 'port': 443}],
        # http_auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es'),
        http_auth=('master', 'Nidheesha@97'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    """
    response = es.search(
        index="restaurants",
        body={
              "query": {
                "bool": {
                  "must": {
                    "match": {
                      "cuisine": 'chinese'
                    }
                  }
                }
              }
            })
    """
    response = es.search(
        index="photos",
        body={
            "query": {
                "match_all": {}
            }
        })
    print("ES search result:", json.dumps(response))
    return response


def lambda_handler(event, context):
    print(json.dumps(event))
    client = boto3.client('rekognition')

    s3 = event['Records'][0]['s3']
    bucket_name = s3['bucket']['name']
    photo_name = s3['object']['key']

    service = boto3.resource('s3')
    object = service.Object(bucket_name, photo_name)

    print(json.dumps(object.metadata))
    if "customlabels" in object.metadata:
        custom_labels = object.metadata['customlabels'].split(',')
    else:
        custom_labels = []
    pass_object = {'S3Object': {'Bucket': bucket_name, 'Name': photo_name}}
    print('pass_object:', pass_object)

    resp = client.detect_labels(Image=pass_object)
    print(json.dumps(resp))

    labels = []
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])

    labels.extend(custom_labels)
    print(labels)

    try:
        rep = insertElasticSearchData(photo_name, bucket_name, labels)
        print(json.dumps(rep))
        elasticSearch()
    except Exception as ex:
        print(ex)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
