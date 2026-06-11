# -*- coding: utf-8 -*-
"""

@author: QWB
"""

import streamlit as st
import pandas as pd

#页面配置
st.set_page_config(layout="wide")


#path
from pathlib import Path
base_dir = Path(__file__).resolve().parents[1]  # streamlit-app
matrix_dir = base_dir / "data_example" / "Matrix.csv"
gene_function_dir = base_dir / "data_example" / "Gene_function.csv"

#read reference
matrix_df = pd.read_csv(matrix_dir, index_col=0)
matrix_df_filtered = matrix_df.drop(columns=['Sex','Age'])

#read gene function reference
gene_function_df= pd.read_csv(gene_function_dir, index_col=0, encoding="utf-8-sig")

#title
# st.title("血液指标相关基因查询")
st.title("Genes related to blood indices")
st.divider()

# st.info("本系统记录了部分血液指标与部分膝骨关节炎软骨核心调控基因的关联，可供科学研究和病理分析使用。")
st.info("This platform contains associations between some blood indices and cartilage hub regulatory genes among Chinese patients with knee osteoarthritis, supporting further research and analysis.")
# blood_indice = st.selectbox("请选择一个血液指标", options = matrix_df_filtered.columns.tolist())
blood_indice = st.selectbox("Select a blood indice", options = matrix_df_filtered.columns.tolist())

if blood_indice:
    series = matrix_df_filtered[blood_indice]
    # 只保留系数 ≠ 0
    related_genes = series[series != 0]
    
    if related_genes.empty:
        # st.warning("该指标未检测到相关基因")
        st.warning("No related genes detected for this indice")
    else:
        result_df = (related_genes.reset_index().
                     drop(columns=blood_indice).
                     rename(columns={"index": "Gene"})
                     )
        merged_result_df = pd.merge(result_df, gene_function_df,on="Gene")
        st.dataframe(merged_result_df,hide_index=True,width='content')
        