import random
import pandas as pd


def vote_full_view(bands, audience):
    """
    投票方法①

    最初のバンドから最後のバンドまで
    全バンドを見た観客だけが投票できる。
    """

    num_bands = len(bands)

    if (
        audience["見始めたバンド"] != 1
        or audience["見終わったバンド"] != num_bands
    ):
        return None

    # 不正投票の場合
    if audience["不正投票"] == 1:
        return audience["好きなバンド"]

    scores = []

    for band in bands:

        ability_score = (
            band["ability"]
            * audience["実力重視度"]
            / 100
        )

        if band["name"] == audience["好きなバンド"]:
            favorite_score = audience["好きなバンド補正"]
        else:
            favorite_score = 0

        total_score = (
            ability_score
            + favorite_score
        )

        scores.append({
            "name": band["name"],
            "score": total_score
        })

    max_score = max(
        item["score"]
        for item in scores
    )

    candidates = [
        item["name"]
        for item in scores
        if item["score"] == max_score
    ]

    selected_band = random.choice(candidates)

    return selected_band


# ========================================
# 顧問票を加える投票方法
# ========================================

def vote_with_advisor_top(bands, audience):
    """
    投票方法②

    通常の投票に加えて、
    顧問票10票を実力1位のバンドに加える。
    """

    return vote_full_view(bands, audience)


def vote_with_advisor_distribution(bands, audience):
    """
    投票方法③

    通常の投票に加えて、
    顧問票10票を実力値の割合で各バンドに配分する。
    """

    return vote_full_view(bands, audience)


# ========================================
# いつでも投票できる方法
# ========================================

def vote_anytime(bands, audience):
    """
    投票方法④

    全員に基本1票の投票権がある。

    通常の観客：
        自分が見たバンドの中から投票する。

    不正投票：
        1～5票を持ち、すべて好きなバンドに投票する。
    """

    # 不正投票
    if audience["不正投票"] == 1:

        vote_count = random.randint(1, 5)

        return [
            audience["好きなバンド"]
            for _ in range(vote_count)
        ]

    # 通常投票
    viewed_bands = [
        band
        for band in bands
        if (
            audience["見始めたバンド"]
            <= band["performance_order"]
            <= audience["見終わったバンド"]
        )
    ]

    scores = []

    for band in viewed_bands:

        ability_score = (
            band["ability"]
            * audience["実力重視度"]
            / 100
        )

        if band["name"] == audience["好きなバンド"]:
            favorite_score = audience["好きなバンド補正"]
        else:
            favorite_score = 0

        total_score = (
            ability_score
            + favorite_score
        )

        scores.append({
            "name": band["name"],
            "score": total_score
        })

    max_score = max(
        item["score"]
        for item in scores
    )

    candidates = [
        item["name"]
        for item in scores
        if item["score"] == max_score
    ]

    selected_band = random.choice(candidates)

    return [selected_band]


# ========================================
# 順位投票
# ========================================

def vote_rank(bands, audience, apply_min_rank=True):
    """
    投票方法⑤⑥

    見たバンドに順位をつける。

    1位 = 最も高い点数
    2位 = 次に高い点数
    ・・・

    apply_min_rank=True：
        見ていないバンドにも最低順位を適用する。

    apply_min_rank=False：
        見ていないバンドには点数を与えない。
    """

    viewed_bands = [
        band
        for band in bands
        if (
            audience["見始めたバンド"]
            <= band["performance_order"]
            <= audience["見終わったバンド"]
        )
    ]

    scores = {}

    # 見たバンドを実力＋好みで評価
    band_scores = []

    for band in viewed_bands:

        ability_score = (
            band["ability"]
            * audience["実力重視度"]
            / 100
        )

        if band["name"] == audience["好きなバンド"]:
            favorite_score = audience["好きなバンド補正"]
        else:
            favorite_score = 0

        total_score = (
            ability_score
            + favorite_score
        )

        band_scores.append({
            "name": band["name"],
            "score": total_score
        })

    # 評価値の高い順に並べる
    band_scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # 順位を点数に変換
    for rank, band in enumerate(
        band_scores,
        start=1
    ):
        scores[band["name"]] = (
            len(viewed_bands) - rank + 1
        )

    # 見ていないバンドにも最低順位を与える
    if apply_min_rank:

        minimum_score = 1

        for band in bands:

            if band["name"] not in scores:
                scores[band["name"]] = minimum_score

    return scores


# ========================================
# 投票シミュレーション
# ========================================

