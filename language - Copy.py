import streamlit as st
from jamaibase import JamAI, protocol as p

# Initialize JamAI
jamai = JamAI(api_key="jamai_pat_73eea57ed1907ae41abb4968ed9ad64e0be2f675fa3650a8", project_id="proj_65f97c5c9e50da15d6c8faff")

# Configuration constants
API_CONFIG = {
    "PAT": "jamai_pat_73eea57ed1907ae41abb4968ed9ad64e0be2f675fa3650a8",
    "PROJ_ID": "proj_65f97c5c9e50da15d6c8faff",
    "TABLE_ID": "language_assistant",
    "BASE_URL": "https://api.jamaibase.com/v1"  
}

#Streamlit 
st.set_page_config(page_title="Cultural Language Assistant", page_icon="🌎")
st.title("🌎 Cultural Language Assistant")


st.markdown("""
    <style>
    h1 {
        color: #9932CC; 
    }
    .response-box {
        background-color: #444;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
    }
    .stButton > button {
        background-color: #4B0082;
        color: white;
        width: 100%;
    }
    .title {
        color: #9932CC;
        text-align: center;
        font-size: 40px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)



# Input containers

input_text = st.text_area("Enter your text", placeholder="Example: Good morning, nice to meet you", height=100)
target_language = st.selectbox(
    "Select target language",
    ["Arabic", "Chinese", "Japanese", "Korean", "Persian", "Spanish"]
)
context = st.selectbox(
    "Select context",
    ["Business meeting", "Casual conversation", "Restaurant", 
     "Family gathering", "Academic setting", "First meeting"]
)

# Process button
if st.button("Translate&nbsp;&nbsp;&nbsp;&&nbsp;&nbsp;&nbsp;Get&nbsp;Cultural&nbsp;Tips", use_container_width=True):
    if input_text and target_language and context:
        try:
            # Call JamAI action table
            completion = jamai.add_table_rows(
                "action",
                p.RowAddRequest(
                    table_id="language_assistant",
                    data=[{
                        "input_text": input_text,
                        "target_language": target_language,
                        "context": context
                    }],
                    stream=False
                )
            )

            if completion.rows:
                output_row = completion.rows[0].columns
                translation = output_row.get("translation")
                cultural_tips = output_row.get("cultural_tips")
                response_suggestions = output_row.get("response_suggestions")

                # Display results in organized sections
                st.subheader("📝 Translation & Pronunciation")
                st.markdown(f'<div class="response-box">{translation.text if translation else "N/A"}</div>', 
                          unsafe_allow_html=True)

                st.subheader("🎯 Cultural Tips")
                st.markdown(f'<div class="response-box">{cultural_tips.text if cultural_tips else "N/A"}</div>', 
                          unsafe_allow_html=True)

                st.subheader("💬 Common Responses")
                st.markdown(f'<div class="response-box">{response_suggestions.text if response_suggestions else "N/A"}</div>', 
                          unsafe_allow_html=True)

                # Add copy buttons for each section
                col1, col2, col3 = st.columns(3)
                with col1:
                    if translation:
                        st.button("📋 Copy Translation", key="copy_trans")
                with col2:
                    if cultural_tips:
                        st.button("📋 Copy Tips", key="copy_tips")
                with col3:
                    if response_suggestions:
                        st.button("📋 Copy Responses", key="copy_resp")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please fill in all fields.")

# Add helpful examples at the bottom
with st.expander("See examples"):
    st.markdown("""
    Try these common phrases:
    - "Good morning, nice to meet you"
    - "Thank you very much"
    - "Could you help me, please?"
    - "I apologize for being late"
    """)
