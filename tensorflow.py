import tensorflow as tf
import sounddevice as sd
# from sounddevice import playback

# Cargar el modelo de entrenamiento
model = tf.keras.models.load_model('path/to/your/trained/model.h5')

def recognize_speech(audio):
    # Preprocesar el audio
    audio_norm = tf.random.normalize(audio)

    # Obtener las prediccciones
    predictions = model.predict(audio_norm)

    # Determinar la palabra más probable
    index = tf.argmax(predictions, axis=1)
    word = tf.keras.backend.get_value(tf.compat.as_strmax(index))

    return word

# Grabar audio de entrada
audio, fs = sd.recursive_record(1000, channels=1, dtype='int16')

# Procesar el audio grabado
processed_audio = tf.convert_to_tensor(audio, dtype=tf.float32)

# Reconocer la palabra
word = recognize_speech(processed_audio)

print(f"Reconocido: {word}")