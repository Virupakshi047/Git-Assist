import streamlit as st
import requests
import json

st.set_page_config(page_title="GitHub Issue Assistant")

col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("assets/github-copilot-logo.png", width=80)
with col2:
    st.title("GitHub Issue Assistant")
st.markdown("Analyze and summarize any public GitHub issue using AI.")

# -- Input fields --
repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/owner/repo")
issue_number = st.number_input("Issue Number", min_value=1, step=1)

# -- Session state to preserve output --
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# -- Button --
if st.button("🔍 Analyze Issue"):
    if repo_url and issue_number:
        with st.spinner("Analyzing issue with LLM..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze-issue",
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

    st.markdown(f"**🔥 Priority Score**: {result.get('priority_score', '-')}/5")

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

def fetch_and_update_history():
    """Fetches analysis history from the backend and updates session state."""
    try:
        history_response = requests.get("http://127.0.0.1:8000/history")
        if history_response.status_code == 200:
            st.session_state.history = history_response.json()
        else:
            st.toast(f"Failed to fetch history: {history_response.status_code}", icon="🚨")
            st.session_state.history = []  # Avoid crashing if fetch fails
    except Exception as e:
        st.toast(f"Could not connect to backend: {str(e)}", icon="❌")
        st.session_state.history = []  # Avoid crashing if fetch fails

# Layout for the refresh button
col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("🔁 Refresh"):
        fetch_and_update_history()

# Initialize and fetch history on first load
if "history" not in st.session_state:
    fetch_and_update_history()

# Show table
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
