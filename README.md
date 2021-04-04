# Creación de contenedor
Fuente: https://towardsdatascience.com/deploying-a-tensorflow-model-to-production-made-easy-4736b2437103

docker pull tensorflow/serving

docker run -p 8501:8501 --mount type=bind,source=/D:/GitHub/Inteligencia_Artificial_repositorios_varios/virufy/IATos/src/saved_model,target=/models/saved_model/1 -e MODEL_NAME=saved_model -t tensorflow/serving