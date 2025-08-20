from typing import Literal, TypeAlias

FeatureLabel: TypeAlias = Literal["メッセージ展開", "投票", "その他", "ヘルプ"]
FEATURE_LABEL_LIST: list[FeatureLabel] = [
    "メッセージ展開",
    "投票",
    "その他",
    "ヘルプ",
]
