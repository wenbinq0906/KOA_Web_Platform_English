# -*- coding: utf-8 -*-
"""
@author: QWB
"""

import streamlit as st

# 页面配置
st.set_page_config(layout="wide")

#标题和说明
# st.title("中国人群膝骨关节炎风险评估系统")
st.title("Knee Osteoarthritis Risk Assessment System for Chinese")

st.divider()

# st.text("""
# 本平台基于机器学习方法，利用血液生化指标，对膝骨关节炎的患病风险进行诊断。除风险评估外，本系统还可为每例输入提供简单的解释分析。

# 本平台包括两个模式，具体模式选择请见侧边栏：

# 1、单个病例输入模式：直接输入一位病人的基本信息和血液生化指标数据
# 2、批量病例输入模式：通过csv文件或excel表一次性输入多位病人的基本信息和血液生化指标数据

# 此外本平台还记录了在中国膝骨关节炎患者群体中，部分血液指标与部分膝骨关节炎软骨核心调控基因的关联，可供科学研究和病理分析使用。
# """)
st.text("""
This platform adopts machine learning algorithms to diagnose the risk of knee osteoarthritis using blood biochemical indices. In addition to risk evaluation, this system provides simple interpretation for each submitted case.

Two input modes are available, which can be selected via the sidebar:

1. Single Case Input Mode: Manually enter data for one case
2. Batch Case Input Mode: Upload a CSV or Excel file to input data for multiple cases at once

Furthermore, this platform contains associations between some blood indices and cartilage hub regulatory genes among Chinese patients with knee osteoarthritis, supporting further research and analysis.
""")

# st.warning("注意：本系统不对任何临床诊断或医疗建议负责。")
st.warning("Warning: This system is not responsible for any clinical diagnosis or medical advice.")

