import random
import pandas as pd


def vote_full_view(bands, audience):
    """
    投票方法①

    最初のバンドから最後のバンドまで
    全バンドを見た観客だけが投票できる。

    通常投票：
        実力と好みから評価値を計算し、
        評価値が最も高いバンドに投票する。

    不正投票：
        評価値を考慮せず、好きなバンドに投票する。
    """

    num_bands = len(bands)

    # 最初から最後まで見た観客か確認
    if (
        audience["見始めたバンド"] != 1
        or audience["見終わったバンド"] != num_bands
    ):
        return None

    # 不正投票の場合
    if audience["不正投票"] == 1:
        return audience["好きなバンド"]

    scores = []

    # 各バンドの評価値を計算
    for band in bands:

        # 実力による評価
        ability_score = (
            band["ability"]
            * audience["実力重視度"]
            / 100
        )

        # 好きなバンドによる評価
        if band["name"] == audience["好きなバンド"]:
            favorite_score = audience["好きなバンド補正"]
        else:
            favorite_score = 0

        # 総合評価値
        total_score = (
            ability_score
            + favorite_score
        )

        scores.append({
            "name": band["name"],
            "score": total_score
        })

    # 最大評価値を取得
    max_score = max(
        item["score"]
        for item in scores
    )

    # 最大評価値のバンドを取得
    candidates = [
        item["name"]
        for item in scores
        if item["score"] == max_score
    ]

    # 同点の場合はランダムに決定
    selected_band = random.choice(candidates)

    return selected_band


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

        results.append({
            "観客ID": person["観客ID"],
            "投票権": selected_band is not None,
            "投票先": selected_band
        })

    return pd.DataFrame(results)


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

        total_votes = (
            voting_results["投票先"]
            .notna()
            .sum()
        )

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
        # 実力1位と得票1位の一致
        # ========================================

        strongest_band = bands[0]["name"]

        highest_votes = vote_counts.max()

        vote_winners = vote_counts[
            vote_counts == highest_votes
        ].index.tolist()

        if strongest_band in vote_winners:
            top_band_match_count += 1

        # ========================================
        # 実力順位と得票順位の一致率
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
    cheating_rate = 0.05
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