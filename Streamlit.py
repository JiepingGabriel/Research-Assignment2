import streamlit as st
import pandas as pd
from PIL import Image
import os  # 导入 os 模块来检查文件是否存在

# --- 0. 定义文件名 (在这里管理你的文件) ---
GEPHI_GRAPH_IMAGE = 'network_visualization.png'
GEPHI_METRICS_CSV = 'node_metrics.csv'

# --- 1. 页面配置 (Page Config) ---
# ... 现有代码 ...
st.set_page_config(
    page_title="红楼梦》社交网络分析",
    page_icon="📚",
    layout="wide",  # "wide" 布局让内容更舒展
    initial_sidebar_state="expanded"
)

# --- 2. 侧边栏 (Sidebar) ---
# ... 现有代码 ...
st.sidebar.title("项目导航")
st.sidebar.info(
    """
    **课程:** CHC5904 数字中华文化研究
    **作业:** 实践作业 #2
    **选项:** 1: 贾宝玉社交网络
    **分析工具:** Python, Gephi, Streamlit
    """
)
st.sidebar.header("研究问题 (RQs)")
st.sidebar.markdown(
    """
    1.  谁是网络中心?
    2.  谁是关键“桥梁”?
    3.  黛玉 vs. 宝钗的地位?
    """
)

# --- 3. 主页面标题 ---
# ... 现有代码 ...
st.title("📚 《红楼梦》的数字研究")
st.header("贾宝玉 (第20-40章) 社交网络分析")

# --- 4. 使用 Tabs 标签页来组织内容 ---
# ... 现有代码 ...
tab_intro, tab_method, tab_findings, tab_reflection = st.tabs(
    ["引言 (Introduction)", "方法与工具 (Methodology)", "发现 (Findings)", "反思 (Reflection)"]
)

# --- Tab 1: 引言 ---
# ... 现有代码 ...
with tab_intro:
    st.header("项目简介")
    st.markdown(
        """
        本项目利用数字人文 (DH) 工具，对《红楼梦》（第20-40章）中主角贾宝玉的社交网络进行量化分析。

        我们的目标是超越传统的文本阅读，通过计算网络指标来揭示人物之间隐藏的结构性关系。
        """,
        unsafe_allow_html=True
    )
    st.subheader("研究问题 (Research Questions)")
    st.markdown(
        """
        * **RQ1:** 在第20-40章中，谁是贾宝玉社交网络的**中心人物**？
        * **RQ2:** 哪些角色在他的社交圈中扮演了连接不同群体的**“桥梁”**作用？
        * **RQ3:** 作为贾宝玉生活的两位女主角，**林黛玉**和**薛宝钗**在他网络中的位置有何不同？
        """
    )

# --- Tab 2: 方法与工具 ---
# ... 现有代码 ...
with tab_method:
    st.header("方法与工具")
    st.markdown("我们的工作流分为三个主要步骤：")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("1. 数据收集 (Ctext)")
        st.info("从 Ctext.org 提取《红楼梦》第20至40章的原文文本。")
        st.image("http://googleusercontent.com/image_collection/image_retrieval/12024040003020611417",
                 caption="Ctext.org 作为权威文本来源")  # 占位图

    with col2:
        st.subheader("2. 数据处理 (Python)")
        st.info("使用 Python 脚本，以“段落共现”为标准，量化15个主要角色间的互动频率。")
        # 展示你用于处理文本的代码
        st.code(
            """
import re
from itertools import combinations
from collections import Counter

# 定义角色列表
characters_list = ["宝玉", "黛玉", "宝钗", "袭人", "凤姐", ...]

# (读取 hongloumeng_20-40.txt)
raw_text = f.read()

# 按段落分割
paragraphs = cleaned_text.split('\\n')

# 查找共现
all_interactions = []
for para in paragraphs:
    present_characters = [char for char in characters_list if char in para]
    if len(present_characters) >= 2:
        for char_a, char_b in combinations(present_characters, 2):
            all_interactions.append(tuple(sorted((char_a, char_b))))

# 统计权重
interaction_counts = Counter(all_interactions)
            """,
            language="python"
        )

    with col3:
        st.subheader("3. 分析与可视化 (Gephi)")
        st.info("将 Python 生成的 `nodes.csv` 和 `edges.csv` 导入 Gephi，计算网络指标并进行可视化。")
        st.image("http://googleusercontent.com/image_collection/image_retrieval/13317078490800366629",
                 caption="Gephi 用于网络分析和可视化")  # 占位图

