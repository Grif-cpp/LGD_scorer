import pickle
import pandas as pd
import sys
from io import StringIO
import sklearn


class LGDModel(object):
    def __init__(self):
        with open("ml/model.pkl", "rb") as f:
            self.model = pickle.load(f)


    def score(self, df):
        return self.model.predict(df)

    def get_model_info(self):
        feature_names = self.model.feature_names_in_
        feature_importances = self.model.feature_importances_
        return feature_names, feature_importances

    def make_prediction(self, data):
        df = pd.read_csv(data,sep=',')

        for col in df.columns:
            df[col] = df[col].str.replace(',','.')

        feature_cols = self.get_model_info()[0]
        df[feature_cols] = df[feature_cols].astype(float)

        score = df
        score['LGDscore'] = self.score(df[feature_cols]) / 2.2

        return score