import functions_framework
import configFile as c
from google.cloud import storage
import json
import requests
from multiprocessing import Pool

def mapper(args):
    processNumber, filename = args
    headers = {'Authorization': c.AUTH}
    params = {'filename':filename,'mapperIdx':processNumber}
    response = requests.post(url = c.MAPPERURL,json=params,headers=headers)
    return response

def reducer(args):
    processNumber, filename = args
    headers = {'Authorization': c.AUTH}
    params = {'filename':filename,'mapperIdx':processNumber}
    response = requests.post(url = c.REDUCERURL,json=params,headers=headers)
    return response

def cleanup():
    cleanupList = json.loads(c.CLEANUP)
    client = storage.Client(project=c.PROJECTID)
    
    for bucketname in cleanupList:
        bucket = client.bucket(bucketname)
        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.delete()

def finalIndexing():
    client = storage.Client(project=c.PROJECTID)
    bucket = client.bucket(c.INDEXING_INPUT)
    client = storage.Client(project=c.PROJECTID)
    for blob in client.list_blobs(c.INDEXING_INPUT):
        blobFile = bucket.get_blob(blob.name)
        reducerData = json.loads(blobFile.download_as_text(encoding=c.FORMAT))
        
        outputBucket = client.bucket(c.INDEXING_OUTPUT)        
        if outputBucket.get_blob(c.OUTPUT_FILENAME) != None:
            outputBlobFile = outputBucket.get_blob(c.OUTPUT_FILENAME)
            existingIndexing = json.loads(outputBlobFile.download_as_text(encoding=c.FORMAT))
            
            for key in reducerData:
                if key in existingIndexing.keys():
                    #print(f'current = {reducerData[key]} existing = {existingIndexing[key]}')
                    flag=True
                    for i in range(len(existingIndexing[key])):
                        if reducerData[key][0][0] == existingIndexing[key][i][0]:
                            flag=False
                    if flag == True:
                        existingIndexing[key].append(reducerData[key][0])
                else:
                    existingIndexing[key] = reducerData[key]
            outputBlobFile.upload_from_string(json.dumps(existingIndexing),content_type='application/json')
        else:
            outputBlobFile = outputBucket.blob(c.OUTPUT_FILENAME)
            outputBlobFile.upload_from_string(json.dumps(reducerData),content_type='application/json')


@functions_framework.http
def master(request):
    if request.get_json():
        request_json = request.get_json()
        filename = request_json['filename']

    headers = {'Authorization': c.AUTH}
    noOfMappers = c.NUMBER_OF_MAPPERS
    params = {'filename':filename,'noOfMappers':noOfMappers}
    response = requests.post(url = c.CREATE_CHUNKS,json=params,headers=headers)
    print(f'Chunks Response: {response}')

    if response.status_code == 200:
        print('Calling Mappers')
        with Pool(processes=c.NUMBER_OF_MAPPERS) as pool:
            processArgs = [(i, filename) for i in range(1, c.NUMBER_OF_MAPPERS + 1)]
            response = pool.map(mapper, processArgs)
            pool.close()
            pool.join()
    print(f'Mapper Response: {response}')

    params = {'filename':filename}
    response = requests.post(url = c.SHUFFLEURL,json=params,headers=headers)
    print(f'Shuffle Sort Response: {response}')
    
    if response.status_code == 200:
        print('Calling Reducers')
        with Pool(processes=c.NUMBER_OF_REDUCERS) as pool:
            processArgs = [(i, filename) for i in range(1, c.NUMBER_OF_REDUCERS + 1)]
            response = pool.map(reducer, processArgs)
            pool.close()
            pool.join()
    print(f'Reducer Response: {response}')
    
    finalIndexing()
    cleanup()
    return "Success"