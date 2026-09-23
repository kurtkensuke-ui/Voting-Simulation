import random
import string


def create_bands(num_bands):
    # 指定した数のバンドを、実力順に作成する

    # 実力差のパターンをランダムに決定
    pattern = random.choice([
        "high",
        "low",
        "upper_close",
        "lower_close",
        "random"
    ])

    # 実力値を生成
    if pattern == "high":
        # 全バンド実力が高い
        ability_values = random.sample(range(70, 101), num_bands)

    elif pattern == "low":
        # 全バンド実力が低い
        ability_values = random.sample(range(1, 51), num_bands)

    elif pattern == "upper_close":
        # 上位数バンドが実力的に拮抗
        upper_count = max(2, num_bands // 2)
        upper_values = random.sample(range(75, 91), upper_count)
        lower_values = random.sample(range(1, 61), num_bands - upper_count)
        ability_values = upper_values + lower_values

    elif pattern == "lower_close":
        # 下位数バンドが実力的に拮抗
        lower_count = max(2, num_bands // 2)
        upper_values = random.sample(range(50, 101), num_bands - lower_count)
        lower_values = random.sample(range(30, 46), lower_count)
        ability_values = upper_values + lower_values

    else:
        # 実力がばらばら
        ability_values = random.sample(range(1, 101), num_bands)

    # 実力値が高い順に並べる
    ability_values.sort(reverse=True)

    bands = []

    for i, ability in enumerate(ability_values):
        band_name = f"バンド{string.ascii_uppercase[i]}"
        bands.append({
            "name": band_name,
            "ability": ability
        })

    # 演奏順をランダムに決定
    performance_order = bands.copy()
    random.shuffle(performance_order)

    # 演奏順を設定
    for i, band in enumerate(performance_order, start=1):
        band["performance_order"] = i

    return bands, pattern


if __name__ == "__main__":
    # ここで実力パターンを指定
    bands, pattern = create_bands(
        num_bands=5,
        pattern="upper_close"
    )
    # パターンの名前
    pattern_names = {
        "high": "全バンド実力が高い",
        "low": "全バンド実力が低い",
        "upper_close": "上位数バンドが拮抗",
        "lower_close": "下位数バンドが拮抗",
        "random": "実力がばらばら"
    }

    print(f"実力パターン: {pattern_names[pattern]}")

    # 実力順
    print("\n実力順")
    for band in bands:
        print(f"{band['name']}: 実力値 {band['ability']}")

    # 演奏順
    print("\n演奏順")
    for band in sorted(bands, key=lambda x: x["performance_order"]):
        print(
            f"{band['performance_order']}番目: "
            f"{band['name']}（実力値 {band['ability']}）"
        )