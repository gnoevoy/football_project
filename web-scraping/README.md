>> impelemnt logging ?
>> schedule tasks with prefect - lear how 

* place code to cloud 
    - how to get the most recent and stable version of code
    - will prefect get it and excute?

------------

scrape links
    yes -> there're links move next
    no -> inform that there's no content

simle script generate num
    if 1 -> append value to a file
    else -> notify about incorrect number
* execute every minute


Write task results to cloud storage - connect to GCS (not in memory), result_storage
can cache resutl to not rerurn again -> https://docs.prefect.io/v3/develop/task-caching

prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true
You can configure remote storage (e.g., S3, GCS).


caching:
enable only for retries inside one specifc flow 
* no other need because my scipt dynamic
can store in docker container and deleting after finishing
