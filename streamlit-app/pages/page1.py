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
# st.title("骨关节炎风险评估（单个样本）")
st.title("Knee Osteoarthritis Risk Assessment (Single Case)")

st.divider()

#input data
# st.header("请输入病人信息")
st.header("Please enter the patient's blood test result")
# patient id


col1, col2 = st.columns(2)
# patient gender
with col1:
    # patient_id = st.text_input("病人编号：")
    patient_id = st.text_input("Patient ID:")
    # patient_gender = st.selectbox("病人性别：", ["男", "女"])
    patient_gender = st.selectbox("Patient Gender:", ["Male", "Female"])
# patient age
with col2:
    # patient_id = st.text_input("病人编号：")
    patient_name = st.text_input("Patient Name:")
    # patient_age = st.number_input("年龄（岁）",min_value=0,max_value=120)
    patient_age = st.number_input("Age (years)",min_value=0,max_value=120)

st.caption("  ")
st.caption("  ")

#blood indices
col1, col2, col3 = st.columns(3)
with col1:
    patient_Basophil_count = st.number_input("Basophil count (10^9/L)", value=None,step=0.01,format="%.2f")
    patient_Eosinophil_percentage = st.number_input("Eosinophil percentage (%)", value=None,step=0.01,format="%.2f")
    patient_Lymphocyte_count = st.number_input("Lymphocyte count (10^9/L)", value=None,step=0.01,format="%.2f")
    patient_Mean_corpuscular_volume = st.number_input("Mean corpuscular volume (fL)", value=None,step=0.01,format="%.2f")
    patient_Monocyte_percentage = st.number_input("Monocyte percentage (%)", value=None,step=0.01,format="%.2f")
    patient_Platelet_crit = st.number_input("Platelet crit (%)", value=None,step=0.01,format="%.2f")
    patient_Red_blood_cell_distribution_width = st.number_input("Red blood cell (erythrocyte) distribution width CV (%)", value=None,step=0.01,format="%.2f")
    patient_White_blood_cell_count = st.number_input("White blood cell (leukocyte) count (10^9/L)", value=None,step=0.01,format="%.2f")
    patient_Alkaline_phosphatase = st.number_input("Alkaline phosphatase (U/L)", value=None,step=0.01,format="%.2f")
    patient_Aspartate_aminotransferase = st.number_input("Aspartate aminotransferase (U/L)", value=None,step=0.01,format="%.2f")
    patient_Direct_bilirubin = st.number_input("Direct bilirubin (umol/L)", value=None,step=0.01,format="%.2f")
    patient_Total_bilirubin = st.number_input("Total bilirubin (umol/L)", value=None,step=0.01,format="%.2f")
    patient_Urate = st.number_input("Urate (umol/L)", value=None,step=0.01,format="%.2f")
    

with col2:
    patient_Basophil_percentage = st.number_input("Basophil percentage (%)", value=None,step=0.01,format="%.2f")
    patient_Haematocrit_percentage = st.number_input("Haematocrit percentage (%)", value=None,step=0.01,format="%.2f")
    
    patient_Lymphocyte_percentage = st.number_input("Lymphocyte percentage (%)", value=None,step=0.01,format="%.2f")
    
    patient_Neutrophil_count = st.number_input("Neutrophil count (10^9/L)", value=None,step=0.01,format="%.2f")
    patient_Platelet_distribution_width = st.number_input("Platelet distribution width (fL)", value=None,step=0.01,format="%.2f")
    patient_Mean_corpuscular_haemoglobin_concentration = st.number_input("Mean corpuscular haemoglobin concentration (g/L)", value=None,step=0.01,format="%.2f")
    patient_Alanine_aminotransferase = st.number_input("Alanine aminotransferase (U/L)", value=None,step=0.01,format="%.2f")
    patient_Creatinine = st.number_input("Creatinine (umol/L)", value=None,step=0.01,format="%.2f")
    patient_Gamma_glutamyltransferase = st.number_input("Gamma glutamyltransferase (U/L)", value=None,step=0.01,format="%.2f")
    patient_Total_protein = st.number_input("Total protein (g/L)", value=None,step=0.01,format="%.2f")
    patient_Glucose = st.number_input("Glucose (mmol/L)", value=None,step=0.01,format="%.2f")
    patient_Phosphate = st.number_input("Phosphate (mmol/L)", value=None,step=0.01,format="%.2f")

