import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from tpot.builtins import StackingEstimator

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
print(results)
