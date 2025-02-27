#! /usr/bin/bash

ENV="/home/bars1k/football_project/env"
FILE=" /home/bars1k/football_project/web_scraping/scripts/orders_generator.py"
CREDENTIALS="/home/bars1k/football_project/.credentials"

# export credentials 
set -a
source $CREDENTIALS
set +a

# run code with env
source $ENV/bin/activate
python $FILE
deactivate
