# frontend/app.py

import streamlit as st
import requests
import time

API_URL = "https://reeana.onrender.com/analyze"
HEALTH_URL = "https://reeana.onrender.com/health"

# ── Page config ──
st.set_page_config(
    page_title="Reeana - Resume Analyzer",
    layout="centered"
)

# ── Server Wake-Up Check ──
def wake_up_backend():
    """Check if backend is awake. If not, show friendly message and wait."""

    if st.session_state.get("backend_ready"):
        return

    # Quick check — is it already awake?
    try:
        r = requests.get(HEALTH_URL, timeout=5)
        if r.status_code == 200:
            st.session_state.backend_ready = True
            return
    except requests.exceptions.RequestException:
        pass  # Server is sleeping, fall through to wake-up UI

    # Show wake-up UI
    st.warning("**Hang tight! Our server is waking up from sleep mode.**")
    st.info(
        "Reeana uses a free hosting plan, so the server dozes off after inactivity. "
        "**The first startup usually takes 20–30 seconds.** "
        "No need to refresh this page will automatically continue once it's ready!"
    )

    progress_bar = st.progress(0, text="Waking up server...")
    status_text = st.empty()

    max_wait_seconds = 90
    interval = 3
    steps = max_wait_seconds // interval

    for i in range(steps):
        time.sleep(interval)
        elapsed = (i + 1) * interval
        progress = min(int((i + 1) / steps * 95), 95)
        progress_bar.progress(progress, text=f"Still warming up... ({elapsed}s elapsed)")
        status_text.caption(f"Attempt {i + 1} of {steps} — checking if server is ready...")

        try:
            r = requests.get(HEALTH_URL, timeout=5)
            if r.status_code == 200:
                progress_bar.progress(100, text="Server is ready!")
                status_text.empty()
                st.success("Server is awake! Loading Reeana now...")
                time.sleep(1.5)
                st.session_state.backend_ready = True
                st.rerun()
                return
        except requests.exceptions.RequestException:
            continue

    # Timed out after 90 seconds
    st.error(
        "The server took too long to respond. "
        "Please **refresh the page** and try again. If the issue persists, check back in a few minutes."
    )
    st.stop()

# ── Run wake-up check before anything else ──
wake_up_backend()

st.title("Reeana")
st.write("Upload your resume and specify your target job role to get AI-powered feedback.")

# ── Main form ──
with st.form("resume_form"):
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, and TXT (Max 5MB)",
    )

    job_role = st.text_input(
        "Target job role",
        placeholder="e.g., Data Scientist, Software Engineer, Chef",
    )

    submitted = st.form_submit_button("Analyze Resume")

# ── Handle submission ──
if submitted:
    # Validate inputs
    if uploaded_file is None:
        st.warning("Please upload a resume file before submitting.")
    elif not job_role.strip():
        st.warning("Please enter a target job role.")
    else:
        # Show loading spinner
        with st.spinner("Analyzing your resume... This may take a few seconds."):
            try:
                # Prepare the files and data to send
                files = {
                    "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                data = {
                    "job_role": job_role.strip()
                }

                # Make the API request
                response = requests.post(
                    API_URL,
                    files=files,
                    data=data,
                    timeout=30  # 30 second timeout
                )

                # Check if request was successful
                response.raise_for_status()

                # Parse the JSON response
                feedback = response.json()

                # ── Display Results ──
                st.success("✅ Analysis complete!")

                # Overall score
                overall_score = feedback.get("overall_score")
                if overall_score is not None:
                    st.metric(
                        label="Overall Resume Score",
                        value=f"{overall_score}/10",
                        delta=f"{overall_score - 5} from average" if overall_score >= 5 else None
                    )

                # Create two columns for better layout
                col1, col2 = st.columns(2)

                # ── Strengths ──
                with col1:
                    st.subheader("Strengths")
                    strengths = feedback.get("strengths", [])
                    if strengths:
                        for strength in strengths:
                            st.success(f"✓ {strength}")
                    else:
                        st.info("No strengths identified.")

                # ── Keyword Gaps ──
                with col2:
                    st.subheader("Missing Keywords")
                    keyword_gaps = feedback.get("keyword_gaps", [])
                    if keyword_gaps:
                        for gap in keyword_gaps:
                            st.warning(f"⚠ {gap}")
                    else:
                        st.info("No keyword gaps found.")

                # ── Weaknesses ──
                st.subheader("Areas to Improve")
                weaknesses = feedback.get("weaknesses", [])
                if weaknesses:
                    for i, weakness in enumerate(weaknesses, 1):
                        with st.expander(f"Issue {i}: {weakness.get('issue', 'N/A')[:60]}..."):
                            st.write(f"**Problem:** {weakness.get('issue', 'N/A')}")
                            st.write(f"**Solution:** {weakness.get('fix', 'N/A')}")
                else:
                    st.info("No major weaknesses identified.")

                # ── Top Priority ──
                st.subheader("Top Priority")
                top_priority = feedback.get("top_priority")
                if top_priority:
                    st.info(f"**Most impactful change:** {top_priority}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. The API might be slow or down. Please try again.")

            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to the API at {API_URL}. Make sure the backend is running.")

            except requests.exceptions.HTTPError as e:
                # API returned an error (4xx or 5xx)
                try:
                    error_detail = response.json().get("detail", str(e))
                except:
                    error_detail = str(e)
                st.error(f"API Error: {error_detail}")

            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

# ── Footer ──
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Developed by Namshima Iordye</div>",
    unsafe_allow_html=True
)
