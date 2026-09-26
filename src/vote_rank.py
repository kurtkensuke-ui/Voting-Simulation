def vote_rank(
    bands,
    audience,
    apply_min_rank=True
):
    """
    順位投票。

    5バンドの場合：

    1位：5点
    2位：4点
    3位：3点
    4位：2点
    5位：1点

    見たバンドだけを順位付けする。

    apply_min_rank=True：
        見ていないバンドにも、
        見たバンドの最低点を与える。

    apply_min_rank=False：
        見ていないバンドは評価しない。
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

    # 評価値の高い順
    band_scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    scores = {}

    # ========================================
    # 順位を点数に変換
    # ========================================

    for rank, band in enumerate(
        band_scores,
        start=1
    ):

        point = len(bands) - rank + 1

        scores[band["name"]] = point

    # ========================================
    # 見ていないバンド
    # ========================================

    unseen_bands = [
        band
        for band in bands
        if band["name"] not in scores
    ]

    if apply_min_rank:

        # 見たバンドの最低点
        min_point = min(scores.values())

        for band in unseen_bands:
            scores[band["name"]] = min_point

    else:

        # 見ていないバンドは評価しない
        for band in unseen_bands:
            scores[band["name"]] = None

    return scores


def vote_rank_min(bands, audience):
    """
    順位投票。

    見ていないバンドにも
    見たバンドの最低点を与える。
    """

    return vote_rank(
        bands,
        audience,
        apply_min_rank=True
    )


def vote_rank_no_min(bands, audience):
    """
    順位投票。

    見ていないバンドは評価しない。
    """

    return vote_rank(
        bands,
        audience,
        apply_min_rank=False
    )