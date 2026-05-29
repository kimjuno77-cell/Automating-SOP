import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* Custom CSS for Sticky Right Column */
    [data-testid="stHorizontalBlock"] {
        align-items: start !important;
    }
    div[data-testid="column"]:has(#right-col-marker) {
        position: sticky !important;
        top: 4rem;
        height: calc(100vh - 5rem);
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

left, right = st.columns([3, 1])

with left:
    for i in range(50):
        st.write(f"Left {i}")
        c1, c2 = st.columns(2)
        c1.write("c1")
        c2.write("c2")

with right:
    st.markdown('<div id="right-col-marker"></div>', unsafe_allow_html=True)
    st.write("Right Column (Should be sticky)")
    for i in range(10):
        st.write(f"Right item {i}")