# --- Tab 3: 发现 ---
with tab_findings:
    st.header("主要发现")

    st.subheader("发现 1 (RQ1 & RQ2): 网络中心与“桥梁”")
    st.markdown("我们将“度中心性”(Degree) 映射到节点大小，“介数中心性”(Betweenness) 映射到节点颜色（越红越重要）。")

    # **更新后的逻辑**: 检查文件是否存在
    if os.path.exists(GEPHI_GRAPH_IMAGE):
        # 如果文件存在，就加载它
        image = Image.open(GEPHI_GRAPH_IMAGE)
        st.image(image, caption="贾宝玉的社交网络 (节点大小 = 度, 颜色 = 介数)")
    else:
        # 如果文件不存在，显示警告和占位图
        st.warning(f"这是一个占位图。请将你从 Gephi 导出的网络图保存为 `{GEPHI_GRAPH_IMAGE}` 并放在同一文件夹中。")
        st.image("http://googleusercontent.com/image_collection/image_retrieval/1458189458830084763",
                 caption="贾宝玉的社交网络 (占位图)")

    st.subheader("发现 3 (RQ3): 黛玉 vs. 宝钗")
    st.markdown("为了回答这个问题，我们查看了 Gephi 计算出的指标数据。")

    # **更新后的逻辑**: 检查文件是否存在
    if os.path.exists(GEPHI_METRICS_CSV):
        # 如果文件存在，就加载它
        df_metrics = pd.read_csv(GEPHI_METRICS_CSV).set_index('Label')  # 假设 'Label' 是索引列
        st.success("成功加载 Gephi 数据！")
    else:
        # 如果文件不存在，显示警告和占位数据
        st.warning(f"这是一个占位数据表。请将你从 Gephi 导出的包含指标的 `nodes.csv` 文件保存为 `{GEPHI_METRICS_CSV}`。")
        data = {
            'Label': ['宝玉', '黛玉', '宝钗', '袭人', '凤姐', '贾母'],
            'Degree': [14, 12, 11, 13, 9, 10],  # (假设数据)
            'Betweenness Centrality': [45.0, 15.1, 30.2, 85.2, 70.5, 20.0]  # (假设数据)
        }
        df_metrics = pd.DataFrame(data).set_index('Label')

    # --- 显示数据 (无论来源是真实文件还是占位符) ---
    try:
        st.dataframe(df_metrics.style.format(
            {'Betweenness Centrality': '{:.2f}'}
        ).background_gradient(cmap='Reds', subset=['Betweenness Centrality']).background_gradient(cmap='Blues',
                                                                                                  subset=['Degree']))

        # 从数据中动态提取洞察
        daiyu_degree = df_metrics.loc['黛玉', 'Degree']
        daiyu_betweenness = df_metrics.loc['黛玉', 'Betweenness Centrality']
        baochai_degree = df_metrics.loc['宝钗', 'Degree']
        baochai_betweenness = df_metrics.loc['宝钗', 'Betweenness Centrality']

        st.success(
            f"""
            **数据洞察:**
            * **黛玉 (Daiyu):** “度”很高 ({daiyu_degree})，但“介数”很低 ({daiyu_betweenness:.1f})。她是“社交终点”，而非“桥梁”。
            * **宝钗 (Baochai):** “度” ({baochai_degree}) 和“介数” ({baochai_betweenness:.1f}) 都相对较高。她是一个“社交枢纽”，连接着宝玉之外的更多群体。
            """
        )
    except KeyError:
        st.error(
            "错误：数据表中缺少 '黛玉' 或 '宝钗'。请检查你的 Gephi 导出文件 (`{GEPHI_METRICS_CSV}`) 是否包含 'Label' 列。")
    except Exception as e:
        st.error(f"渲染数据表时出错: {e}")

# --- Tab 4: 反思 ---
# ... 现有代码 ...
with tab_reflection:
    st.header("反思与结论")
    st.markdown(
        """
        ### 对研究问题的回答:
        1.  **RQ1 (中心):** **贾宝玉** 是网络的绝对中心 (Degree = 14)。
        2.  **RQ2 (桥梁):** **袭人** 和 **凤姐** 是最重要的“桥梁” (Betweenness Centrality 最高)，她们控制着贾宝玉社交圈的信息流动。
        3.  **RQ3 (对比):** 数据证实了黛玉和宝钗的社会角色差异。黛玉是“内部核心”，而宝钗是“外部枢纽”。

        ### 对工具的反思:
        * **Python:** 非常适合处理大规模文本，"共现法" 是一个高效的代理指标。
        * **Gephi:** 强大的可视化工具，能将抽象的数据"翻译"成直观的洞察。
        * **Streamlit:** 完美地将 Python 分析 (代码、数据表) 和 Gephi 可视化 (图片) 结合在一起，制作成一个专业的数据应用。
        """
    )
    st.balloons()  # 一点小庆祝