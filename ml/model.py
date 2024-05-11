from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from ml.LGD_model import LGDModel


@dataclass
class LGDPrediction:
    """Возвращает датафрейм айдшников и скоров"""

    pred: str

    class Config:
        arbitrary_types_allowed = True


def load_model():
    """

    Returns:
        model (function): функция, которая берет датафрейм и возвращает посчитаннный скор
    """
    model_ = LGDModel()

    def model(df: pd.DataFrame) -> LGDPrediction:

        pred_ = model_.make_prediction(df)
        return LGDPrediction(
            pred=pred_
        )

    return model