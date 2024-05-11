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
        feature_names = self.model.feature_names
        feature_types = self.model.feature_types
        #self.model.get_split_value_histogram()
        return feature_names, feature_types

    def make_prediction(self, data):
        df = pd.read_csv(data,sep=',')

        for col in df.columns:
            df[col] = df[col].str.replace(',','.')

        df = df.astype(float)

        score = df
        score['LGDscore'] = self.score(df)

        return score