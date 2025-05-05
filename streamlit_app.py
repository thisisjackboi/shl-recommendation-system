
import streamlit as st
from urllib.parse import urlparse
import re
from recommender import get_top_assessments

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

# Custom CSS styling (simplified from original static/style.css)
custom_css = """
<style>
body {
    font-family: 'Inter', sans-serif;
    background-color: #edf1eb;
}
h1 {
    font-weight: 700;
    font-family: 'Poppins', sans-serif;
}
.glass-box {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
}
button {
    font-family: 'Inter', sans-serif;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Header
st.markdown("<div class='glass-box'><h1>🔍 SHL Assessment Recommender</h1></div>", unsafe_allow_html=True)

# Input Mode
mode = st.radio("Select Input Mode", ["URL", "Query"], horizontal=True)

# URL Input (if applicable)
if mode == "URL":
    job_url = st.text_input("Paste Job URL Here")
    if st.button("Extract Keywords"):
        try:
            path = urlparse(job_url).path
            match = re.search(r"/(?:jobs/view|jobs|job)/([^/?]+)", path, re.IGNORECASE)
            if match:
                raw_keywords = match.group(1)
                keywords = " ".join(raw_keywords.lower().split("-")[:5])
                st.success(f"Extracted keywords: {keywords}")
                query = keywords  # auto-fill into the text area
            else:
                st.error("Could not extract keywords from that URL.")
        except:
            st.error("Invalid URL.")


# Query Input
query = st.text_area("Enter job description or keywords")

# Number of Results
num_results = st.slider("Number of Recommendations", 1, 20, 5)

# Recommend Button
if st.button("Recommend"):
    if query.strip() == "":
        st.error("Please enter a valid query.")
    else:
        results = get_top_assessments(query, K=20, N=num_results)
        if results:
            st.success(f"Top {len(results)} recommendations:")
            for i, item in enumerate(results, 1):
                with st.container():
                    st.markdown(f"**{i}. [{item['name']}]({item['url']})**")
                    st.markdown(f"- **Duration:** {item.get('duration', 'N/A')} min")
                    st.markdown(f"- **Adaptive:** {item.get('adaptive', False)}")
                    st.markdown(f"- **Remote:** {item.get('remote', False)}")
                    st.markdown(f"- **Test Type:** {', '.join(item.get('test_type', []))}")
                    st.markdown("---")
        else:
            st.warning("No recommendations found.")
