import tensorflow as tf
import statistics
import tqdm
import librosa
from .util import *
from .config import RUTA_MODELO
import os

import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def get_result_from_model(tos):
    b64_str = tos
    
    file_id = 'TAKE ID FROM SHAREABLE LINK'
    destination = 'variables.data-00000-of-00001'
    download_file_from_google_drive(file_id, destination)

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
        extract_snippets(folder_wav_path, snippet_duration_sec=1)


    WORDS_X = np.array(tf.io.gfile.listdir(str(data_testExterno)))

    TARGET_SAMPLE_RATE = 16000

    os.mkdir('./audio_procesado/16Hz')
    
    word_dir = data_test
    resample_wavs(word_dir, target_sample_rate=TARGET_SAMPLE_RATE)

    files = tf.io.gfile.glob('./audio_procesado/16Hz'+ '/*_16000hz.wav')
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
    return f'Resultado: {results[pred_moda]}'


if __name__ == '__main__':
    get_result('')
