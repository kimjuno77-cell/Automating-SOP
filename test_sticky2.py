import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* Sticky Column Content */
    div[data-testid="column"]:has(#right-col-marker) > div {
        position: sticky !important;
        top: 4rem;
        max-height: calc(100vh - 5rem);
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

left, right = st.columns([3, 1])

with left:
    for i in range(50):
        st.write(f"Left {i}")

with right:
    st.markdown('<div id="right-col-marker"></div>', unsafe_allow_html=True)
    st.write("Right Column (Should be sticky)")
    for i in range(10):
        st.write(f"Right item {i}")
