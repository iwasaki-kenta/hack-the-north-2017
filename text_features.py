import re

import indicoio
from nltk.tokenize import PunktSentenceTokenizer
from sklearn.model_selection import train_test_split
from tpot import TPOTClassifier
import numpy as np

import config

indicoio.config.api_key = config.indico_key()

categories = ['education', 'legal', 'nutrition']

tokenizer = PunktSentenceTokenizer()

dataset = {
    "education": [],
    "legal": [],
    "nutrition": []
}

for category in categories:
    category_sentences = []
    for index in range(5):
        with open(category + 'Samples' + str(index) + '.txt') as file:
            text = file.read()

            sentences = [re.sub('[^0-9a-zA-Z]+', ' ', sentence).strip() for sentence in tokenizer.tokenize(text)]
            category_sentences.extend(sentences)

    features = indicoio.text_features(category_sentences, batch=True)
    dataset[category].extend(features)

data = []
target = []

for key in categories:
    category_sentences = dataset[key]
    data.extend(category_sentences)
    target.extend([categories.index(key)] * len(category_sentences))

data = np.asarray(data, np.float32)
target = np.asarray(target, np.float32)

np.savez('dataset.htn', data=data, target=target)

# print("Data Shape:", data.shape)
# print("Target Shape:", target.shape)
#
# X_train, X_test, y_train, y_test = train_test_split(data, target,
#                                                     train_size=0.9, test_size=0.1)
#
# tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)
# tpot.fit(X_train, y_train)
# print(tpot.score(X_test, y_test))
# tpot.export('classifier.py')
