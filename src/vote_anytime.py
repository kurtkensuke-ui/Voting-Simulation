import random


def vote_anytime(bands, audience):
    """
    全員が基本1票投票できる。

    通常の観客：
        自分が見たバンドの中から1票。

    不正投票：
        1～5票を持ち、
        すべて好きなバンドに投票する。
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

    # ========================================
    # 不正投票
    # ========================================

    if audience["不正投票"] == 1:

        if audience["好きなバンド"] is not None:

            vote_count = random.randint(1, 5)

            return [
                audience["好きなバンド"]
                for _ in range(vote_count)
            ]

    # ========================================
    # 通常投票
    # ========================================

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

    return [random.choice(candidates)]