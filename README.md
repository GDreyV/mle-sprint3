uvicorn main:app --reload
uvicorn app.churn_app:app --host 0.0.0.0 --port 80 
docker image build . --tag simple_fast_api:2
docker container run --publish 4600:1702 simple_fast_api:2 
docker container run --publish 4601:8081 --volume=./models:/churn_app/models   --env-file .env <image-name>