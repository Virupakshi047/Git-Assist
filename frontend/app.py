import streamlit as st
import requests
import json
import os


BACKEND_URL = st.secrets["backend_url"]

st.set_page_config(page_title="GitHub Issue Assistant")

def get_severity_label(score: int) -> str:
    labels = {
        1: "Trivial",
        2: "Low",
        3: "Medium",
        4: "High",
        5: "Critical"
    }
    return labels.get(score, "Unknown")

severity_colors = {
    "Trivial": "gray",
    "Low": "green",
    "Medium": "blue",
    "High": "orange",
    "Critical": "red"
}

col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("assets/github-copilot-logo.png", width=80)
with col2:
    st.title("GitHub Issue Assistant")
st.markdown("Analyze and summarize any public GitHub issue using AI.")


repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/owner/repo")
issue_number = st.number_input("Issue Number", min_value=1, step=1)

# -- Session state to preserve output --
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

def fetch_and_update_history():
    """Fetches analysis history from the backend and updates session state. load the history"""
    try:
        history_response = requests.get(BACKEND_URL + "/history")
        if history_response.status_code == 200:
            st.session_state.history = history_response.json()
        else:
            st.toast(f"Failed to fetch history: {history_response.status_code}", icon="🚨")
            st.session_state.history = []  
    except Exception as e:
        st.toast(f"Could not connect to backend: {str(e)}", icon="❌")
        st.session_state.history = []  

# -- Button --
if st.button("🔍 Analyze Issue"):
    if repo_url and issue_number:
        with st.spinner("Analyzing issue with LLM..."):
            try:
                response = requests.post(
                    BACKEND_URL + "/analyze-issue",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({
                        "repo_url": repo_url,
                        "issue_number": int(issue_number)
                    })
                )
                if response.status_code == 200:
                    st.session_state.analysis_result = response.json()
                    st.success("✅ Analysis Complete")
                    fetch_and_update_history()
                else:
                    st.error(f"❌ {response.text}")
            except Exception as e:
                st.error(f"🚨 Exception: {str(e)}")
    else:
        st.warning("Please enter both repo URL and issue number.")

# -- Result Output --
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    st.markdown("### 🧾 Analysis Summary")

    st.markdown(f"**📝 Summary**: {result.get('summary', '-')}")
    st.markdown(f"**📌 Type**: `{result.get('type', '-')}`")

    severity_label = get_severity_label(result["priority_score"])
    color = severity_colors[severity_label]
    st.markdown(f"**🔥 Priority**: <span style='color:{color};'>{severity_label}</span>", unsafe_allow_html=True)

    st.markdown("**🏷️ Suggested Labels**:")
    for label in result.get("suggested_labels", []):
        st.markdown(f"- `{label}`")

    st.markdown("**⚠️ Potential Impact**:")
    st.info(result.get("potential_impact", "-"))

    # Copyable JSON
    st.markdown("---")
    st.markdown("#### 📋 Full JSON Output")
    pretty_json = json.dumps(result, indent=2)
    st.code(pretty_json, language="json")
    st.caption("👉 Select and copy the JSON above manually.")

st.markdown("---")
st.markdown("## 🧾 Analysis History")

col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("🔁 Refresh"):
        fetch_and_update_history()

# Initialize and fetch history on first load
if "history" not in st.session_state:
    fetch_and_update_history()

if st.session_state.history:
    st.subheader("Analysis History")
    for item in st.session_state.history:
        repo_name = '/'.join(item['repo_url'].split('/')[-2:])
        url = f"{item['repo_url']}/issues/{item['issue_number']}"
        with st.expander(f"📌 {repo_name} #{item['issue_number']} ({item['type']}, Priority {item['priority_score']})"):
            st.markdown(f"**View on GitHub:** [{url}]({url})")
            st.markdown("---")
            st.markdown(f"**📝 Summary**: {item['summary']}")
            st.markdown(f"**🏷️ Labels**: `{item['suggested_labels']}`")
            st.markdown(f"**⚠️ Impact**: {item['potential_impact']}")
            st.markdown("**📋 Full JSON Output:**")
            st.code(item["full_json"], language="json")
