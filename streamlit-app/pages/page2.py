# -*- coding: utf-8 -*-
"""

@author: QWB
"""

import streamlit as st
import pandas as pd
import joblib
import shap
import numpy as np

#页面配置
st.set_page_config(layout="wide")

#path
from pathlib import Path
base_dir = Path(__file__).resolve().parents[1]  # streamlit-app
model_dir = base_dir / "models"
example_data_dir = base_dir / "data_example" / "example_data.csv"
font_dir = base_dir / "fonts"
font_path = font_dir / "simhei.ttf"

#标题和说明
# st.title("骨关节炎风险评估（批量样本）")
st.title("Knee Osteoarthritis Risk Assessment (Batch Cases)")
st.divider()

#data example
# st.header("数据格式示例：")
st.header("Data Format Example:")
example_df = pd.read_csv(example_data_dir,header=0)

st.dataframe(example_df,hide_index=True)
# st.info("如有缺失值可直接留空，各项指标的输入单位与单个样本模式一致")
st.info("Missing values can be left blank. Units for all indices should match those in the single case input mode.")
st.divider()

#upload file
# st.header("请上传数据文件：")
st.header("Please upload data file:")
# uploaded_file = st.file_uploader("拖拽文件至此或点击选择",type=["csv", "xlsx"])
uploaded_file = st.file_uploader("Drag file here or click to select",type=["csv", "xlsx"])
# st.caption("支持 CSV / Excel 文件")
st.caption("CSV / Excel files")
if uploaded_file is not None:
    # st.success(f"文件上传完成：{uploaded_file.name}")
    st.success(f"File uploaded successfully: {uploaded_file.name}")

#button
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    # predict_button = st.button("评估风险", type="primary")
    predict_button = st.button("Assess Risk", type="primary")

  
    
#predict    
if predict_button:    
    st.divider()
    # st.header("风险评估结果")
    st.header("Risk Assessment Results")
    
    if uploaded_file is None:
        # st.error("请先上传数据文件")
        st.error("Please upload a data file first")
        
    else:
        
        #prepare data
        if uploaded_file.name.endswith(".csv"):
                test_set = pd.read_csv(uploaded_file, header=0, index_col=0)
        elif uploaded_file.name.endswith(".xlsx"):
                test_set = pd.read_excel(uploaded_file, header=0, index_col=0)
        else:
            st.error("Unsupported file format")
            test_set = None
        
        
        test_df = test_set.copy()
        # test_df['性别'] = test_df['性别'].map({'男': 1, '女': 0}).astype(int)
        test_df['Gender'] = test_df['Gender'].map({'Male': 1, 'Female': 0}).astype(int)
        
        
        #check column sequence
        # example_feature_order = example_df.drop(columns=['编号']).columns.tolist()
        example_feature_order = example_df.drop(columns=['ID']).columns.tolist()
        test_df = test_df[example_feature_order]
        st.session_state["test_df_2"] = test_df
        # X_test = test_df.drop(columns=['姓名'])
        X_test = test_df.drop(columns=['Name'])
        
        #-----perform imputation on features-----
        # features = [col for col in X_test.columns if col not in ['年龄','性别']]
        features = [col for col in X_test.columns if col not in ['Age','Gender']]
        if len(features) !=0:
            # perform imputation
            imputer=joblib.load(model_dir / "imputer.pkl")
            X_test_imputed = imputer.transform(X_test[features])
            # merge imputed data
            X_test[features] = X_test_imputed
            
        st.session_state["X_test_2"] = X_test
        
        #-----features scaling-----
        scaler = joblib.load(model_dir / "scaler.pkl")
        X_test_scaled = scaler.transform(X_test)
        X_test_scaled =pd.DataFrame(X_test_scaled,columns=X_test.columns)
        st.session_state["X_test_scaled_2"] = X_test_scaled        

        #predict
        ensemble_model=joblib.load(model_dir / "ensemble_model.pkl")
        risk_prob = ensemble_model.predict_proba(X_test_scaled)[:,1]
        
        #save results
        result_df = test_set.copy()
        # result_df["风险概率"] = risk_prob
        result_df["Risk Probability"] = risk_prob
        st.session_state["result_df_2"] = result_df
        
