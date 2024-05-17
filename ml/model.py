from dataclasses import dataclass
import pandas as pd
from ml.LGD_model import LGDModel


@dataclass
class LGDPrediction:
    """Возвращает датафрейм со скорингом"""
    pred: str
    class Config:
        arbitrary_types_allowed = True

class ModelConnector(object):

    def __init__(self):
        self.model_ = LGDModel()


    def send_and_recieve_data(self, df: pd.DataFrame) -> LGDPrediction:

        pred_ = self.model_.make_prediction(df)
        return LGDPrediction(
            pred=pred_
        )