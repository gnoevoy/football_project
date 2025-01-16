Aim: scrape data from rgol and upload it to cloud storage.
Result: get structured 2 files (json or csv) and 2 folders with content images

===================

shoes: https://www.r-gol.com/en/football-boots?filters=131%5B7502%5D%7e135%5B7586%2C7547%2C7504%2C8212%2C7617%5D%7e152%5B83011%5D
balls: https://www.r-gol.com/en/footballs?filters=131%5B83115%5D%7e135%5B7586%2C7547%2C7504%2C19117%5D
- title
- price
- rgol id
- images
- colors (linked products by id's)
- sizes (only for shoes)
- description
- features (list)

===================

plan
1. create a file with:
    - total vs actual
    - page | name | link
-> identify a problem

2. separate code by function and blocks (perhaps severals files: functions, actual code and tranformation)
3. handle product page data