with col3:
    patient_Eosinophil_count = st.number_input("Eosinophil count (10^9/L)", value=None,step=0.01,format="%.2f")
    patient_Haemoglobin_concentration = st.number_input("Haemoglobin concentration (g/L)", value=None,step=0.01,format="%.2f")
    
    patient_Mean_corpuscular_haemoglobin = st.number_input("Mean corpuscular haemoglobin (pg)", value=None,step=0.01,format="%.2f")
    patient_Mean_platelet_volume = st.number_input("Mean platelet (thrombocyte) volume (fL)", value=None,step=0.01,format="%.2f")
    patient_Monocyte_count = st.number_input("Monocyte count (10^9/L)", value=None,step=0.01,format="%.2f")
    patient_Neutrophil_percentage = st.number_input("Neutrophil percentage (%)", value=None,step=0.01,format="%.2f")
    patient_Platelet_count = st.number_input("Platelet count (10^9/L)", value=None,step=0.01,format="%.2f")
    patient_Red_blood_cell_count = st.number_input("Red blood cell (erythrocyte) count (10^12/L)", value=None,step=0.01,format="%.2f")

    patient_Albumin = st.number_input("Albumin (g/L)", value=None,step=0.01,format="%.2f")
    patient_Calcium = st.number_input("Calcium (mmol/L)", value=None,step=0.01,format="%.2f")
    patient_Cystatin_C = st.number_input("Cystatin_C (mg/L)", value=None,step=0.01,format="%.2f")
    patient_Urea = st.number_input("Urea (mmol/L)", value=None,step=0.01,format="%.2f")
    
    

# st.info("如有缺失值可直接留空，请注意各项指标的输入单位。")    
st.info("If any blood indice is missing, just leave it blank. Please note the unit of measurement for each indice.")  
st.divider()

col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    # predict_button = st.button("评估风险", type="primary")
    predict_button = st.button("Assess Risks", type="primary")

input_dict = {
    "ID": patient_id,
    "Name": patient_name,
    "Gender": patient_gender,
    "Age": patient_age,
    
    "Basophil count": patient_Basophil_count,
    "Basophil percentage": patient_Basophil_percentage,
    "Eosinophil count": patient_Eosinophil_count,
    "Eosinophil percentage": patient_Eosinophil_percentage,
    "Lymphocyte count": patient_Lymphocyte_count,
    "Lymphocyte percentage": patient_Lymphocyte_percentage,
    "Monocyte count": patient_Monocyte_count,
    "Monocyte percentage": patient_Monocyte_percentage,
    "Neutrophil count": patient_Neutrophil_count,
    "Neutrophil percentage": patient_Neutrophil_percentage,
    "White blood cell (leukocyte) count": patient_White_blood_cell_count,
    "Red blood cell (erythrocyte) count": patient_Red_blood_cell_count,
    "Haemoglobin concentration": patient_Haemoglobin_concentration,
    "Haematocrit percentage": patient_Haematocrit_percentage,
    "Red blood cell (erythrocyte) distribution width": patient_Red_blood_cell_distribution_width,
    "Mean corpuscular haemoglobin": patient_Mean_corpuscular_haemoglobin,
    "Mean corpuscular haemoglobin concentration": patient_Mean_corpuscular_haemoglobin_concentration,
    "Mean corpuscular volume": patient_Mean_corpuscular_volume,
    "Platelet count": patient_Platelet_count,
    "Mean platelet (thrombocyte) volume": patient_Mean_platelet_volume,
    "Platelet crit": patient_Platelet_crit,
    "Platelet distribution width": patient_Platelet_distribution_width,


    "Albumin": patient_Albumin,
    "Total protein": patient_Total_protein,
    "Calcium": patient_Calcium,
    "Phosphate": patient_Phosphate,
    "Glucose": patient_Glucose,
    "Urea": patient_Urea,
    "Creatinine": patient_Creatinine,
    "Cystatin C": patient_Cystatin_C,
    "Urate": patient_Urate,
    "Alanine aminotransferase": patient_Alanine_aminotransferase,
    "Aspartate aminotransferase": patient_Aspartate_aminotransferase,
    "Alkaline phosphatase": patient_Alkaline_phosphatase,
    "Gamma glutamyltransferase": patient_Gamma_glutamyltransferase,
    "Total bilirubin": patient_Total_bilirubin,
    "Direct bilirubin": patient_Direct_bilirubin
}    

