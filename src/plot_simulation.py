import matplotlib.pyplot as plt

from voting_model import (
    vote_full_view,
    vote_anytime,
    vote_rank_min,
    vote_rank_no_min
)

from simulation import run_simulation
from simulation_rank import run_rank_simulation


# ========================================
# シミュレーション条件
# ========================================

simulation_count = 1000
num_bands = 5
num_audience = 500
pattern = "random"


# ========================================
# 比較する投票方法
# ========================================

voting_methods = [
    vote_full_view,
    vote_anytime,
    vote_rank_min,
    vote_rank_no_min
]


# ========================================
# 不正投票率の範囲
# ========================================

cheating_rates = [
    0.00,
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.07,
    0.08,
    0.09,
    0.10
]


# ========================================
# シミュレーション実行関数
# ========================================

def run_method(
    voting_method,
    ability_weight,
    cheating_rate
):

    rank_methods = [
        vote_rank_min,
        vote_rank_no_min
    ]

    if voting_method in rank_methods:

        return run_rank_simulation(
            simulation_count=simulation_count,
            num_bands=num_bands,
            num_audience=num_audience,
            cheating_rate=cheating_rate,
            pattern=pattern,
            voting_method=voting_method,
            ability_weight=ability_weight
        )

    else:

        return run_simulation(
            simulation_count=simulation_count,
            num_bands=num_bands,
            num_audience=num_audience,
            cheating_rate=cheating_rate,
            pattern=pattern,
            voting_method=voting_method,
            ability_weight=ability_weight,
            advisor_mode=None
        )


# ========================================
# ① ability_weightの比較
# ========================================

ability_weights = list(range(0, 101, 10))


ability_top_results = {}
ability_rank_results = {}


for voting_method in voting_methods:

    method_name = voting_method.__name__

    ability_top_results[method_name] = []
    ability_rank_results[method_name] = []

    print(
        f"\n{method_name}のability_weight比較中..."
    )

    for weight in ability_weights:

        results = run_method(
            voting_method=voting_method,
            ability_weight=weight,
            cheating_rate=0.05
        )

        ability_top_results[method_name].append(
            results["実力1位＝結果1位率"]
        )

        ability_rank_results[method_name].append(
            results["実力順位と結果順位の平均一致率"]
        )

        print(
            f"ability_weight={weight}: "
            f"1位一致率="
            f"{results['実力1位＝結果1位率']:.2f}% "
            f"順位一致率="
            f"{results['実力順位と結果順位の平均一致率']:.2f}%"
        )


# ========================================
# ability_weight
# 実力1位＝結果1位率
# ========================================

plt.figure(figsize=(10, 6))

for voting_method in voting_methods:

    method_name = voting_method.__name__

    plt.plot(
        ability_weights,
        ability_top_results[method_name],
        marker="o",
        label=method_name
    )

plt.xlabel("Ability Weight")
plt.ylabel("実力1位＝結果1位率（%）")
plt.title(
    "Ability Weightによる実力1位＝結果1位率の変化"
)

plt.xticks(ability_weights)
plt.ylim(0, 100)

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# ========================================
# ability_weight
# 実力順位と結果順位の平均一致率
# ========================================

plt.figure(figsize=(10, 6))

for voting_method in voting_methods:

    method_name = voting_method.__name__

    plt.plot(
        ability_weights,
        ability_rank_results[method_name],
        marker="o",
        label=method_name
    )

plt.xlabel("Ability Weight")
plt.ylabel("実力順位と結果順位の平均一致率（%）")
plt.title(
    "Ability Weightによる実力順位と結果順位の平均一致率の変化"
)

plt.xticks(ability_weights)
plt.ylim(0, 100)

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# ========================================
# ② cheating_rateの比較
# ========================================

cheating_top_results = {}
cheating_rank_results = {}


for voting_method in voting_methods:

    method_name = voting_method.__name__

    cheating_top_results[method_name] = []
    cheating_rank_results[method_name] = []

    print(
        f"\n{method_name}のcheating_rate比較中..."
    )

    for cheating_rate in cheating_rates:

        results = run_method(
            voting_method=voting_method,
            ability_weight=50,
            cheating_rate=cheating_rate
        )

        cheating_top_results[method_name].append(
            results["実力1位＝結果1位率"]
        )

        cheating_rank_results[method_name].append(
            results["実力順位と結果順位の平均一致率"]
        )

        print(
            f"cheating_rate="
            f"{cheating_rate * 100:.0f}%: "
            f"1位一致率="
            f"{results['実力1位＝結果1位率']:.2f}% "
            f"順位一致率="
            f"{results['実力順位と結果順位の平均一致率']:.2f}%"
        )


# ========================================
# cheating_rate
# 実力1位＝結果1位率
# ========================================

plt.figure(figsize=(10, 6))

for voting_method in voting_methods:

    method_name = voting_method.__name__

    plt.plot(
        [
            rate * 100
            for rate in cheating_rates
        ],
        cheating_top_results[method_name],
        marker="o",
        label=method_name
    )

plt.xlabel("Cheating Rate（%）")
plt.ylabel("実力1位＝結果1位率（%）")
plt.title(
    "不正投票率による実力1位＝結果1位率の変化"
)

plt.xticks(
    [
        rate * 100
        for rate in cheating_rates
    ]
)

plt.ylim(0, 100)

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# ========================================
# cheating_rate
# 実力順位と結果順位の平均一致率
# ========================================

plt.figure(figsize=(10, 6))

for voting_method in voting_methods:

    method_name = voting_method.__name__

    plt.plot(
        [
            rate * 100
            for rate in cheating_rates
        ],
        cheating_rank_results[method_name],
        marker="o",
        label=method_name
    )

plt.xlabel("Cheating Rate（%）")
plt.ylabel("実力順位と結果順位の平均一致率（%）")
plt.title(
    "不正投票率による実力順位と結果順位の平均一致率の変化"
)

plt.xticks(
    [
        rate * 100
        for rate in cheating_rates
    ]
)

plt.ylim(0, 100)

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()