def simulate_votes(bands, audience, voting_method):
    """
    指定された投票方法で、
    全観客の投票をシミュレーションする。
    """

    results = []

    for _, person in audience.iterrows():

        selected_band = voting_method(
            bands,
            person
        )

        # 複数票に対応
        if isinstance(selected_band, list):

            for band_name in selected_band:

                results.append({
                    "観客ID": person["観客ID"],
                    "投票権": True,
                    "投票先": band_name
                })

        else:

            results.append({
                "観客ID": person["観客ID"],
                "投票権": selected_band is not None,
                "投票先": selected_band
            })

    return pd.DataFrame(results)


# ========================================
# シミュレーション
# ========================================

def run_simulation(
    simulation_count,
    num_bands,
    num_audience,
    cheating_rate,
    pattern,
    voting_method
):
    """
    指定された条件でシミュレーションを複数回行い、
    平均結果を返す。
    """

    total_voting_rate = 0
    top_band_match_count = 0
    total_rank_match_rate = 0

    for _ in range(simulation_count):

        # バンドを作成
        bands, _ = create_bands(
            num_bands=num_bands,
            pattern=pattern
        )

        # 観客を作成
        audience = create_audience(
            bands=bands,
            num_audience=num_audience,
            cheating_rate=cheating_rate
        )

        # 投票
        voting_results = simulate_votes(
            bands=bands,
            audience=audience,
            voting_method=voting_method
        )

        # ========================================
        # 投票率
        # ========================================

        total_votes = len(voting_results)

        voting_rate = (
            total_votes
            / num_audience
            * 100
        )

        total_voting_rate += voting_rate

        # ========================================
        # 得票数
        # ========================================

        vote_counts = (
            voting_results["投票先"]
            .value_counts()
            .reindex(
                [band["name"] for band in bands],
                fill_value=0
            )
        )

        # ========================================
        # 実力1位と得票1位
        # ========================================

        strongest_band = bands[0]["name"]

        highest_votes = vote_counts.max()

        vote_winners = vote_counts[
            vote_counts == highest_votes
        ].index.tolist()

        if strongest_band in vote_winners:
            top_band_match_count += 1

        # ========================================
        # 実力順位と得票順位
        # ========================================

        ability_order = [
            band["name"]
            for band in bands
        ]

        vote_order = (
            vote_counts
            .sort_values(ascending=False)
            .index
            .tolist()
        )

        rank_matches = 0

        for ability_rank, band_name in enumerate(
            ability_order
        ):
            vote_rank = vote_order.index(band_name)

            if ability_rank == vote_rank:
                rank_matches += 1

        rank_match_rate = (
            rank_matches
            / num_bands
            * 100
        )

        total_rank_match_rate += rank_match_rate

    # ========================================
    # 平均値
    # ========================================

    average_voting_rate = (
        total_voting_rate
        / simulation_count
    )

    top_band_match_rate = (
        top_band_match_count
        / simulation_count
        * 100
    )

    average_rank_match_rate = (
        total_rank_match_rate
        / simulation_count
    )

    return {
        "平均投票率": average_voting_rate,
        "実力1位＝得票1位率": top_band_match_rate,
        "実力順位と得票順位の平均一致率": average_rank_match_rate
    }


if __name__ == "__main__":

    from band_model import create_bands
    from audience_model import create_audience


    # ========================================
    # シミュレーション条件
    # ========================================

    simulation_count = 1000
    num_bands = 5
    num_audience = 500
    cheating_rate = 0.8
    pattern = "random"

    voting_method = vote_full_view


    # ========================================
    # シミュレーション実行
    # ========================================

    results = run_simulation(
        simulation_count=simulation_count,
        num_bands=num_bands,
        num_audience=num_audience,
        cheating_rate=cheating_rate,
        pattern=pattern,
        voting_method=voting_method
    )


    # ========================================
    # 結果表示
    # ========================================

    print("\n==============================")
    print("シミュレーション結果")
    print("==============================")

    print(f"\nシミュレーション回数：{simulation_count}回")
    print(f"バンド数：{num_bands}組")
    print(f"観客数：{num_audience}人")
    print(f"不正投票率：{cheating_rate * 100:.1f}%")

    print("\n投票方法")
    print(voting_method.__name__)

    print("\n実力パターン")
    print(pattern)

    print("\n平均投票率")
    print(f"{results['平均投票率']:.2f}%")

    print("\n実力1位＝得票1位率")
    print(f"{results['実力1位＝得票1位率']:.2f}%")

    print("\n実力順位と得票順位の平均一致率")
    print(f"{results['実力順位と得票順位の平均一致率']:.2f}%")