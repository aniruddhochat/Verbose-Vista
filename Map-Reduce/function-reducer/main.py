import functions_framework
import configFile as c
from google.cloud import storage
import json
import collections

@functions_framework.http
def reducer(request):
    if request.get_json():
        request_json = request.get_json()
        filename = request_json['filename']
        mapperIdx = request_json['mapperIdx']

    client = storage.Client(project=c.PROJECTID)
    bucket = client.bucket(c.INPUT_BUCKET_NAME)
    blobFile = bucket.get_blob(f'{filename}-shufflesort-{mapperIdx}')
    sortedData = json.loads(blobFile.download_as_text(encoding=c.FORMAT))
    reducerData = collections.defaultdict(list)
    
    for i in range(len(sortedData)):
        reducerData[sortedData[i][0]].append([sortedData[i][1],sum(sortedData[i][3])])
        
    outputBucket = client.bucket(c.REDUCER_OUTPUT_BUCKET)
    outputBlobFile = outputBucket.blob(f'{filename}-reducer-{mapperIdx}')
    outputBlobFile.upload_from_string(json.dumps(reducerData),content_type='application/json')
    # if outputBucket.get_blob(c.OUTPUT_FILENAME) != None:
    #     outputBlobFile = outputBucket.get_blob(c.OUTPUT_FILENAME)
    #     existingIndexing = json.loads(outputBlobFile.download_as_text(encoding=c.FORMAT))
        
    #     for key in reducerData:
    #         if key in existingIndexing.keys():
    #             flag=True
    #             for i in range(len(existingIndexing[key])):
    #                 if reducerData[key][0][0] == existingIndexing[key][i][0]:
    #                     flag=False
    #             if flag == True:
    #                 existingIndexing[key].append(reducerData[key][0])
    #         else:
    #             existingIndexing[key] = reducerData[key]
    #     outputBlobFile.upload_from_string(json.dumps(existingIndexing),content_type='application/json')
    # else:
    #     outputBlobFile = outputBucket.blob(c.OUTPUT_FILENAME)
    #     outputBlobFile.upload_from_string(json.dumps(reducerData),content_type='application/json')
    
    return reducerData