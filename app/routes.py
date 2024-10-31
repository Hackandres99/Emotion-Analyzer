import os
import cv2
import numpy as np
from flask import Flask, request, jsonify

deepface_models = os.path.join(os.getcwd(), "app", "models")
os.environ["DEEPFACE_HOME"] = deepface_models
from deepface import DeepFace

app = Flask(__name__)

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    # print("Solicitud recibida para análisis de emociones.")
    
    if 'image' not in request.files:
        # print("Error: Imagen no encontrada en la solicitud.")
        return jsonify({"error": "Image key 'image' not found in request"}), 400

    file = request.files['image']
    if file.filename == '':
        # print("Error: No se seleccionó ninguna imagen para cargar.")
        return jsonify({"error": "No image selected for uploading"}), 400

    try:
        # print("Leyendo la imagen...")
        image = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # print("Imagen leída y decodificada correctamente.")
    except Exception as e:
        # print(f"Error al leer la imagen: {e}")
        return jsonify({"error": "Error reading the image: " + str(e)}), 500

    actions = ['emotion', 'age', 'gender', 'race']
    # print(f"Iniciando análisis de imagen con las acciones: {actions}")

    try:
        # print("Redondeando las puntuaciones de emociones a 4 decimales")
        decimal_places = 4
        analysis = DeepFace.analyze(img, actions=actions, enforce_detection=False)
        # print("Análisis completado.")

        if isinstance(analysis, list):
            analysis = analysis[0]
            # print("Se obtuvo el primer elemento del análisis de la lista.")

        # print("Asegurando compatibilidad JSON.")
        emotion_scores = {}
        
        for k, v in analysis['emotion'].items():
            if isinstance(v, (float, np.float32)):
                emotion_scores[k] = round(float(v), decimal_places)
            else:
                emotion_scores[k] = v

        # Obtener parámetros adicionales de la solicitud
        age = request.form.get('age', type=int)
        gender = request.form.get('gender', type=str)
        race = request.form.get('race', type=str)

        # Si no se proporcionan parámetros de edad, género o raza, devuelve la respuesta original
        if age is None and gender is None and race is None:
            response = {
                "emotion": analysis['dominant_emotion'],
                "emotion_scores": emotion_scores,
                "age": round(float(analysis.get('age', 0.0)), decimal_places),
                "gender": analysis.get('dominant_gender', None),
                "race": analysis.get('dominant_race', None)
            }
            # print("Respuesta JSON original formada exitosamente.")
        else:
            # Ajustar las puntuaciones de emociones según los parámetros dados
            adjusted_emotion_data = adjust_emotion(emotion_scores=emotion_scores, age=age, gender=gender, race=race)

            response = {
            "emotion": adjusted_emotion_data['emotion'],
            "emotion_scores": adjusted_emotion_data['emotion_scores'],
            "age": age if age is not None else round(float(analysis.get('age', 0.0)), decimal_places),
            "gender": gender if gender is not None else analysis.get('dominant_gender', None),
            "race": race if race is not None else analysis.get('dominant_race', None)
        }
        # print("Respuesta JSON ajustada formada exitosamente.")

    except Exception as e:
        # print(f"Error durante el análisis de emociones: {e}")
        return jsonify({"error": str(e)}), 500

    # print("Análisis completado y respuesta devuelta al cliente.")
    return jsonify(response)

def adjust_emotion(emotion_scores, age=None, gender=None, race=None):
    adjusted_emotion_scores = emotion_scores.copy()

    # Ajustes basados en el género
    # Male (Masculino)
    # Female (Femenino)
    # Genderless (Sin género)
    if gender is not None:
        if gender.lower() == 'male':
            adjusted_emotion_scores['angry'] = min(adjusted_emotion_scores['angry'] + 0.5, 1)
        elif gender.lower() == 'female':
            adjusted_emotion_scores['happy'] = min(adjusted_emotion_scores['happy'] + 0.3, 1)

    # Ajustes basados en la edad
    if age is not None:
        if age < 18:
            adjusted_emotion_scores['surprise'] = min(adjusted_emotion_scores['surprise'] + 0.2, 1)
            adjusted_emotion_scores['sad'] = max(adjusted_emotion_scores['sad'] - 0.1, 0)
        elif age > 50:
            adjusted_emotion_scores['sad'] = min(adjusted_emotion_scores['sad'] + 0.3, 1)
            adjusted_emotion_scores['happy'] = max(adjusted_emotion_scores['happy'] - 0.2, 0)

    # Ajustes basados en la raza
    # Asian (Asiático)
    # Indian (Indio)
    # Black (Negro)
    # White (Blanco)
    # Middle Eastern (Medio Oriente)
    # Latino Hispanic (Latino/Hispano)
    if race is not None:
        if race.lower() == 'asian':
            adjusted_emotion_scores['neutral'] = min(adjusted_emotion_scores['neutral'] + 0.2, 1)
        elif race.lower() == 'african':
            adjusted_emotion_scores['angry'] = min(adjusted_emotion_scores['angry'] + 0.15, 1)
        elif race.lower() == 'caucasian':
            adjusted_emotion_scores['happy'] = min(adjusted_emotion_scores['happy'] + 0.1, 1)

    # Normalización para que la suma de los porcentajes de emociones ajustadas sea 100%
    total_score = sum(adjusted_emotion_scores.values())
    if total_score > 0:  # Para evitar división por cero
        adjusted_emotion_scores = {k: round((v / total_score) * 100, 4) for k, v in adjusted_emotion_scores.items()}

    # Determinar la emoción dominante ajustada
    dominant_emotion = max(adjusted_emotion_scores, key=adjusted_emotion_scores.get)
    return {
        "emotion": dominant_emotion,
        "emotion_scores": adjusted_emotion_scores
    }

# print(f"DeepFace está usando modelos desde: {deepface_models}")