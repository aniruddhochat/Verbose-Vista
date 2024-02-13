import functions_framework
import configFile as c
from google.cloud import storage
import json
import collections
def groupByHashing(groupBy,filename):
    
    shuffleSortDict = collections.defaultdict(list)
    for key in groupBy:
        shuffleSortDict[(hash(key)%c.NUMBER_OF_REDUCERS)+1].append([key,filename,(hash(key)%c.NUMBER_OF_REDUCERS)+1,groupBy[key]])
    
    client = storage.Client(project=c.PROJECTID)
    bucket = client.bucket(c.SHUFFLE_OUTPUT_BUCKET)
    for i in shuffleSortDict:
        blobName = f"{filename}-shufflesort-{i}"        
        blob = bucket.blob(blobName)
        blob.upload_from_string(json.dumps(shuffleSortDict[i]),content_type='application/json')
    
    return shuffleSortDict
@functions_framework.http
def shuffleSort(request):    
    if request.get_json():
        request_json = request.get_json()
        filename = request_json['filename']

    client = storage.Client(project=c.PROJECTID)    
    bucket = client.bucket(c.INPUT_BUCKET_NAME)
    groupBy = collections.defaultdict(list)
    for blob in client.list_blobs(c.INPUT_BUCKET_NAME):
        if blob.name.startswith(filename):
            blobFile = bucket.get_blob(blob.name)
            chunk = json.loads(blobFile.download_as_text(encoding=c.FORMAT))
            for word in chunk:
                groupBy[word[0]].append(word[1])
    
    finalList = groupByHashing(groupBy,filename)
    return finalList