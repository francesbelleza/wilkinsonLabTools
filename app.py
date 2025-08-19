import streamlit as st
from tools.missteps import missteps_scatter_tool
from tools.steps import steps_scatter_tool

def main():
    st.title("Lab Tools")

    # 1) bootstrap session_state
    if "tool" not in st.session_state:
        st.session_state.tool = None

    # 2) buttons
    if st.session_state.tool is None:
        if st.button("missteps scatterplots"):
            st.session_state.tool = "missteps"
        if st.button("steps scatterplots"):
            st.session_state.tool = "steps"
        ####add for future button

    # 3) dispatch
    if st.session_state.tool == "missteps":
        missteps_scatter_tool()
    elif st.session_state.tool == "steps":
        steps_scatter_tool()

if __name__ == "__main__":
    main()
