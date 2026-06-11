# -*- coding: utf-8 -*-
"""
@author: QWB
"""

import streamlit as st



#path
from pathlib import Path
base_dir = Path(__file__).resolve().parent # streamlit-app

LOGO_path = base_dir / "art_materials" / "BIGC_logo.png"
LOGO_bigc = base_dir / "art_materials" / "BIGC.png"
LOGO_xjtu = base_dir / "art_materials" / "XJTU.png"


col1, col2, col3 = st.columns([1.4,2,2])
with col1:
    st.image(LOGO_xjtu)
with col3:
    st.image(LOGO_bigc)


#page definition
home = st.Page("pages/home.py", title="Home")
page1 = st.Page("pages/page1.py", title="Single Case Input")
page2 = st.Page("pages/page2.py", title="Batch Cases Input")
page3 = st.Page("pages/page3.py", title="Blood Indices - Cartilage Genes")
pg = st.navigation([home, page1, page2, page3 ],position="hidden")
pg.run()

with st.sidebar:
    st.image(LOGO_path)
    st.divider()
    st.page_link("pages/home.py", label="Home")
    st.page_link("pages/page1.py", label="Single Case Input")
    st.page_link("pages/page2.py", label="Batch Cases Input")
    st.page_link("pages/page3.py", label="Blood Indices - Cartilage Genes")


