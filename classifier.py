import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from tpot.builtins import StackingEstimator

import re
import indicoio

from sklearn.model_selection import train_test_split
import numpy as np

import config

indicoio.config.api_key = config.indico_key()

dataset = np.load('datasets/dataset.htn.npz')
data, target = dataset['data'], dataset['target']

training_features, testing_features, training_target, testing_target = \
    train_test_split(data, target, random_state=42)

exported_pipeline = make_pipeline(
    StackingEstimator(estimator=LogisticRegression(C=20.0)),
    LogisticRegression(C=15.0, dual=True)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)

from sklearn.externals import joblib
joblib.dump(exported_pipeline, 'classifier.pkl')

while True:
    sentence = input("Enter a sentence: ")
    sentence = re.sub('[^0-9a-zA-Z]+', ' ', sentence).strip()

    features = indicoio.text_features(sentence)

    print(exported_pipeline.predict([features]))