# Descripcion de Gráficos Estadísticas Tipo Pastel y Barras en Lenguaje Natural

El presente trabajo tiene como objetivo desarrollar una aplicación que permita describir gráficos estadísticos de tipo pastel y de barras utilizando modelos preentrenados, flask y python. Estos gráficos estadísticos son representaciones visuales que permiten comunicar información de forma estructurada y resumida. Sin embargo, muchas personas encuentran difícil comprender este tipo de gráficos, especialmente aquellas que prefieren la información en formato textual o que tienen discapacidad visual. En este trabajo, se intentó realizar un fine-tuning al modelo multimodal BLIP utilizando 100 imágenes subtituladas manualmente. Además, se implementó un asistente virtual en forma de chat que permite hacer preguntas sobre las imágenes cargadas. Aunque no se logró el objetivo de manera eficiente debido a varias razones, como el conjunto de datos utilizado, se espera que este trabajo pueda evolucionar con un poco más de trabajo en sus metadatos para un nuevo entrenamiento.

## Instalación

Python 3.10.13

1. Descargar la carpeta "models" que contiene los modelos del repositorio en Google Drive.
2. Extraer los modelos que se encuentran en archivos .rar dentro de la carpeta.

3. Ejecutar el comando: pip install -r requirements.txt

En caso de presentar algún tipo de inconveniente se debe instalar:

- pip install flask
- pip install transformers
- pip3 install torch torchvision torchaudio
- pip install deep-translator
- pip install gTTS

4. Ejecutar el archivo app.py
5. Abrir http://127.0.0.1:5000/

## Contribuciones
Human Perception in Computer Vision, 24 de Febrero del 2024

By 17JDSM

## Licencia
...
