import streamlit as st
from few_shot import fewShotPosts
from post_generator import generate_post

LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Urdu"]


def main():
    st.set_page_config(page_title="LinkedIn Post Generator", page_icon="📝", layout="centered")
    st.title("📝 LinkedIn Post Generator")

    fs = fewShotPosts()
    tags = fs.get_tags()

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("Tag", options=tags)
    with col2:
        selected_length = st.selectbox("Length", options=LENGTH_OPTIONS)
    with col3:
        selected_language = st.selectbox("Language", options=LANGUAGE_OPTIONS)

    if st.button("Generate", type="primary", use_container_width=True):
        with st.spinner("Generating your LinkedIn post..."):
            post = generate_post(selected_tag, selected_length, selected_language)
        st.subheader("Generated Post")
        st.write(post)


if __name__ == "__main__":
    main()
