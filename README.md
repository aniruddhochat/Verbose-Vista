## Verbose Vista : Document Search Engine based on Map-Reduce

### Introduction.
This repository deals with designing, developing, and implementing a robust search engine based on the concepts of Map-Reduce using Google Cloud Functions. 

The input corpus has been taken from the Gutenberg website which is the data of books in a text format (UTF-8). 

For storage of these files, I have made the use of Google Cloud Storage Buckets. 

To process these data, the map-reduce creates intermediate files which are also stored in the Buckets. 

I have also developed an interactive website to upload new files of new upcoming books to the corpus as well as make a search of a particular keyword. 

The end-to-end search engine was implemented using Flask framework which was then deployed on Google Cloud Run.

### Prerequisites.  
•	Install Google SDK in your local machine to access Google Cloud Platform.    
•	A Google Cloud account with active credits and projects are required.  
•	Clone this Repo.  
•	Create cloud functions from the Google Console (Not included in Bash Script since I created and deployed code manually).  
•	Create a Bucket and Blob in Google Cloud Storage (Not included in the Bash script since I created it manually and did not get the equivalent CLI command).    
•	Mention respective bucket and blob details in the `configFile.py`.  

### Initial Setup and Instructions.
Once the Google account has been configured with active credits and project, we need to first create Google Cloud Functions and Bucket Storage. 

All the Cloud Functions that are listed in the system architecture are included in the Map-Reduce folder. 

Each cloud function has its own set of `configFile.py` with a set of configurations required for processing data at that stage. 

They also contain their respective `requirements.txt` files consisting of the necessary installation of libraries.

### Files.
The Map-Reduce folder contains all the necessary cloud functions (FaaS).

•	`Function-master` – Contains all the necessary files required for the Master process.
•	`Function-create-chunks` – Contains all the necessary files required for creating the chunks of the data.
•	`Function-mapper` – Contains all the necessary files required for running the defined number of masters in parallel.
•	`Function-shufflesort` – Contains all the necessary files required for the grouping and redirecting words to reducers using hashing.
•	`Function-reducer` – Contains all the necessary files required for the reducer process.
•	`Function-search` – Contains all the necessary files required for searching the keyword from the website.
•	`Function-gcs-bucket-trigger` – Contains all the necessary files required for handling the new incoming files and linking the bucket to the Map-Reduce system.

The remaining files on repository are all the necessary web development files required for flask app along with Google Cloud Run Deployment.


### Execution Instructions.

Since there are no Virtual Machines involved, we need to create Functions as a Service (FaaS) in Google Cloud Platform.

Create the exact same functions in Google Cloud with the same name, code , files and `requirements.txt`.
  
•	Use the `upload files` functionality on the Verbose Vista website to upload txt files from [Gutenberg][1] website.  
•	On uploading these files, the map-reduce system will create inverted index of the words in the books and store it in Google Cloud Storage Buckets.  
•	Use the `search` functionality to search for the frequency of the keywords apprearing in different books.  

### Map-Reduce Design.

#### Master.
The master plays a big part of this map-reduce system where it controls the whole process and ensures serial as well as parallel execution of the respective processes.

When a file has been uploaded from the website, it gets uploaded in the `books-dataset` bucket which in turn triggers the cloud function `gcs-bucket-trigger`. 

This function then calls the main master program with the parameters as filename to fetch and process the file which was just uploaded.

The master first creates chunks of this file based on the number of mappers defined in the `configFile.py`. 

Once the chunks are created the master creates a pool of multiprocessing tasks in parallel to process these chunks.

On completion of the mapping process, it turns to the Shuffle and Sorting algorithm function which groups the words based on their hash value and number of reducers.

Finally, it calls the reducer to process these sorted and grouped output and update/create the final inverted index.

In a nutshell, the master servers as an organiser orchestrating the whole map-reduce and ensures that the barrier has been implemented perfectly.

#### Chunks.
The chunks creation process is an important one since this is the stage the books are being read as input and based on this data the whole efficiency of the map-reduce is going to be dependent. Thus, the incoming data needs to be pre-processed and cleaned so that our indexing is done appropriately.

In this regard, I have made the use of python library **SpaCy** which vectorizes each word and cleans all the spaces, punctuations, junk characters and other impurities. 

SpaCy is known for its speed and efficiency, making it suitable for processing large volumes of text data.

Once the vectorization of the words is completed then onwards it is a simple function which gets the number of mappers and filename as input parameters and divides the file into that many number of chunks.

#### Mapper.
The chunks created by the above function serve as an input to mappers where each word irrespective of repetition is mapped as `[word, filename,1]`.

#### Shuffle Sort.
The output from the mapper serves as the input to the shuffle and sort function which groups the words and their occurrences and removes the duplicates created in the mapper stage. 

It also does a small calculation of hashing the words and then taking modulo with the number of reducers. This is done to decide which word should go to which reducer pool. 

The output of the Shuffle Sort stage is `[word, filename, 2, [1,1,1,1,1]]` where 2 determines that it must go to the reducer pool 2.

#### Reducer.
The reducer is executed in parallel as per the number of reducers defined in pool of parallelism. 

The reducer aggregates and takes the sum of the count received from the	 shuffle sort stage. The output of each reducer is `[word, filename,23]`.

### Combining and updating the inverted index.
This is executed by the master which combines the output of the reducers and does the inverted indexing. Finally, it updates the unique words currently present in the existing inverted index with the incoming data.

•	**Case 1 – New Word**
New words get appended in the existing hash table of the inverted index in the form of `{"melancholy": [["A Study in Scarlet.txt", 43]]}`.
•	**Case 2 – Existing Word**
In case there is an existing word already present in some other book (which is bound to happen), then it appends the current book name and the count of the times it has occurred in the incoming book into the has map in the form of `{"this": [["A Study in Scarlet.txt", 1400], ["Sherlock Holmes.txt", 390]]}` which means that the word `this` occurs **1400** times in `A study in Scarlet.txt` and **390** times in `Sherlock Holmes.txt`.

This is out final stage of indexing which can be used to perform search operation on.

Note: The design also supports multiple bulk uploading of the files and this creates multiple pools of the map-reduce system to handle such a heavy task.

### Verbose Vista – Document Search Engine.
Verbose Vista is a search engine website which makes use of this map-reduce design. 

The whole website is developed based on the flask framework and the design also supports multiple file uploads to be fed to the map-reduce system. 

This was developed keeping in mind that the super user should have access to add new upcoming books to our corpus of indexing. In this way we stay updated with the latest book releases.

### Web Development and Deployment Setup.
Once the website is ready and all the functionalities are working on your local host, we start creating a Dockerfile to include all the necessary files of the web application. 

For deployment, I have made the use of Google Cloud Run integrated with Google Cloud GitHub repositories. 

The key idea is to maintain this whole web application along with the Dockerfile in a GitHub repository. 

Then using Google Cloud run create a new service and integrate the GitHub repository. 

This setup offers Continuous Integration (CI) and continuous Deployment (CD) which means any new commits to the Git repository will automatically update the live web application. 

The link to the web application is: [Verbose Vista][2]

### Conclusion.
Search Engine based on the inverted index map-reduce system was successfully implement using cloud functions. 

System was designed keeping in mind parallel processing in pool for the mapper and reducer tasks and implementing a barrier. 

Verbose Vista, a web application was also implemented with the functionality such as search for general users and upload file for superuser/administrator.


[1]:    https://www.gutenberg.org/ "Gutenberg Website"
[2]:    https://verbose-vista-etlijojsoa-uc.a.run.app/ "Verbose Vista"