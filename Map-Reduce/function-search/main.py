import functions_framework
import configFile as c
from google.cloud import storage
import json

@functions_framework.http
def search(request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Max-Age": "3600"
    }

    if request.get_json():
        request_json = request.get_json()
        keyword = request_json['keyword']
    
    client = storage.Client(project=c.PROJECTID)
    bucket = client.bucket(c.SEARCH_BUCKET_NAME)
    blobFile = bucket.get_blob(c.SEARCH_FILE_NAME)
    searchData = json.loads(blobFile.download_as_text(encoding=c.FORMAT))

    print(f'Request {request}')
    print(request.headers.get("keyword"))

    if keyword in searchData.keys():
        return (json.dumps(searchData[keyword]),200,headers)
    else:
        return ('Keyword not found', 404, headers)