import random
import pandas as pd


def calculate_score(band, audience):
    """
    1人の観客から見た、1つのバンドの評価値を計算する。

    評価値 =
        実力 × 実力重視度
        ＋
        好み × 好きなバンド補正
    """

    ability_score = (
        band["ability"]
        * audience["実力重視度"]
        / 100
    )

    if band["name"] == audience["好きなバンド"]:
        favorite_score = audience["好きなバンド補正"]
    else:
        favorite_score = 0

    total_score = ability_score + favorite_score

    return total_score


def vote(bands, audience):
    """
    全バンドを最後まで見た観客が1バンドに投票する。

    投票権：
        見始めたバンド == 1
        かつ
        見終わったバンド == バンド数

    それ以外の観客には投票権を与えない。
    """

    num_bands = len(bands)

    # 最初から最後まで見たか確認
    if (
        audience["見始めたバンド"] != 1
        or audience["見終わったバンド"] != num_bands
    ):
        return None

    scores = []

    for band in bands:
        score = calculate_score(band, audience)

        scores.append({
            "name": band["name"],
            "score": score
        })

    # 最も評価値の高いバンドを取得
    max_score = max(item["score"] for item in scores)

    candidates = [
        item["name"]
        for item in scores
        if item["score"] == max_score
    ]

    # 評価値が同じ場合はランダムに決定
    selected_band = random.choice(candidates)

    return selected_band


def simulate_votes(bands, audience):
    """
    全観客について投票をシミュレーションする。
    """

    results = []

    for _, person in audience.iterrows():

        selected_band = vote(bands, person)

        results.append({
            "観客ID": person["観客ID"],
            "投票権": selected_band is not None,
            "投票先": selected_band
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    from band_model import create_bands
    from audience_model import create_audience

    # バンドを作成
    bands, pattern = create_bands(5)

    # 観客を作成
    audience = create_audience(
        bands=bands,
        num_audience=500,
        cheating_rate=0.05
    )

    # 投票を実行
    voting_results = simulate_votes(
        bands=bands,
        audience=audience
    )

    print("\n投票結果")
    print(voting_results)

    print("\n各バンドの得票数")

    vote_counts = (
        voting_results["投票先"]
        .value_counts()
        .reindex(
            [band["name"] for band in bands],
            fill_value=0
        )
    )

    print(vote_counts)