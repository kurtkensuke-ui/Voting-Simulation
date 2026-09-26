import pandas as pd


def simulate_votes(
    bands,
    audience,
    voting_method
):
    """
    全観客の投票をシミュレーションする。
    """

    results = []

    for _, person in audience.iterrows():

        selected_band = voting_method(
            bands,
            person
        )

        # 複数票
        if isinstance(selected_band, list):

            for band_name in selected_band:

                results.append({
                    "観客ID": person["観客ID"],
                    "投票先": band_name,
                    "点数": 1
                })

        # 順位投票
        elif isinstance(selected_band, dict):

            for band_name, score in selected_band.items():

                if score is not None:

                    results.append({
                        "観客ID": person["観客ID"],
                        "投票先": band_name,
                        "点数": score
                    })

        # 通常の1票
        else:

            if selected_band is not None:

                results.append({
                    "観客ID": person["観客ID"],
                    "投票先": selected_band,
                    "点数": 1
                })

    return pd.DataFrame(results)


def run_simulation(
    simulation_count,
    num_bands,
    num_audience,
    cheating_rate,
    pattern,
    voting_method,
    advisor_mode=None,
    ability_weight=None
):
    """
    通常の投票方法をシミュレーションする。
    """

    from band_model import create_bands
    from audience_model import create_audience
    from vote_advisor import add_advisor_votes

    total_voting_rate = 0
    top_band_match_count = 0
    total_rank_match_rate = 0

    for _ in range(simulation_count):

        bands, _ = create_bands(
            num_bands=num_bands,
            pattern=pattern
        )

        audience = create_audience(
            bands=bands,
            num_audience=num_audience,
            cheating_rate=cheating_rate
            
        )

        voting_results = simulate_votes(
            bands=bands,
            audience=audience,
            voting_method=voting_method,
            ability_weight=ability_weight
        )

        vote_counts = (
            voting_results
            .groupby("投票先")["点数"]
            .sum()
            .reindex(
                [band["name"] for band in bands],
                fill_value=0
            )
        )

        # 顧問票
        if advisor_mode is not None:

            add_advisor_votes(
                vote_counts,
                bands,
                advisor_mode
            )

        # 投票率
        if len(voting_results) > 0:

            voting_people = (
                voting_results["観客ID"]
                .nunique()
            )

        else:

            voting_people = 0

        voting_rate = (
            voting_people
            / num_audience
            * 100
        )

        total_voting_rate += voting_rate

        # 実力1位と結果1位
        strongest_band = bands[0]["name"]

        highest_score = vote_counts.max()

        vote_winners = vote_counts[
            vote_counts == highest_score
        ].index.tolist()

        if strongest_band in vote_winners:
            top_band_match_count += 1

        # 順位一致率
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

    return {
        "平均投票率":
            total_voting_rate / simulation_count,

        "実力1位＝結果1位率":
            top_band_match_count
            / simulation_count
            * 100,

        "実力順位と結果順位の平均一致率":
            total_rank_match_rate
            / simulation_count
    }