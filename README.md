# Emotion Analyzer
Para poder ejecutar esta api en tu computadora necesitas: 
1. Tener python 3.7 o superior instalado.
2. Descargar este projecto
3. Ubicarse en la raiz del projecto
4. Crear un entorno virtual a travez del cmd:
```sh
python -m venv venv
```
5. Activar el entorno virtual:
```sh
venv\scripts\activate
```
6. Instalar las dependecias del archivo requirements.txt:
```sh
pip install -r requirements.txt
```
7. Agregar variables de entorno a arcivo .env:
```bash
CONFIG_ENV=config.dev
TF_ENABLE_ONEDNN_OPTS=0
```
8. Ejecutar el servidor waitress:
```sh
waitress-serve --host=localhost --port=5000 run:app
```
## Consumo de la api:
A traves de la url [local] se pueden enviar las peticiones http

Si solo se envia la imagen a traves de post devolvera el resultado que detectaron los modelos de deepface para el reconocimiento facial:

![only image][only image]

Si se envia una peticion con parametros adicionales como lo son la edad, la raza y la edad estos se reflejaran en la repuesta, ademas de modificar los porcentajes de las emociones detectadas en la imagen:

![with parameters][with parameters]

La emocion que tenga mayor porcetaje sera la que refleje la emocion dominante de la respuesta.

Para que la aplicación que va a consumir esta api pueda realizar estas peticiones es necesario
establecer en la carpeta config cuales van a ser las urls que tendran acceso a la api

![url access][url access]

Esto se puede hacer tanto en el archivo .dev o .prod, dependiendo de que entorno se va a utilizar se puede cambiar la forma de ejecucion creando un archivo .env que contenga lo siguiente:


[local]: http://localhost:5000/analyze_emotion
[only image]: documentation/only_image.jpg
[with parameters]: documentation/with_parameters.jpg
[url access]: documentation/app_access_url.jpg