1. figure out how to deploy me script
2. configurate it porperly 
1. figure out how to deploy me script
2. configurate it porperly 


------------

prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true
You can configure remote storage (e.g., S3, GCS).


caching:
enable only for retries inside one specifc flow 
* no other need because my scipt dynamic
can store in docker container and deleting after finishing

-------------------
questions

work-pool - general config where to execute (yaml and ui setting)
queus - limit and priority can be changes
worker - execute code, can have its own name  
-> better to have 2 workers and execute it 
