import requests
import json


def get_result_from_model(tos):
    b64_str = tos
    
    
    #data = test_audio
    PARAMS = {'data':b64_str}
    response = requests.post(url='http://localhost:5001/predict?',data=PARAMS)
    print('Respuesta de la red neuronal: {}'.format(response.text))
    predictions = json.loads(response.text)

    #data = json.dumps({"signature_name": "serving_default", "instances": test_audio.tolist()})
    #headers = {"content-type": "application/json"}
    #json_response = requests.post('http://localhost:5001/predict', data=data, headers=headers)
    #print(json_response.text)
    #predictions = json.loads(json_response.text)['predictions']
    print(predictions)
    

    return f'Resultado: {predictions}'


if __name__ == '__main__':
    get_result_from_model('')
