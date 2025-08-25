import streamlit as st
from tools.front_limbs_missteps import front_limbs_missteps_tool
from tools.back_limbs_missteps import back_limbs_missteps_tool
from tools.front_limbs_total_steps import front_limbs_total_steps_tool
from tools.back_limbs_total_steps import back_limbs_total_steps_tool
from tools.wire_and_inversion_tool import wire_and_inversion_tool


def main():
    st.title("Wilkinson Lab Tools")

    # 1) bootstrap session_state
    if "tool" not in st.session_state:
        st.session_state.tool = None

    # 2) buttons
    if st.session_state.tool is None:
        st.subheader("Missteps Analysis")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Front Limbs Missteps"):
                st.session_state.tool = "front_missteps"
        with col2:
            if st.button("Back Limbs Missteps"):
                st.session_state.tool = "back_missteps"

        st.subheader("Total Steps Analysis")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Front Limbs Steps"):
                st.session_state.tool = "front_steps"
        with col4:
            if st.button("Back Limbs Steps"):
                st.session_state.tool = "back_steps"

        st.subheader("Wire and Inversion")
        if st.button("Wire + Inversion"):
            st.session_state.tool = "wire_and_inversion"

    # 3) dispatch
    if st.session_state.tool == "front_missteps":
        front_limbs_missteps_tool()
    elif st.session_state.tool == "back_missteps":
        back_limbs_missteps_tool()
    elif st.session_state.tool == "front_steps":
        front_limbs_total_steps_tool()
    elif st.session_state.tool == "back_steps":
        back_limbs_total_steps_tool()
    elif st.session_state.tool == "wire_and_inversion_tool":
        wire_and_inversion_tool()

if __name__ == "__main__":
    main()