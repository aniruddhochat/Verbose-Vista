import functions_framework
import configFile as c
from google.cloud import storage
import json

@functions_framework.http
def mapper(request):
    if request.get_json():
        request_json = request.get_json()
        filename = request_json['filename']
        mapperIdx = request_json['mapperIdx']
        
    client = storage.Client(project=c.PROJECTID)
    bucket = client.bucket(c.INPUT_BUCKET_NAME)
    blobFile = bucket.get_blob(f'{filename}-chunk-{mapperIdx}')
    chunk = json.loads(blobFile.download_as_text(encoding=c.FORMAT))
    
    mapping = []
    for i in range(len(chunk)):
        mapping.append([chunk[i],1])
        
    outputBucket = client.bucket(c.MAPPER_OUTPUT_BUCKET)
    outputBlobFile = outputBucket.blob(f'{filename}-mapper-{mapperIdx}')
    outputBlobFile.upload_from_string(json.dumps(mapping),content_type='application/json')

    return mapping
