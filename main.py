import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

def main():
    st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")

    # Stylish Title
    st.markdown("<h1 style='text-align: center; color: #0a66c2;'>💡 LinkedIn Post Generator</h1>", unsafe_allow_html=True)

    fs = FewShotPosts()

    # Expander for selection options
    with st.expander("⚙️ Customize Your Post"):
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_tag = st.selectbox("📌 Title", options=fs.get_tags())

        with col2:
            selected_length = st.selectbox("📏 Length", options=length_options)

        with col3:
            selected_language = st.selectbox("🗣️ Language", options=language_options)

    # Generate Button
    if st.button("✨ Generate Post", use_container_width=True):
        with st.spinner("Generating... ⏳"):
            post = generate_post(selected_length, selected_language, selected_tag)

        # Display the generated post
        st.markdown("### ✨ Your LinkedIn Post:")
        st.success(post)

if __name__ == "__main__":
    main()
