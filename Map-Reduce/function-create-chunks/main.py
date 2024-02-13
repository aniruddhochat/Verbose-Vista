import functions_framework
import configFile as c
from google.cloud import storage
import spacy
import json
def uploadChunks(response,filename,noOfMappers):
    sublists =[]
    for i in range(noOfMappers):
        currentIdx = int(len(response)/noOfMappers)
        sublists.append(response[:currentIdx])
        response = response[currentIdx:]
        noOfMappers -= 1
  
    client = storage.Client(project=c.PROJECTID)
    bucket = client.bucket(c.CHUNKS_OUTPUT_BUCKET)
    for i,data in enumerate (sublists,start=1):
        blobName = f"{filename}-chunk-{i}"        
        blob = bucket.blob(blobName)
        blob.upload_from_string(json.dumps(data),content_type='application/json')

@functions_framework.http
def createChunks(request):
    if request.get_json():
        request_json = request.get_json()
        filename = request_json['filename']
        noOfMappers = request_json['noOfMappers']
    
    client = storage.Client(project=c.PROJECTID)
    bucket = client.bucket(c.INPUT_BUCKET_NAME)
    blobFile = bucket.get_blob(filename)
    text = blobFile.download_as_text(encoding=c.FORMAT)
    
    dataPreProcessModule = spacy.load('en_core_web_sm', disable=["ner", "parser","tagger"])
    
    document = dataPreProcessModule(text)
    words = [token.text.lower() for token in document if token.is_punct != True]
    newWord =[]
    for word in words:
        newWord.append(' '.join(word.split()))
    words = ' '.join(newWord).split()

    uploadChunks(words,filename,noOfMappers)

    return words
