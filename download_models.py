import os
import requests

# Lista de URLs de los modelos
model_urls = {
    "facial_expression_model_weights.h5": "https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5",
    "age_model_weights.h5": "https://github.com/serengil/deepface_models/releases/download/v1.0/age_model_weights.h5",
    "gender_model_weights.h5": "https://github.com/serengil/deepface_models/releases/download/v1.0/gender_model_weights.h5",
    "race_model_single_batch.h5": "https://github.com/serengil/deepface_models/releases/download/v1.0/race_model_single_batch.h5"
}

# Ruta donde se guardarán los modelos
model_dir = '/app/models/.deepface/weights'

# Crea el directorio si no existe
os.makedirs(model_dir, exist_ok=True)

# Descarga los modelos si no existen
for model_name, url in model_urls.items():
    model_path = os.path.join(model_dir, model_name)
    if not os.path.exists(model_path):
        response = requests.get(url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print(f'Descargado: {model_name}')
    else:
        print(f'Ya existe: {model_name}')
