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

**products**
my_id | scraped_id | category_id | name | price | description | link

**colors**
product_id | color_id (id of the same product but with differet color and params)

**sizes**
size_id | product_id | size_num | in_stock

**categories**
category_id | category_name

**category-boots**
product_id | param-1 | param-2 | ...

**category-balls**
product_id | param-1 | param-2 | ...

images
-- boots
-- product_id
-- image
-- balls
-- product_id
-- image
