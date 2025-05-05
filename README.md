
## Quick Start
- in folder ```app``` copy  ```.env.template``` and name it ```.env```, if need you can change some variables
- in root folder copy ```.env.template``` and name it ```.env``` enter REACT_APP_API
- in root folder run ```docker compose up --build -d```
- open ```http://127.0.0.1``` in your browser if its locally or open ip of your machine, now you can upload dataset (.zip format), in Statistic Page you can see how many images were uploaded in system
- to search images you can upload one photo on Image Page and receive the most similar results from db

## System requirements
- CPU min 2 cores
- RAM recommend at least 10gb, in another case you should change limit in docker-compose.yml, for fastapi
- Storage as much as you your datasets will require

### Used dataset:
- https://www.kaggle.com/datasets/bwandowando/basic-human-emotions

https://github.com/user-attachments/assets/29753c44-61d4-4963-92a9-9d42cdb4c820

