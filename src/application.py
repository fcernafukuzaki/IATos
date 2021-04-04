import tensorflow as tf
import statistics
import librosa
from .util import *
from .config import RUTA_MODELO, TARGET_SAMPLE_RATE
import os
import requests
import json


def get_result_from_model(tos):
    b64_str = tos
    
    directory = './audio_sin_procesar/'
    #directory = '.\\audio_sin_procesar'
    os.makedirs(directory, exist_ok=True)
    webmfile = 'audio.webm'
    audio_name_wav = 'audio_transformado.wav'

    # Generar archivo WAV

    generate_webm_file(b64_str, directory, webmfile)
    webm_to_wav(directory, webmfile, audio_name_wav)
    
    # Cargar modelo

    model = tf.keras.models.load_model(RUTA_MODELO)

    data_test = './audio_procesado/'
    os.makedirs(data_test, exist_ok=True)
    data_testExterno = './audio_sin_procesar'
    #data_testExterno = '.\\audio_sin_procesar'

    folder_wav_paths = glob.glob(os.path.join(data_testExterno, "*.wav"))
    print(folder_wav_paths)
    snippets_dir_x = os.path.join(data_test, '')
    os.makedirs(snippets_dir_x, exist_ok=True)

    for folder_wav_path in folder_wav_paths:
        print("Extraído de %s..." % folder_wav_path)
        extract_snippets(snippets_dir_x, folder_wav_path, snippet_duration_sec=1)


    WORDS_X = np.array(tf.io.gfile.listdir(str(data_testExterno)))

    

    CARPETA_ARCHIVOS_SAMPLE = './audio_procesado/16Hz'
    if not os.path.exists(CARPETA_ARCHIVOS_SAMPLE):
        os.mkdir(CARPETA_ARCHIVOS_SAMPLE)
    
    word_dir = data_test
    resample_wavs(word_dir, target_sample_rate=TARGET_SAMPLE_RATE)

    files = tf.io.gfile.glob(CARPETA_ARCHIVOS_SAMPLE + '/*_16000hz.wav')
    print(type(files))

    test_audio = []
    test_labels = []

    for idx, file in enumerate(files):
        print(idx, file)
        sample_file = files[idx]
        test_ds = preprocess_dataset([str(sample_file)])

        for audio, label in test_ds:
            print(type(audio))
            test_audio.append(audio.numpy())

    test_audio = np.array(test_audio)

    pred = np.argmax(model.predict(test_audio),axis=1)
    print('El resultado es: {}'.format(pred))

    pred_moda = statistics.mode(pred)
    print('La moda es: {}'.format(pred_moda))

    results = {0:'negativo',1:'noise',2:'positivo'}
    print(f'Resultado: {results[pred_moda]}')

    #data = test_audio
    data = json.dumps({"signature_name": "serving_default", "instances": test_audio.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://localhost:8501/v1/models/saved_model:predict', data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    print(predictions)
    print('El resultado es: {}'.format(pred))

    pred_moda = statistics.mode(pred)
    print('La moda es: {}'.format(pred_moda))

    results = {0:'negativo',1:'noise',2:'positivo'}
    print(f'Resultado: {results[pred_moda]}')


    return f'Resultado: {results[pred_moda]}'


if __name__ == '__main__':
    get_result('')
