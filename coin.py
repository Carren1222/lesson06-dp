# 你是有丰富经验的 Python 算法工程师（角色）。 
# 我是 Python 初学者，正在做课堂实验（我的角色）。
# 实现两个函数：coin_greedy(coins, amount) 每步取≤余额的最大面额； coin_dp(coins, amount) 动规求最少枚数。 
# 面额 [1,5,11]、金额 15：两个函数各返回枚数与组合，打印对比（任务）。 
# 带中文注释、单文件、不装第三方库（约束）

# 我需要预算改 800 元，对比结果并解释 10 元的组合

# -*- coding: utf-8 -*-
# ============================================================
# 课堂练习（第6课）：找零钱问题 —— 贪心 vs 动态规划
#
# 面额 [1, 5, 11]，凑 800 元：
#   贪心：72 个 11 + 1 个 5 + 3 个 1 = 76 枚
#   动规：同样 76 枚（800 恰好是贪心也能取最优的金额）
#
# 对比结论：贪心并非总是错；它在 [1,5,11] 面额下，
#   只有当余额落到 "贪心会多拿 11 导致余数被 1 硬凑" 的情况才吃亏
#   （例如 15 元：贪心 5 枚 vs 动规 3 枚）。800 元余数为 8，
#   用 5+1+1+1 正好 4 枚，已是最优，所以两者打平。
# ============================================================

def coin_greedy(coins, amount):
    """贪心法：每一步都取「不超过剩余余额」的最大面额。

    返回 (枚数, 组合列表)；凑不出来时返回 (None, [])。
    """
    coins = sorted(coins, reverse=True)  # 从大到小排序，方便优先拿大的
    used = []                            # 记录每一步拿走的面额
    remain = amount                      # 剩余还没凑够的金额
    while remain > 0:
        pick = None
        for c in coins:                  # coins 已是降序
            if c <= remain:              # 第一个 <= 余额的面额就是最大的
                pick = c
                break
        if pick is None:                 # 所有面额都大于余额 -> 凑不出
            return None, []
        used.append(pick)                # 贪心的关键：只选当前最优
        remain -= pick
    return len(used), used

def coin_dp(coins, amount):
    """动态规划：dp[a] 表示凑出金额 a 所需的最少枚数。

    状态转移：dp[a] = min(dp[a - c] + 1)，c 取遍所有 <= a 的面额
    choice[a] 记录凑 a 时最后用的那枚硬币，用于倒推还原组合。
    """
    INF = float('inf')                   # INF 表示目前还凑不出来
    dp = [0] + [INF] * amount            # dp[0] = 0：凑 0 元需要 0 枚
    choice = [0] * (amount + 1)          # 记录每个金额的最后一枚硬币
    for a in range(1, amount + 1):       # 自底向上：小金额 -> 大金额
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1    # 拿一枚 c，剩余问题变成凑 a-c
                choice[a] = c            # 记下这个选择
    if dp[amount] == INF:                # 无解（例如面额不含 1 且金额很怪）
        return None, []
    combo = []                           # 从 amount 元倒着回溯，还原组合
    a = amount
    while a > 0:
        combo.append(choice[a])
        a -= choice[a]
    return dp[amount], combo

def summarize(combo):
    """把组合列表压缩成"面额 x 次数"的可读形式，避免 800 元时打印一长串。"""
    counts = {}
    for c in combo:
        counts[c] = counts.get(c, 0) + 1
    parts = ["%dx%d" % (c, counts[c]) for c in sorted(counts, reverse=True)]
    return " + ".join(parts)

if __name__ == '__main__':
    coins = [1, 5, 11]
    amount = 800                         # 预算从 15 改为 800

    n_g, combo_g = coin_greedy(coins, amount)
    n_d, combo_d = coin_dp(coins, amount)

    print("面额 =", coins, "  预算 =", amount, "元")
    print("-" * 50)
    print("贪心法   : %d 枚  组合: %s" % (n_g, summarize(combo_g)))
    print("动态规划 : %d 枚  组合: %s" % (n_d, summarize(combo_d)))
    print("-" * 50)

    # 对比解释
    if n_d < n_g:
        print("结论: 贪心吃亏! 多用 %d 枚。原因: 贪心先拿 11, 余数被 1 硬凑" % (n_g - n_d))
        print("      而动规会少拿几个 11, 改用 5 凑, 反而更省。")
    elif n_g < n_d:
        print("结论: 不可能出现这种情况(动规保证最优)。")
    else:
        print("结论: 两者相等, 都是 %d 枚。" % n_g)
        print("      原因: 800 = 72 x 11 + 8, 余数 8 用 5+1+1+1 = 4 枚,")
        print("      恰好已是凑 8 元的最优解, 所以贪心没有走弯路。")

    # 顺带验证 15 元的经典反例, 证明贪心确实会出错
    print()
    print("对照: 面额不变, 预算 = 15 元时")
    n15_g, _ = coin_greedy(coins, 15)
    n15_d, _ = coin_dp(coins, 15)
    print("  贪心 = %d 枚, 动规 = %d 枚  -> 此时贪心才吃亏" % (n15_g, n15_d))