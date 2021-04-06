# Create Docker container

docker pull tensorflow/serving

docker run -p 8501:8501 --mount type=bind,source=/IATos/src/saved_model,target=/models/saved_model/1 -e MODEL_NAME=saved_model -t tensorflow/serving

# Upload Docker image to Docker Hub:

docker ps -a # To get id_docker_image
docker commit {id_docker_image} {username}/iatos-docker
docker push {username}/iatos-docker

Source:
https://towardsdatascience.com/deploying-a-tensorflow-model-to-production-made-easy-4736b2437103
https://medium.com/tensorflow/serving-ml-quickly-with-tensorflow-serving-and-docker-7df7094aa008

# Install requirements.txt

pip install -r requirements.txt
Declarar variable con la ubicación del archivo
set FLASK_APP=app.py
flask run
python app.py