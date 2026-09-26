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
cheating_rate = 0.05
pattern = "random"
ability_weight=None


# ========================================
# 使用する投票方法
# ========================================

voting_method = vote_full_view

# 顧問票
# None
# "top"
# "distribution"

advisor_mode = None


# ========================================
# 順位投票かどうか
# ========================================

rank_methods = [
    vote_rank_min,
    vote_rank_no_min
]


# ========================================
# シミュレーション実行
# ========================================

if voting_method in rank_methods:

    results = run_rank_simulation(
        simulation_count=simulation_count,
        num_bands=num_bands,
        num_audience=num_audience,
        cheating_rate=cheating_rate,
        pattern=pattern,
        voting_method=voting_method,
        ability_weight=ability_weight
    )

else:

    results = run_simulation(
        simulation_count=simulation_count,
        num_bands=num_bands,
        num_audience=num_audience,
        cheating_rate=cheating_rate,
        pattern=pattern,
        voting_method=voting_method,
        advisor_mode=advisor_mode,
        ability_weight=ability_weight
    )


# ========================================
# 結果表示
# ========================================

print("\n==============================")
print("シミュレーション結果")
print("==============================")

print(
    f"\nシミュレーション回数："
    f"{simulation_count}回"
)

print(f"バンド数：{num_bands}組")
print(f"観客数：{num_audience}人")

print(
    f"不正投票率："
    f"{cheating_rate * 100:.1f}%"
)

print("\n投票方法")
print(voting_method.__name__)

if advisor_mode == "top":
    print("顧問票：実力1位に10票")

elif advisor_mode == "distribution":
    print("顧問票：実力比率で10票を配分")

print("\n実力パターン")
print(pattern)

print("\n平均投票率")
print(
    f"{results['平均投票率']:.2f}%"
)

print("\n実力1位＝結果1位率")
print(
    f"{results['実力1位＝結果1位率']:.2f}%"
)

print("\n実力順位と結果順位の平均一致率")
print(
    f"{results['実力順位と結果順位の平均一致率']:.2f}%"
)