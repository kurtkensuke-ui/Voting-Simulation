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


        # ========================================
        # 好きなバンドを決める
        # ========================================

        # 実際に見たバンドだけを候補にする
        viewed_bands = [
            band
            for band in bands
            if start_band
            <= band["performance_order"]
            <= end_band
        ]

        # 好きなバンドがいない場合もある
        favorite_band_number = random.randint(
            0,
            len(viewed_bands)
        )

        if favorite_band_number == 0:
            favorite_band = None
        else:
            favorite_band = viewed_bands[
                favorite_band_number - 1
            ]["name"]


        # ========================================
        # 実力重視度と好きなバンド補正
        # ========================================

        if favorite_band is None:
            ability_weight = 100
            favorite_weight = 0

        else:
            ability_weight = random.randint(0, 100)
            favorite_weight = 100 - ability_weight


        # ========================================
        # 不正投票を行うか
        # ========================================

        cheating = (
            1
            if random.random() < cheating_rate
            else 0
        )


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