if "result_df_2" in st.session_state:
   # st.success("风险评估完成，详情请见“风险概率”列")
   st.success("The risk assessment has been completed. Please refer to the ‘Risk Probability’ column for further details.")

   #显示结果表
   show_result_df=st.session_state["result_df_2"].copy()
   # show_result_df["风险概率"]=show_result_df["风险概率"].apply(lambda x: f"{x:.2f}")
   show_result_df["Risk Probability"]=show_result_df["Risk Probability"].apply(lambda x: f"{x:.2f} ")
   cols = list(show_result_df.columns)
   # cols.remove("风险概率")
   cols.remove("Risk Probability")
   # cols.insert(1, "风险概率")  
   cols.insert(1, "Risk Probability") 
   from matplotlib.colors import LinearSegmentedColormap
   single_color_cmap = LinearSegmentedColormap.from_list(
    "same_color", ["#fbfbda", "#fbfbda"])
   # show_result_df = show_result_df[cols].reset_index().astype(str).style.background_gradient(subset=["风险概率"],cmap=single_color_cmap)
   show_result_df = show_result_df[cols].astype(str).style.background_gradient(subset=["Risk Probability"],cmap=single_color_cmap)
   st.dataframe(show_result_df,hide_index=True,width="content")

   #下载结果
   result_file = st.session_state["result_df_2"][cols].to_csv(index=True).encode("utf-8-sig")
   col1, col2, col3 = st.columns([3, 1, 1])
   with col3:
       # st.download_button("下载评估结果",data=result_file,
       #                    file_name="评估结果.csv",type="primary")
       st.download_button("Download Results",data=result_file,
                          file_name="Assessment Results.csv",type="primary")
   
   #shap
   st.divider()
   # st.header("解释分析")
   st.header("Interpretation")
   explainer = joblib.load(model_dir / "shap_explainer.pkl")
   shap_values = explainer.shap_values(st.session_state["X_test_scaled_2"])
   
   #set font
   from matplotlib import font_manager, rcParams
   #手动注册字体
   font_manager.fontManager.addfont(font_path)
   font_prop = font_manager.FontProperties(fname=font_path)
   font_name = font_prop.get_name()
   # 设置为全局默认字体
   rcParams['font.family'] = font_name
   rcParams['axes.unicode_minus'] = False
   
   
   # st.subheader("选择一个样本进行局部解释")
   st.subheader("Select one case for local interpretation")
   # sample_id = st.selectbox("请选择样本编号",options=st.session_state["test_df_2"].index)
   sample_id = st.selectbox("Select Patient ID",options=st.session_state["test_df_2"].index)
   # st.info("本系统会对缺失的血液指标自动填充，请谨慎解读解释结果")  
   st.info("This system will automatically fill in missing blood test results. Please interpret the results with caution.") 
   #行号转换
   index_to_pos = {idx: i for i, idx in enumerate(st.session_state["test_df_2"].index)}
   row_pos = index_to_pos[sample_id]
   shap_value = shap_values[row_pos]

   #plot
   force_plot = shap.plots.force(base_value=np.round(explainer.expected_value,2),
                   shap_values=shap_value,
                   features=np.round(st.session_state["X_test_2"].iloc[row_pos],2),
                   feature_names=st.session_state["X_test_scaled_2"].columns,
                   plot_cmap=["#ff4777", "#00e079"])
   import streamlit.components.v1 as components
   html_str = shap.getjs() + force_plot.html()
   components.html(html_str ,width=1000)
   
   # st.warning("若图片显示不全，可直接下载查看")
   st.warning("If the image does not display properly, you can download it.")
   col1, col2, col3 = st.columns([3, 1, 1])
   with col3:
       # st.download_button(label='下载图片',data=html_str,
       #                file_name=f"shap_force_plot_{sample_id}.html",
       #                type="primary")
       st.download_button(label='Download',data=html_str,
                      file_name="shap_force_plot.html",
                      type="primary")
