def add_advisor_votes(
    vote_counts,
    bands,
    advisor_mode
):
    """
    顧問票10票を追加する。

    advisor_mode

    "top":
        実力1位に10票。

    "distribution":
        実力値の割合で10票を配分。
    """

    advisor_votes = 10

    # ========================================
    # 実力1位に10票
    # ========================================

    if advisor_mode == "top":

        strongest_band = bands[0]["name"]

        vote_counts[strongest_band] += advisor_votes

    # ========================================
    # 実力比率で10票
    # ========================================

    elif advisor_mode == "distribution":

        total_ability = sum(
            band["ability"]
            for band in bands
        )

        raw_votes = []

        for band in bands:

            value = (
                band["ability"]
                / total_ability
                * advisor_votes
            )

            raw_votes.append({
                "name": band["name"],
                "value": value
            })

        # 小数点以下を切り捨て
        allocated_votes = 0

        for item in raw_votes:

            votes = int(item["value"])

            vote_counts[item["name"]] += votes

            item["votes"] = votes

            allocated_votes += votes

        # 余った票を小数部分が大きい順に配る
        remaining_votes = (
            advisor_votes
            - allocated_votes
        )

        raw_votes.sort(
            key=lambda x: x["value"] - x["votes"],
            reverse=True
        )

        for i in range(remaining_votes):

            band_name = raw_votes[i]["name"]

            vote_counts[band_name] += 1