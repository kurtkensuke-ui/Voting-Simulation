import pandas as pd


def simulate_rank_votes(
    bands,
    audience,
    voting_method
):
    """
    順位投票をシミュレーションする。
    """

    results = []

    for _, person in audience.iterrows():

        scores = voting_method(
            bands,
            person
        )

        for band_name, score in scores.items():

            if score is not None:

                results.append({
                    "観客ID": person["観客ID"],
                    "投票先": band_name,
                    "点数": score
                })

    return pd.DataFrame(results)


def run_rank_simulation(
    simulation_count,
    num_bands,
    num_audience,
    cheating_rate,
    pattern,
    voting_method
):
    """
    順位投票専用シミュレーション。

    各バンドを実際に見た人の
    平均点を最終結果とする。
    """

    from band_model import create_bands
    from audience_model import create_audience

    total_voting_rate = 0
    top_band_match_count = 0
    total_rank_match_rate = 0

    for _ in range(simulation_count):

        # ========================================
        # バンド作成
        # ========================================

        bands, _ = create_bands(
            num_bands=num_bands,
            pattern=pattern
        )

        # ========================================
        # 観客作成
        # ========================================

        audience = create_audience(
            bands=bands,
            num_audience=num_audience,
            cheating_rate=cheating_rate
        )

        # ========================================
        # 順位投票
        # ========================================

        voting_results = simulate_rank_votes(
            bands=bands,
            audience=audience,
            voting_method=voting_method
        )

        # ========================================
        # バンドごとの平均点
        # ========================================

        vote_counts = (
            voting_results
            .groupby("投票先")["点数"]
            .mean()
            .reindex(
                [band["name"] for band in bands]
            )
        )

        # ========================================
        # 実力1位と結果1位
        # ========================================

        strongest_band = bands[0]["name"]

        highest_score = vote_counts.max()

        vote_winners = vote_counts[
            vote_counts == highest_score
        ].index.tolist()

        if strongest_band in vote_winners:
            top_band_match_count += 1

        # ========================================
        # 実力順位と結果順位
        # ========================================

        ability_order = [
            band["name"]
            for band in bands
        ]

        result_order = (
            vote_counts
            .sort_values(ascending=False)
            .index
            .tolist()
        )

        rank_matches = 0

        for ability_rank, band_name in enumerate(
            ability_order
        ):

            if band_name not in result_order:
                continue

            result_rank = result_order.index(
                band_name
            )

            if ability_rank == result_rank:
                rank_matches += 1

        rank_match_rate = (
            rank_matches
            / num_bands
            * 100
        )

        total_rank_match_rate += rank_match_rate

        # ========================================
        # 投票率
        # ========================================

        voting_people = (
            voting_results["観客ID"]
            .nunique()
        )

        voting_rate = (
            voting_people
            / num_audience
            * 100
        )

        total_voting_rate += voting_rate

    return {
        "平均投票率":
            total_voting_rate
            / simulation_count,

        "実力1位＝結果1位率":
            top_band_match_count
            / simulation_count
            * 100,

        "実力順位と結果順位の平均一致率":
            total_rank_match_rate
            / simulation_count
    }