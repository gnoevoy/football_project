sheduler:
1. centralized  loogers locaion 
2. move in one file script 

pipelines
1. env variables if file exists
2. better comments and review logic for analytic_pipeline

readme
1. good description for pipilines with scheduler + rest api
    - images / graphics
    - describe logic
    - provide links

------------------

-> hide sensitive data to .env file and not track in git


rest api
-> clean structure, good comments
-> explanation: displaying produts and orders as json
-> link for jwt token + explanations what is it:
    fastapi docs: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    explanations: https://www.geeksforgeeks.org/json-web-token-jwt/

pipelines
-> centralized locatios for loggers, connections, cloud functions and enviroments
-> main.py: compose all etl logic, add logger, measure run time, try-except block for error handling

-> for each pipeline simple picture (represented logic) and steps what to do 
    + screenshot of the services, code, logs
    






