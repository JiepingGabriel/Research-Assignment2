import re
from itertools import combinations
from collections import Counter

# --- 1. 定义你的角色列表 (节点) ---
characters_list = [
    "宝玉", "黛玉", "宝钗",
    "袭人", "鸳鸯", "贾母", "贾政",
    "凤姐", "王夫人", "晴雯", "平儿",
    "湘云", "探春", "迎春", "惜春"
]

# --- 2. 从文件读取原文 ---
file_name = 'Hongloumeng.txt'  # 你保存原文的文件名
raw_text = ''

try:
    # 'utf-8' 编码通常适用于中文
    with open(file_name, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    print(f"成功从 {file_name} 读取文件。")
except FileNotFoundError:
    print(f"错误：找不到文件 '{file_name}'。")
    print("请确保你已经将 Ctext 的原文保存为该文件，并与此脚本放在同一文件夹中。")
    exit()
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    print("请检查文件编码是否为 'utf-8'。")
    exit()

# --- 3. 清理和处理文本 ---
# Ctext 可能有一些特殊字符如 M<...>，我们用正则表达式移除它们
cleaned_text = re.sub(r'M<[0-9a-fA-F]{4}>', '', raw_text)

# 按段落（换行符）分割
paragraphs = cleaned_text.split('\n')

all_interactions = []
print(f"正在分析 {len(paragraphs)} 个段落...")

for para in paragraphs:
    if not para.strip():
        continue

    # 检查这一段里有哪些角色出现了
    present_characters = []
    for char in characters_list:
        if char in para:
            present_characters.append(char)

    # 如果有两个或更多角色在同一段落，则认为他们之间有互动
    if len(present_characters) >= 2:
        # 创建所有可能的配对 (combinations)
        for char_a, char_b in combinations(present_characters, 2):
            # 为保证 A->B 和 B->A 不重复，我们排序
            pair = tuple(sorted((char_a, char_b)))
            all_interactions.append(pair)

# --- 4. 统计互动次数 (边的权重) ---
interaction_counts = Counter(all_interactions)

print(f"分析完成！共找到 {len(interaction_counts)} 种不同的角色配对。")
print("\n" + "=" * 30)

# --- 5. 生成 Gephi 节点表 (Nodes) ---
# 这次我们直接将结果写入文件
nodes_file = 'nodes.csv'
with open(nodes_file, 'w', encoding='utf-8') as f:
    f.write("Id,Label\n")
    for char in characters_list:
        f.write(f"{char},{char}\n")
print(f"已生成节点文件: {nodes_file}")

print("\n" + "=" * 30)

# --- 6. 生成 Gephi 边表 (Edges) ---
# 这次我们也直接将结果写入文件
edges_file = 'edges.csv'
with open(edges_file, 'w', encoding='utf-8') as f:
    f.write("Source,Target,Weight\n")
    for (source, target), weight in interaction_counts.items():
        f.write(f"{source},{target},{weight}\n")
print(f"已生成边文件: {edges_file}")
print("\n" + "=" * 30)

print(f"下一步：请打开 Gephi，导入 '{nodes_file}' 和 '{edges_file}'。")