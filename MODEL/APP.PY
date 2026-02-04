pip install tensorflow pillow numpy matplotlib
import numpy as np
from PIL import Image
from keras.applications.xception import Xception
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from pickle import load
import matplotlib.pyplot as plt
def extract_features(filename, model):
   image = Image.open(filename).resize((299, 299))
   image = np.array(image)[..., :3] / 127.5 - 1.0
   image = np.expand_dims(image, axis=0)
   return model.predict(image)
def word_for_id(integer, tokenizer):
   for word, index in tokenizer.word_index.items():
       if index == integer:
           return word
   return None
def generate_desc(model, tokenizer, photo, max_length):
   in_text = 'start'
   for _ in range(max_length):
       sequence = tokenizer.texts_to_sequences([in_text])[0]
       sequence = pad_sequences([sequence], maxlen=max_length)
       pred = np.argmax(model.predict([photo, sequence], verbose=0))
       word = word_for_id(pred, tokenizer)
       if word is None or word == 'end':
           break
       in_text += ' ' + word
   return in_text.replace('start', '').strip()
max_length = 32
tokenizer = load(open("tokenizer.p", "rb"))
caption_model = load_model('models/model_9.h5')
xception_model = Xception(include_top=False, pooling="avg")
image_path = "example.jpg"
photo_features = extract_features(image_path, xception_model)
caption = generate_desc(caption_model, tokenizer, photo_features, max_length)
print("Generated Caption:", caption)
plt.imshow(Image.open(image_path))
plt.axis('off')
plt.show()
