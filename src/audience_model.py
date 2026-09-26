import random
import pandas as pd


def create_audience(
    bands,
    num_audience=500,
    cheating_rate=0.05,
    ability_weight=None
):

    audience = []

    # バンド数を取得
    num_bands = len(bands)

    # ========================================
    # ability_weightの確認
    # ========================================

    if ability_weight is not None:

        if not 0 <= ability_weight <= 100:
            raise ValueError(
                "ability_weightは0～100で指定してください"
            )

    # ========================================
    # 観客作成
    # ========================================

    for audience_id in range(
        1,
        num_audience + 1
    ):

        # ========================================
        # 見始める・見終わるバンド
        # ========================================

        start_band = random.randint(
            1,
            num_bands
        )

        end_band = random.randint(
            start_band,
            num_bands
        )


        # ========================================
        # 実際に見たバンド
        # ========================================

        viewed_bands = [
            band
            for band in bands
            if (
                start_band
                <= band["performance_order"]
                <= end_band
            )
        ]


        # ========================================
        # 好きなバンド
        # ========================================

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
        # 実力重視度・好きなバンド補正
        # ========================================

        if favorite_band is None:

            # 好きなバンドがいない場合
            audience_ability_weight = 100
            audience_favorite_weight = 0

        elif ability_weight is None:

            # 指定なし → 観客ごとにランダム
            audience_ability_weight = random.randint(
                0,
                100
            )

            audience_favorite_weight = (
                100
                - audience_ability_weight
            )

        else:

            # 指定値
            audience_ability_weight = ability_weight

            audience_favorite_weight = (
                100
                - ability_weight
            )


        # ========================================
        # 不正投票
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
            "実力重視度": audience_ability_weight,
            "好きなバンド": favorite_band,
            "好きなバンド補正":
                audience_favorite_weight,
            "不正投票": cheating
        })


    return pd.DataFrame(audience)


if __name__ == "__main__":

    from band_model import create_bands

    bands, pattern = create_bands(5)

    audience = create_audience(
        bands=bands,
        num_audience=500,
        cheating_rate=0.05,

        # ========================================
        # ここで指定
        # ========================================

        # None → 観客ごとにランダム
        # 0    → 好きなバンド100%
        # 50   → 実力50%、好きなバンド50%
        # 100  → 実力100%

        ability_weight=None
    )

    print(audience)