import random
import pandas as pd


def create_audience(bands, num_audience=500, cheating_rate=0.05):

    audience = []

    # バンド数を取得
    num_bands = len(bands)

    for audience_id in range(1, num_audience + 1):

        # 何番目のバンドから見始めるか
        start_band = random.randint(1, num_bands)

        # 何番目のバンドまで見るか
        end_band = random.randint(start_band, num_bands)

        # 好きなバンドを決める
        # 0は特定の好きなバンドがないことを表す
        favorite_band = random.randint(0, num_bands)

        # 実力重視度と好きなバンド補正
        if favorite_band == 0:
            ability_weight = 100
            favorite_weight = 0
        else:
            ability_weight = random.randint(0, 100)
            favorite_weight = 100 - ability_weight

        # 不正投票を行うか
        cheating = 1 if random.random() < cheating_rate else 0

        audience.append({
            "観客ID": audience_id,
            "見始めたバンド": start_band,
            "見終わったバンド": end_band,
            "実力重視度": ability_weight,
            "好きなバンド": favorite_band,
            "好きなバンド補正": favorite_weight,
            "不正投票": cheating
        })

    return pd.DataFrame(audience)


if __name__ == "__main__":

    from band_model import create_bands

    bands, pattern = create_bands(5)

    audience = create_audience(
        bands=bands,
        num_audience=500,
        cheating_rate=0.05
    )

    print(audience)