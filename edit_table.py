# 你是资深算法工程师；我是要给学生演示算法的讲师（角色变了）。 
# 实现 edit_distance(a, b)，用 kitten → sitting 验证； 
# 要求带逐步填表的讲解：每格打印"插入/删除/替换取最小"的算式， 
# 每填完一行打印一张中间表快照（任务+约束收紧）。


# -*- coding: utf-8 -*-
# ============================================================
# 课堂演示（第6课）：编辑距离（Levenshtein 距离）
#
# 问题：把字符串 a 最少经过几次「插入/删除/替换」能变成 b？
# 经典算例：kitten -> sitting, 答案 = 3
#   kitten -> sitten  (替换 k->s)
#   sitten -> sittin  (替换 e->i)
#   sittin -> sitting (末尾插入 g)
#
# 动规定义：dp[i][j] = a 的前 i 个字符 -> b 的前 j 个字符
#           所需的最少编辑次数
# ============================================================

def show_table(dp, a, b, cur_row):
    """打印 dp 表快照：显示 0~cur_row 行并标 '>'；None 则显示整表无标记"""
    rows = range(len(a) + 1) if cur_row is None else range(cur_row + 1)
    print("      |" + "".join("%4s" % x for x in ["''"] + list(b)))
    print("  " + "-" * (7 + 4 * (len(b) + 1)))
    for i in rows:
        label = a[i - 1] if i > 0 else "''"
        mark = ">" if i == cur_row else " "
        line = " %s %-2s |" % (mark, label)
        line += "".join("%4d" % dp[i][j] for j in range(len(b) + 1))
        print(line)
    print()

def edit_distance(a, b):
    """编辑距离主函数：边填表边打印每格算式，返回最少编辑次数。"""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    print("定义: dp[i][j] = a前i个字符 变成 b前j个字符 的最少编辑次数")
    print("规则1: a[i-1]==b[j-1] 字符相同, 免操作, 直接继承对角")
    print("规则2: 否则在三种操作里取最小 +1:")
    print("   删 = 上格 dp[i-1][j] + 1    插 = 左格 dp[i][j-1] + 1")
    print("   换 = 对角 dp[i-1][j-1] + 1")
    print()

    total = m + 2  # 快照总数 = 空表 1 张 + 初始化 1 张 + 每行 1 张
    print("【快照 1/%d】空表骨架: 行=a的前缀, 列=b的前缀, 全是待填的 0" % total)
    show_table(dp, a, b, None)
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    print("【快照 2/%d】初始化: 第0行=0..%d (空串->b前缀需插j次), 第0列同理" % (total, n))
    show_table(dp, a, b, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                print("dp[%d][%d] (%s->%s): 相同! 直接继承对角 dp[%d][%d] = %d"
                      % (i, j, a[i - 1], b[j - 1], i - 1, j - 1, dp[i][j]))
            else:
                dele = dp[i - 1][j] + 1
                ins = dp[i][j - 1] + 1
                rep = dp[i - 1][j - 1] + 1
                dp[i][j] = min(dele, ins, rep)
                print("dp[%d][%d] (%s->%s): min(删 %d+1, 插 %d+1, 换 %d+1) = %d"
                      % (i, j, a[i - 1], b[j - 1],
                         dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1],
                         dp[i][j]))
        print("【快照 %d/%d】填完第 %d 行 (a 的前 %d 个字符 '%s')" % (i + 2, total, i, i, a[:i]))
        show_table(dp, a, b, i)
    return dp[m][n]

if __name__ == '__main__':
    a, b = "kitten", "sitting"
    print("把 '%s' 变成 '%s', 逐步填表演示:" % (a, b))
    print("=" * 46)
    d = edit_distance(a, b)
    print("=" * 46)
    print("最终答案: edit_distance('%s', '%s') = %d" % (a, b, d))
    if d == 3:
        print("验证通过! 与理论值 3 一致 (替换2次 + 插入1次)")
    else:
        print("警告: 结果 %d 与理论值 3 不符, 请检查!" % d)