#predict    
if predict_button:    
    
    st.divider()
    # st.header("风险评估结果")
    st.header("Risk Assessment Results")
    
    
    #prepare data
    input_data=pd.DataFrame([input_dict])
    input_data_df = input_data.copy()
    # input_data_df['性别'] = input_data_df['性别'].map({'男': 1, '女': 0}).astype(int)
    input_data_df['Gender'] = input_data_df['Gender'].map({'Male': 1, 'Female': 0}).astype(int)

    #set columns sequence
    example_df = pd.read_csv(example_data_dir,header=0)
    # example_feature_order = example_df.drop(columns=['编号']).columns.tolist()
    example_feature_order = example_df.drop(columns=['ID']).columns.tolist()
    input_data_df = input_data_df[example_feature_order]
    st.session_state["input_data_df"] = input_data_df
    # X_test = input_data_df.drop(columns=['姓名'])
    X_test = input_data_df.drop(columns=['Name'])
    
    
    #-----perform imputation on features-----
    # features = [col for col in X_test.columns if col not in ['年龄','性别']]
    features = [col for col in X_test.columns if col not in ['Age','Gender']]
    if len(features) !=0:
        # perform imputation
        imputer=joblib.load(model_dir / "imputer.pkl")
        X_test_imputed = imputer.transform(X_test[features])
        # merge imputed data
        X_test[features] = X_test_imputed
        
    st.session_state["X_test_1"] = X_test
    
    #-----features scaling-----
    scaler = joblib.load(model_dir / "scaler.pkl")
    X_test_scaled = scaler.transform(X_test)
    X_test_scaled =pd.DataFrame(X_test_scaled,columns=X_test.columns)
    st.session_state["X_test_scaled_1"] = X_test_scaled        

    #predict
    ensemble_model=joblib.load(model_dir / "ensemble_model.pkl")
    risk_prob = ensemble_model.predict_proba(X_test_scaled)[:,1]
    
    #save results
    result_df = input_data.copy()
    # result_df["风险概率"] = risk_prob
    result_df["Risk Probability"] = risk_prob
    st.session_state["result_df_1"] = result_df
        
if "result_df_1" in st.session_state:
   # st.success("风险评估完成，详情请见“风险概率”列")
   st.success("The risk assessment has been completed. Please refer to the ‘Risk Probability’ column for further details.")

   #显示结果表
   show_result_df=st.session_state["result_df_1"].copy()
   # show_result_df["风险概率"]=show_result_df["风险概率"].apply(lambda x: f"{x:.2f}")
   show_result_df["Risk Probability"]=show_result_df["Risk Probability"].apply(lambda x: f"{x:.2f} ")
   cols = list(show_result_df.columns)
   # cols.remove("风险概率")
   cols.remove("Risk Probability")
   # cols.insert(2, "风险概率")   
   cols.insert(2, "Risk Probability")   
   from matplotlib.colors import LinearSegmentedColormap
   single_color_cmap = LinearSegmentedColormap.from_list(
    "same_color", ["#fbfbda", "#fbfbda"])
   # show_result_df = show_result_df[cols].astype(str).style.background_gradient(subset=["风险概率"],cmap=single_color_cmap)
   show_result_df = show_result_df[cols].astype(str).style.background_gradient(subset=["Risk Probability"],cmap=single_color_cmap)
   st.dataframe(show_result_df,hide_index=True,width="content")

   
   #shap
   st.divider()
   # st.header("解释分析")
   st.header("Interpretation")
   # st.info("本系统会对缺失的血液指标自动填充，请谨慎解读解释结果")  
   st.info("This system will automatically fill in missing blood test results. Please interpret the results with caution.") 
   explainer = joblib.load(model_dir / "shap_explainer.pkl")
   shap_values = explainer.shap_values(st.session_state["X_test_scaled_1"])
   
   #set font
   from matplotlib import font_manager, rcParams
   #手动注册字体
   font_manager.fontManager.addfont(font_path)
   font_prop = font_manager.FontProperties(fname=font_path)
   font_name = font_prop.get_name()
   # 设置为全局默认字体
   rcParams['font.family'] = font_name
   rcParams['axes.unicode_minus'] = False

   #plot
   force_plot = shap.plots.force(base_value=np.round(explainer.expected_value,2),
                   shap_values=shap_values[0],
                   features=np.round(st.session_state["X_test_1"].iloc[0,:],2),
                   feature_names=st.session_state["X_test_scaled_1"].columns,
                   plot_cmap=["#ff4777", "#00e079"])
   import streamlit.components.v1 as components
   html_str = shap.getjs() + force_plot.html()
   components.html(html_str ,width=1000)
   
   # st.warning("若图片显示不全，可直接下载查看")
   st.warning("If the image does not display properly, you can download it.")
   col1, col2, col3 = st.columns([3, 1, 1])
   with col3:
       # st.download_button(label='下载图片',data=html_str,
       #                file_name="shap_force_plot.html",
       #                type="primary")
       st.download_button(label='Download',data=html_str,
                      file_name="shap_force_plot.html",
                      type="primary")

    
    
    