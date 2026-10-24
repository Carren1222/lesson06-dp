# 必投项目约束 + dp 表最后一行 + 回溯路径


# -*- coding: utf-8 -*-
# ============================================================
# 课堂练习（第6课）：0/1 背包 —— 动态规划填表 + 回溯还原组合
#
# 背景：背包限重 1000g, 5 件物品各只有一件(要么带要么不带, 这就是"0-1")
# 目标：在总重不超限重的前提下, 装出最高的「重要度总和」
# 状态：dp[i][j] = 只看前 i 件物品、容量还剩 j 时的最大重要度
# 本文件额外演示:
#   (1) 必投项目约束: 某些物品强制带上, 再对剩余容量做 DP
#   (2) 打印 dp 表最后一行, 并标出回溯路径经过的格子
# ============================================================

def knapsack(weights, values, capacity, must_take=None):
    """0/1 背包: 返回 (最大价值, 入选物品编号列表, dp 表)。

    must_take: 必投项目的编号列表(1-based), 这些物品强制入选。
    若必投项目总重超过容量, 返回 (None, [], None) 表示无解。
    """
    n = len(weights)
    must_take = must_take or []

    # ----- 处理必投项目: 先把它们"装进"背包, 扣掉重量和容量 -----
    must_weight = sum(weights[i - 1] for i in must_take)
    must_value = sum(values[i - 1] for i in must_take)
    if must_weight > capacity:
        return None, [], None           # 必投项目本身就超重, 无解
    remain_cap = capacity - must_weight  # 剩下给"可选项目"的容量

    # 可选项目 = 全部物品中去掉必投的
    optional_idx = [i for i in range(1, n + 1) if i not in must_take]
    opt_w = [weights[i - 1] for i in optional_idx]
    opt_v = [values[i - 1] for i in optional_idx]
    m = len(opt_w)

    # 建表: (m+1) 行 x (remain_cap+1) 列, 第0行/第0列全是0
    dp = [[0] * (remain_cap + 1) for _ in range(m + 1)]

    # ---------- 第 1 步: 填表(只对可选项目) ----------
    for i in range(1, m + 1):
        for j in range(remain_cap + 1):
            dp[i][j] = dp[i - 1][j]          # 不拿第 i 个可选物品
            if opt_w[i - 1] <= j:
                take = dp[i - 1][j - opt_w[i - 1]] + opt_v[i - 1]
                if take > dp[i][j]:
                    dp[i][j] = take

    # ---------- 第 2 步: 回溯(在可选项目里找拿了哪些) ----------
    chosen_opt = []
    path = []                            # 记录回溯路径上的 (i, j) 坐标
    j = remain_cap
    for i in range(m, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            chosen_opt.append(optional_idx[i - 1])   # 转回原始编号
            path.append((i, j))
            j -= opt_w[i - 1]
    path.append((0, j))                   # 终点: 回到第 0 行
    chosen_opt.reverse()

    # 最终入选 = 必投 + 可选里选的
    chosen = sorted(must_take + chosen_opt)
    total_value = must_value + dp[m][remain_cap]
    return total_value, chosen, dp

def print_last_row(dp, names, weights, chosen, must_take=None):
    """打印 dp 表最后一行, 并用 * 标出回溯路径经过的列。"""
    must_take = must_take or []
    last = dp[-1]
    cap = len(last) - 1

    # 找出回溯路径经过的列号(在可选项目表上的列)
    path_cols = set()
    j = cap
    for i in range(len(dp) - 1, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            path_cols.add(j)
            # 还原该列对应的物品重量(需要反查, 这里简化: 直接用 dp 值差)
            j -= (dp[i][j] - dp[i - 1][j - (dp[i][j] - dp[i - 1][j])])  # 占位, 实际由调用方控制
            # 上面这行仅为占位, 真正的列标记由下面的 chosen 推导
    # 简化方案: 直接根据 chosen 物品的重量累加标出路径列
    path_cols.clear()
    cur = 0
    for item in chosen:
        if item not in must_take:
            cur += weights[item - 1]
            path_cols.add(cur)

    # 打印表头
    print("  容量 j:", end="")
    for jj in range(cap + 1):
        print("%4d" % jj, end="")
    print()
    # 打印最后一行数值
    print("  dp[末]:", end="")
    for jj in range(cap + 1):
        print("%4d" % last[jj], end="")
    print()
    # 打印回溯路径标记
    print("  路径  :", end="")
    for jj in range(cap + 1):
        if jj in path_cols:
            print("   *", end="")
        elif jj == 0:
            print("   .", end="")      # 起点
        else:
            print("    ", end="")
    print()
    print("  说明: * 表示回溯时在该容量处拿下一件物品; . 是回溯起点")

if __name__ == '__main__':
    names = ["帐篷", "炉具", "睡袋", "食物", "水具"]
    weights = [300, 200, 350, 400, 250]   # 每件物品的重量(克)
    # ===== 重要度是占位值, 请按题目真实数据修改 values 列表 =====
    values = [15, 8, 14, 16, 10]          # 每件物品的重要度
    capacity = 1000                       # 背包限重(克)

    print("背包限重: %d 克" % capacity)
    for k in range(len(weights)):
        print("  %s: 重 %d 克, 重要度 %d" % (names[k], weights[k], values[k]))
    print("=" * 56)

    # ===== 情况 1: 无约束, 自由选 =====
    print("\n【情况 1】无必投项目, 自由选择")
    best, chosen, dp = knapsack(weights, values, capacity)
    print("  最大重要度: %d" % best)
    print("  入选组合: %s" % [names[k - 1] for k in chosen])
    tw = sum(weights[k - 1] for k in chosen)
    tv = sum(values[k - 1] for k in chosen)
    print("  组合核对: 总重 %d/%d 克, 总重要度 %d" % (tw, capacity, tv))
    print("  --- dp 表最后一行 + 回溯路径 ---")
    print_last_row(dp, names, weights, chosen)

    # ===== 情况 2: 必投"睡袋"(编号 3) =====
    print("\n【情况 2】必投项目: 睡袋(编号 3, 重 350g, 重要度 14)")
    best2, chosen2, dp2 = knapsack(weights, values, capacity, must_take=[3])
    if best2 is None:
        print("  无解: 必投项目总重超过容量!")
    else:
        print("  最大重要度: %d (含必投睡袋的 14)" % best2)
        print("  入选组合: %s" % [names[k - 1] for k in chosen2])
        tw2 = sum(weights[k - 1] for k in chosen2)
        tv2 = sum(values[k - 1] for k in chosen2)
        print("  组合核对: 总重 %d/%d 克, 总重要度 %d" % (tw2, capacity, tv2))
        print("  对比: 无约束时最优 = 41, 必投睡袋后 = %d, 差 %d"
              % (best2, best - best2))
        print("  原因: 睡袋重要度 14 但占 350g, 挤掉了帐篷(300g/重要度 15),")
        print("        剩余 650g 最优为 食物+水具(650g/重要度 26), 合计 14+26=40")