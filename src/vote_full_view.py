import random


def vote_full_view(bands, audience):
    """
    最初のバンドから最後のバンドまで
    全バンドを見た観客だけが1票投票する。
    """

    num_bands = len(bands)

    # 全バンドを見ていない場合
    if (
        audience["見始めたバンド"] != 1
        or audience["見終わったバンド"] != num_bands
    ):
        return None

    # 不正投票
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

    return random.choice(candidates)