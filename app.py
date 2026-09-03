
# import os
# import io
# import streamlit as st
# import pandas as pd

# # Define local master file path
# HARDCODED_MASTER_PATH = "master_data.xlsx"

# # -------------------------------------------------------------
# # Custom Override Rules Configuration
# # -------------------------------------------------------------
# # Direct Technical Notes (Ignores Object Name & Type)
# DIRECT_TECHNICAL_NOTES = {
#     "2199837", "2215424", "2228241", "2348023", "2438006",
#     "2438110", "2438131", "2610650", "2628699", "2628704",
#     "2628706", "3320010", "2228242", "2669781", "2669857",
#     "2670006"
# }

# # DB operations list to match against CHECK MESSAGE
# DB_OPERATIONS = ["DELETE", "MODIFY", "UPDATE", "SELECT UPDATE", "WRITE"]

# # Notes triggered when CHECK MESSAGE contains any DB operation
# DB_OPERATION_NOTES = {
#     "2768887": "Technical",
#     "2431747": "Functional",
#     "2389136": "Functional",
#     "2265093": "Functional",
#     "1976487": "Functional",
#     "2354768": "Functional",
#     "2378796": "Technical",
#     "2270387": "Functional",
#     "2337368": "Functional",
#     "2226048": "Functional",
#     "2226072": "Functional",
#     "2220005": "Technical",
#     "2332591": "Functional",
#     "2206980": "Functional",
#     "2270388": "Technical",
#     "2870766": "Functional",
# }

# # -------------------------------------------------------------
# # Streamlit Page Config & Styling
# # -------------------------------------------------------------
# st.set_page_config(
#     page_title="SAP Track Segregator",
#     page_icon="✨",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: #FFFFFF !important;
#         font-family: 'Google Sans', 'Inter', -apple-system, sans-serif;
#     }
#     .block-container {
#         padding-top: 4rem !important;
#         padding-bottom: 4rem !important;
#         max-width: 950px;
#     }
#     .ai-greeting {
#         background: linear-gradient(135deg, #4285F4 0%, #9B51E0 50%, #E9446A 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         font-size: 3.2rem !important;
#         font-weight: 700 !important;
#         letter-spacing: -0.03em;
#         margin-bottom: 5px !important;
#     }
#     .ai-subtitle {
#         color: #C4C7C5 !important;
#         font-size: 3.2rem !important;
#         font-weight: 600 !important;
#         letter-spacing: -0.03em;
#         margin-bottom: 40px !important;
#         line-height: 1.1;
#     }
#     .card-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#         gap: 16px;
#         margin-bottom: 40px;
#     }
#     .feature-card {
#         background-color: #F0F4F9;
#         border-radius: 16px;
#         padding: 20px;
#         min-height: 120px;
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#     }
#     .card-title {
#         color: #1E1E1E;
#         font-size: 0.95rem;
#         font-weight: 500;
#         line-height: 1.4;
#     }
#     .card-icon {
#         align-self: flex-end;
#         background-color: #FFFFFF;
#         border-radius: 50%;
#         width: 30px;
#         height: 30px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         color: #4285F4;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#     }
#     .stFileUploader {
#         border: 1px solid #C4C7C5 !important;
#         background-color: #FFFFFF !important;
#         border-radius: 24px !important;
#         padding: 10px 20px !important;
#         box-shadow: 0 1px 3px rgba(0,0,0,0.05);
#     }
#     div.stButton > button:first-child {
#         background: #1A73E8 !important;
#         color: #FFFFFF !important;
#         border-radius: 24px !important;
#         padding: 12px 35px !important;
#         font-weight: 500 !important;
#         font-size: 0.95rem !important;
#         border: none !important;
#     }
#     </style>
# """,
#     unsafe_allow_html=True,
# )

# # Header UI
# st.markdown('<h1 class="ai-greeting">Hello, User</h1>', unsafe_allow_html=True)
# st.markdown('<h1 class="ai-subtitle">How can I help you today?</h1>', unsafe_allow_html=True)

# # Helper functions
# def clean_val(val):
#     if pd.isna(val):
#         return ""
#     if isinstance(val, (int, float)):
#         return str(int(val))
#     return str(val).strip().upper()

# def find_column(columns, keywords_priority):
#     clean_cols = [str(c).strip().lower() for c in columns]
#     for kw in keywords_priority:
#         for idx, c in enumerate(clean_cols):
#             if kw in c:
#                 return columns[idx]
#     return None

# # -------------------------------------------------------------
# # Cached Master File Lookup
# # -------------------------------------------------------------
# @st.cache_data(show_spinner="Loading Master Database...")
# def load_master_lookup(file_path):
#     lookup = {}
#     if os.path.exists(file_path):
#         try:
#             master_df = pd.read_excel(file_path)
#             m_cols = list(master_df.columns)

#             col_m_note = find_column(m_cols, ["ossnotenumber", "ossnote", "notenumber", "note num", "note"])
#             col_m_type = find_column(m_cols, ["sapobjecttype", "object type", "reference object type", "refernce object type", "obj type", "type"])
#             col_m_name = find_column(m_cols, ["sapobjectname", "reference object name", "referenced object", "reference object", "obj name", "object name", "name"])
#             col_m_scope = find_column(m_cols, ["scope", "cat", "track"])

#             if col_m_note and col_m_name and col_m_type and col_m_scope:
#                 for _, row in master_df.dropna(subset=[col_m_note]).iterrows():
#                     key = (
#                         clean_val(row[col_m_note]),
#                         clean_val(row[col_m_name]),
#                         clean_val(row[col_m_type]),
#                     )
#                     lookup[key] = str(row[col_m_scope]).strip()
#         except Exception as e:
#             st.error(f"Error reading master dataset: {e}")
#     return lookup

# master_lookup = load_master_lookup(HARDCODED_MASTER_PATH)

# if not master_lookup:
#     st.error(f"⚠️ Could not load master lookup. Make sure '{HARDCODED_MASTER_PATH}' exists in your folder.")

# # Cards Layout
# st.markdown(
#     """
#     <div class="card-grid">
#         <div class="feature-card">
#             <div class="card-title">Dynamic 3-Way Match & Custom Rule Override Logic.</div>
#             <div class="card-icon">🎯</div>
#         </div>
#         <div class="feature-card">
#             <div class="card-title">Segregate matched objects into Functional, Technical, or HCC/HPO.</div>
#             <div class="card-icon">⚡</div>
#         </div>
#         <div class="feature-card">
#             <div class="card-title">Retain original extracted details with Match_Status tracking.</div>
#             <div class="card-icon">🔍</div>
#         </div>
#     </div>
# """,
#     unsafe_allow_html=True,
# )

# # -------------------------------------------------------------
# # File Upload & Processing Workspace
# # -------------------------------------------------------------
# st.write("##### Upload your freshly extracted SAP sheet:")
# user_file = st.file_uploader("", type=["csv", "xlsx"], key="triplet_uploader")

# # Reset state on file change
# if "current_file_name" in st.session_state and (user_file is None or user_file.name != st.session_state["current_file_name"]):
#     if "processed_df" in st.session_state:
#         del st.session_state["processed_df"]
#     if "export_data" in st.session_state:
#         del st.session_state["export_data"]

# if user_file is not None:
#     st.session_state["current_file_name"] = user_file.name

#     try:
#         if user_file.name.endswith(".csv"):
#             fresh_df = pd.read_csv(user_file)
#         else:
#             fresh_df = pd.read_excel(user_file)

#         fresh_cols = list(fresh_df.columns)

#         col_f_note = find_column(fresh_cols, ["ossnotenumber", "ossnote", "notenumber", "note num", "note"])
#         col_f_type = find_column(fresh_cols, ["reference object type", "refernce object type", "sapobjecttype", "object type", "obj type", "type"])
#         col_f_name = find_column(fresh_cols, ["reference object name", "referenced object", "refernce object", "reference object", "sapobjectname", "obj name", "object name", "name"])
#         col_f_msg = find_column(fresh_cols, ["check message", "check_message", "message", "msg"])

#         if None in (col_f_note, col_f_name, col_f_type):
#             st.error("❌ Column Layout Error: Could not locate columns for Note Number, Reference Object Name, and Reference Object Type.")
#         else:
#             st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
            
#             if st.button("Generate Clean Segregation Layout"):
#                 with st.spinner("Processing records... Please wait."):
#                     scopes_list = []
#                     match_status_list = []

#                     for idx, row in fresh_df.iterrows():
#                         note_val = clean_val(row[col_f_note])
#                         name_val = clean_val(row[col_f_name])
#                         type_val = clean_val(row[col_f_type])
#                         msg_val = clean_val(row[col_f_msg]) if col_f_msg else ""

#                         # Check if message contains ANY DB operation
#                         has_db_op = any(op in msg_val for op in DB_OPERATIONS)

#                         # -------------------------------------------------------------
#                         # RULE 1: Hard Override for Note 1912445
#                         # -------------------------------------------------------------
#                         if note_val == "1912445":
#                             assigned_scope = "HCC/HPO"
#                             status = "Matched"

#                         # -------------------------------------------------------------
#                         # RULE 2: Direct Technical Notes Override List (Ignores Object Name/Type)
#                         # -------------------------------------------------------------
#                         elif note_val in DIRECT_TECHNICAL_NOTES:
#                             assigned_scope = "Technical"
#                             status = "Matched"

#                         # -------------------------------------------------------------
#                         # RULE 3: Special Note 2198647 Object Name Checking
#                         # -------------------------------------------------------------
#                         elif note_val == "2198647" and has_db_op:
#                             if "VBFA" in name_val:
#                                 assigned_scope = "Technical"
#                                 status = "Matched"
#                             elif any(obj in name_val for obj in ["VBUP", "VBUK"]):
#                                 assigned_scope = "Functional"
#                                 status = "Matched"
#                             else:
#                                 fresh_key = (note_val, name_val, type_val)
#                                 if fresh_key in master_lookup:
#                                     assigned_scope = master_lookup[fresh_key]
#                                     status = "Matched"
#                                 else:
#                                     assigned_scope = "New / Unmapped Note"
#                                     status = "Not Found"

#                         # -------------------------------------------------------------
#                         # RULE 4: Specific DB-Operation Notes Override List
#                         # -------------------------------------------------------------
#                         elif note_val in DB_OPERATION_NOTES and has_db_op:
#                             assigned_scope = DB_OPERATION_NOTES[note_val]
#                             status = "Matched"

#                         # -------------------------------------------------------------
#                         # DEFAULT: Master Database 3-Way Composite Lookup
#                         # -------------------------------------------------------------
#                         else:
#                             fresh_key = (note_val, name_val, type_val)
#                             if fresh_key in master_lookup:
#                                 assigned_scope = master_lookup[fresh_key]
#                                 status = "Matched"
#                             else:
#                                 assigned_scope = "New / Unmapped Note"
#                                 status = "Not Found"

#                         scopes_list.append(assigned_scope)
#                         match_status_list.append(status)

#                     output_df = fresh_df.copy()
#                     output_df["Scope"] = scopes_list
#                     output_df["Match_Status"] = match_status_list

#                     # Persist state
#                     st.session_state["processed_df"] = output_df
#                     st.session_state["match_status_list"] = match_status_list

#                     if user_file.name.endswith(".csv"):
#                         st.session_state["export_data"] = output_df.to_csv(index=False).encode("utf-8")
#                         st.session_state["mime_type"] = "text/csv"
#                         st.session_state["export_name"] = f"processed_{user_file.name}"
#                     else:
#                         towrite = io.BytesIO()
#                         with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
#                             output_df.to_excel(writer, index=False)
#                         st.session_state["export_data"] = towrite.getvalue()
#                         st.session_state["mime_type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                         st.session_state["export_name"] = f"processed_{user_file.name}"

#             # Persistent Results View & Download Button
#             if "processed_df" in st.session_state:
#                 output_df = st.session_state["processed_df"]
#                 match_status_list = st.session_state["match_status_list"]

#                 st.markdown('<div style="margin-top: 35px;"></div>', unsafe_allow_html=True)
#                 st.write("### ✨ Matching Results")

#                 tab_preview, tab_metrics = st.tabs(["📄 Appended Sheet Preview", "📊 Metrics Summary"])

#                 with tab_preview:
#                     st.dataframe(output_df, use_container_width=True)

#                 with tab_metrics:
#                     col1, col2, col3 = st.columns(3)
#                     col1.metric("Total Submitted", len(output_df))
#                     col2.metric("Matched", match_status_list.count("Matched"))
#                     col3.metric("Unmapped / New", match_status_list.count("Not Found"))

#                 st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
#                 st.download_button(
#                     label="📥 Download Processed File",
#                     data=st.session_state["export_data"],
#                     file_name=st.session_state["export_name"],
#                     mime=st.session_state["mime_type"],
#                     key="persistent_download_btn"
#                 )

#     except Exception as e:
#         st.error(f"Processing Error: {e}")


#  --------------------------------------- NEW UI ____________________________

# import os
# import io
# import time
# import streamlit as st
# import pandas as pd

# # Define local master file path
# HARDCODED_MASTER_PATH = "master_data.xlsx"

# # -------------------------------------------------------------
# # Custom Override Rules Configuration
# # -------------------------------------------------------------
# DIRECT_TECHNICAL_NOTES = {
#     "2199837", "2215424", "2228241", "2348023", "2438006",
#     "2438110", "2438131", "2610650", "2628699", "2628704",
#     "2628706", "3320010", "2228242", "2669781", "2669857",
#     "2670006"
# }

# DB_OPERATIONS = ["DELETE", "MODIFY", "UPDATE", "SELECT UPDATE", "WRITE"]

# DB_OPERATION_NOTES = {
#     "2768887": "Technical",
#     "2431747": "Functional",
#     "2389136": "Functional",
#     "2265093": "Functional",
#     "1976487": "Functional",
#     "2354768": "Functional",
#     "2378796": "Technical",
#     "2270387": "Functional",
#     "2337368": "Functional",
#     "2226048": "Functional",
#     "2226072": "Functional",
#     "2220005": "Technical",
#     "2332591": "Functional",
#     "2206980": "Functional",
#     "2270388": "Technical",
#     "2870766": "Functional",
# }

# # -------------------------------------------------------------
# # Streamlit Page Config & Custom Design System
# # -------------------------------------------------------------
# st.set_page_config(
#     page_title="OSS Note Scope Segregator",
#     page_icon="🧩",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# st.markdown(
#     """
#     <style>
#     /* Dark Theme Base */
#     .stApp {
#         background-color: #1a1a1a !important;
#         color: #f0f0f0 !important;
#         font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
#     }
#     .block-container {
#         padding-top: 0rem !important;
#         padding-bottom: 3rem !important;
#         max-width: 1200px !important;
#     }
    
#     /* Top Header Bar */
#     .top-header {
#         background-color: #111111;
#         padding: 12px 24px;
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         border-bottom: 1px solid #2a2a2a;
#         margin-bottom: 30px;
#     }
#     .brand-title {
#         color: #ffffff;
#         font-weight: 700;
#         font-size: 1.1rem;
#         display: flex;
#         align-items: center;
#         gap: 10px;
#     }
#     .brand-subtitle {
#         color: #888888;
#         font-size: 0.75rem;
#         text-transform: uppercase;
#         letter-spacing: 0.05em;
#     }
#     .version-badge {
#         background-color: #24282e;
#         color: #9bb0a5;
#         border: 1px solid #343a40;
#         padding: 4px 12px;
#         border-radius: 20px;
#         font-size: 0.8rem;
#         font-family: monospace;
#     }

#     /* Button Styling */
#     div.stButton > button,
#     div.stDownloadButton > button,
#     div[data-testid="stDownloadButton"] > button {
#         background-color: #26292f !important;
#         border: 1px solid #4a4e58 !important;
#         border-radius: 8px !important;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.4) !important;
#         transition: all 0.2s ease-in-out !important;
#     }
    
#     div.stButton > button,
#     div.stButton > button *,
#     div.stButton > button p,
#     div.stButton > button span,
#     div.stDownloadButton > button,
#     div.stDownloadButton > button *,
#     div.stDownloadButton > button p,
#     div.stDownloadButton > button span,
#     div[data-testid="stDownloadButton"] > button,
#     div[data-testid="stDownloadButton"] > button * {
#         color: #ffffff !important;
#         font-weight: 700 !important;
#         font-size: 0.95rem !important;
#     }
    
#     div.stButton > button:hover,
#     div.stDownloadButton > button:hover,
#     div[data-testid="stDownloadButton"] > button:hover {
#         background-color: #32363e !important;
#         border-color: #616775 !important;
#     }

#     /* File Uploader Outer Box */
#     section[data-testid="stFileUploader"] {
#         background-color: #111111 !important;
#         border: 2px dashed #333333 !important;
#         border-radius: 12px !important;
#         padding: 20px !important;
#         margin-top: 10px !important;
#     }
#     section[data-testid="stFileUploader"] button {
#         background-color: #26292f !important;
#         border: 1px solid #4a4e58 !important;
#         border-radius: 6px !important;
#     }
#     section[data-testid="stFileUploader"] button,
#     section[data-testid="stFileUploader"] button * {
#         color: #ffffff !important;
#         font-weight: 700 !important;
#     }
#     section[data-testid="stFileUploader"] button:hover {
#         background-color: #32363e !important;
#     }

#     section[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p,
#     section[data-testid="stFileUploader"] span,
#     section[data-testid="stFileUploader"] small,
#     section[data-testid="stFileUploader"] div {
#         color: #cccccc !important;
#         font-weight: 600 !important;
#     }

#     /* User Guide Container (Placed BEFORE upload box) */
#     .user-guide-container {
#         background-color: #111111;
#         border: 1px solid #2d3748;
#         border-radius: 12px;
#         padding: 20px 24px;
#         margin-top: 15px;
#         margin-bottom: 25px;
#     }
#     .user-guide-header {
#         color: #ffffff;
#         font-weight: 700;
#         font-size: 1.05rem;
#         margin-bottom: 14px;
#         display: flex;
#         align-items: center;
#         gap: 8px;
#     }
#     .guide-step-row {
#         display: flex;
#         align-items: flex-start;
#         gap: 12px;
#         margin-bottom: 12px;
#         color: #d1d5db;
#         font-size: 0.92rem;
#         line-height: 1.5;
#     }
#     .guide-step-row:last-child {
#         margin-bottom: 0;
#     }
#     .guide-badge {
#         background-color: #26292f;
#         border: 1px solid #4a4e58;
#         color: #ffffff;
#         font-weight: 700;
#         border-radius: 50%;
#         min-width: 24px;
#         height: 24px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 0.8rem;
#     }

#     /* Page Headings */
#     .main-heading {
#         font-size: 2.2rem;
#         font-weight: 600;
#         color: #ffffff;
#         margin-bottom: 10px;
#     }
#     .sub-heading {
#         color: #cccccc;
#         font-size: 1rem;
#         margin-bottom: 20px;
#     }

#     /* Metric Cards Grid */
#     .metric-grid {
#         display: grid;
#         grid-template-columns: repeat(4, 1fr);
#         gap: 16px;
#         margin-top: 20px;
#         margin-bottom: 25px;
#     }
#     .metric-card {
#         background-color: #111111;
#         border-radius: 8px;
#         padding: 18px;
#         border-top: 3px solid #333;
#     }
#     .card-technical { border-top-color: #0d5c46; }
#     .card-functional { border-top-color: #2b6cb0; }
#     .card-hcc { border-top-color: #b7791f; }
#     .card-unmapped { border-top-color: #9b2c2c; }

#     .metric-label {
#         font-size: 0.75rem;
#         font-weight: 700;
#         text-transform: uppercase;
#         letter-spacing: 0.05em;
#         color: #a0aec0;
#     }
#     .metric-value {
#         font-size: 2rem;
#         font-weight: 700;
#         color: #ffffff;
#         margin: 5px 0;
#     }
#     .metric-subtext {
#         font-size: 0.8rem;
#         color: #718096;
#     }

#     /* Step Checklist Box */
#     .step-box {
#         background-color: #111111;
#         border-radius: 10px;
#         padding: 20px 30px;
#         border: 1px solid #2d3748;
#         margin-top: 20px;
#     }
#     .step-item {
#         display: flex;
#         justify-content: space-between;
#         padding: 12px 0;
#         border-bottom: 1px solid #1a202c;
#         font-size: 0.95rem;
#     }
#     .step-item:last-child { border-bottom: none; }
#     .step-icon { margin-right: 10px; }
#     .step-meta { color: #a0aec0; font-family: monospace; }

#     /* Please Wait Banner */
#     .wait-message {
#         background-color: #1c251e;
#         border: 1px solid #2d5a35;
#         color: #4ade80;
#         padding: 14px;
#         border-radius: 8px;
#         text-align: center;
#         font-weight: 600;
#         font-size: 1.05rem;
#         margin-top: 20px;
#     }

#     /* Radio Filter Labels */
#     div[data-testid="stRadio"] > label {
#         color: #ffffff !important;
#         font-weight: 700 !important;
#         font-size: 1rem !important;
#     }
#     div[data-testid="stRadio"] div[role="radiogroup"] label * {
#         color: #ffffff !important;
#         font-weight: 600 !important;
#         font-size: 0.95rem !important;
#     }

#     /* Export Card Styling */
#     .export-card {
#         background-color: #ffffff;
#         color: #1a202c !important;
#         border-radius: 12px;
#         padding: 30px;
#         max-width: 600px;
#         margin: 30px auto 10px auto;
#         box-shadow: 0 10px 25px rgba(0,0,0,0.5);
#     }
#     .export-card * { color: #1a202c !important; }
#     .export-badge {
#         background-color: #e6fffa;
#         color: #234e52 !important;
#         border-radius: 50%;
#         width: 36px;
#         height: 36px;
#         display: inline-flex;
#         align-items: center;
#         justify-content: center;
#         font-weight: bold;
#         margin-bottom: 15px;
#     }
#     .export-meta-box {
#         background-color: #f7fafc;
#         border-radius: 8px;
#         padding: 15px;
#         margin: 20px 0;
#         border: 1px solid #e2e8f0;
#     }

#     /* Hide standard Streamlit chrome */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     </style>
# """,
#     unsafe_allow_html=True,
# )

# # Helper functions
# def clean_val(val):
#     if pd.isna(val):
#         return ""
#     if isinstance(val, (int, float)):
#         return str(int(val))
#     return str(val).strip().upper()

# def find_column(columns, keywords_priority):
#     clean_cols = [str(c).strip().lower() for c in columns]
#     for kw in keywords_priority:
#         for idx, c in enumerate(clean_cols):
#             if kw in c:
#                 return columns[idx]
#     return None

# # -------------------------------------------------------------
# # Cached Master File Lookup
# # -------------------------------------------------------------
# @st.cache_data(show_spinner=False)
# def load_master_lookup(file_path):
#     lookup = {}
#     if os.path.exists(file_path):
#         try:
#             master_df = pd.read_excel(file_path)
#             m_cols = list(master_df.columns)

#             col_m_note = find_column(m_cols, ["ossnotenumber", "ossnote", "notenumber", "note num", "note"])
#             col_m_type = find_column(m_cols, ["sapobjecttype", "object type", "reference object type", "refernce object type", "obj type", "type"])
#             col_m_name = find_column(m_cols, ["sapobjectname", "reference object name", "referenced object", "reference object", "obj name", "object name", "name"])
#             col_m_scope = find_column(m_cols, ["scope", "cat", "track"])

#             if col_m_note and col_m_name and col_m_type and col_m_scope:
#                 for _, row in master_df.dropna(subset=[col_m_note]).iterrows():
#                     key = (
#                         clean_val(row[col_m_note]),
#                         clean_val(row[col_m_name]),
#                         clean_val(row[col_m_type]),
#                     )
#                     lookup[key] = str(row[col_m_scope]).strip()
#         except Exception as e:
#             st.error(f"Error reading master dataset: {e}")
#     return lookup

# master_lookup = load_master_lookup(HARDCODED_MASTER_PATH)

# # Top Header Bar
# header_col1, header_col2 = st.columns([4, 1])
# with header_col1:
#     st.markdown(
#         f"""
#         <div class="top-header">
#             <div class="brand-title">
#                 <span>🟩🟧<br>🟦🟥</span>
#                 <div>
#                     OSS Note Scope Segregator
#                     <div class="brand-subtitle">SMARTSHIFT PRE-SALES</div>
#                 </div>
#             </div>
#             <div class="version-badge">
#                 🟢 {HARDCODED_MASTER_PATH} · v14
#             </div>
#         </div>
#     """,
#         unsafe_allow_html=True,
#     )

# with header_col2:
#     if st.session_state.get("step") in ["dashboard", "export_modal"]:
#         if st.button("🔄 Upload New File", use_container_width=True):
#             st.session_state["step"] = "upload"
#             if "processed_df" in st.session_state:
#                 del st.session_state["processed_df"]
#             st.rerun()

# # -------------------------------------------------------------
# # Flow Management
# # -------------------------------------------------------------
# if "step" not in st.session_state:
#     st.session_state["step"] = "upload"

# # STEP 1: FILE UPLOAD SCREEN
# if st.session_state["step"] == "upload":
#     st.markdown('<div class="main-heading">Drop in your ATC extract — we\'ll scope every row.</div>', unsafe_allow_html=True)
#     st.markdown('<div class="sub-heading">No setup, no configuration. We match each finding against the master reference on Note Number + Reference Object, then hand back your file untouched with two new columns.</div>', unsafe_allow_html=True)

#     # USER GUIDE (Placed explicitly BEFORE the file uploader)
#     st.markdown(
#         """
#         <div class="user-guide-container">
#             <div class="user-guide-header">📖 User Guide</div>
#             <div class="guide-step-row">
#                 <span class="guide-badge">1</span>
#                 <div><b>Upload File:</b> Upload your extracted Excel/CSV sheet using the box below.</div>
#             </div>
#             <div class="guide-step-row">
#                 <span class="guide-badge">2</span>
#                 <div><b>Automated Matching:</b> This scope tool will match the uploaded file data with the master reference sheet.</div>
#             </div>
#             <div class="guide-step-row">
#                 <span class="guide-badge">3</span>
#                 <div><b>Scope Categorization:</b> It will give scope of objects as <b>Technical</b>, <b>Functional</b>, <b>HCC/HPO</b>, or <b>Unmapped</b> based on OSS Note Number, Reference Object Name, Object Type (and Check Message column for a few unique note numbers) with a separate count of each.</div>
#             </div>
#             <div class="guide-step-row">
#                 <span class="guide-badge">4</span>
#                 <div><b>Export Scoped Data:</b> You can download your extracted scoped file and use it for your project review.</div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # File Uploader
#     user_file = st.file_uploader("", type=["csv", "xlsx"], key="triplet_uploader")

#     if user_file is not None:
#         st.session_state["user_file"] = user_file
#         st.session_state["step"] = "processing"
#         st.rerun()

# # STEP 2: PROCESSING SIMULATION
# elif st.session_state["step"] == "processing":
#     user_file = st.session_state["user_file"]
    
#     st.markdown(f'<div class="sub-heading">{user_file.name}</div>', unsafe_allow_html=True)
#     st.markdown('<div class="main-heading">Normalising note numbers & object keys...</div>', unsafe_allow_html=True)
    
#     progress_bar = st.progress(0)
#     status_placeholder = st.empty()
#     wait_placeholder = st.empty()

#     def render_steps(step1="⚪", step2="⚪", step3="⚪", step4="⚪", step5="⚪", row_count="..."):
#         status_placeholder.markdown(f"""
#         <div class="step-box">
#             <div class="step-item">
#                 <span><span class="step-icon">{step1}</span> Reading your extract</span>
#                 <span class="step-meta">{row_count} rows</span>
#             </div>
#             <div class="step-item">
#                 <span><span class="step-icon">{step2}</span> Loading master reference</span>
#                 <span class="step-meta">v14 · {len(master_lookup)} notes</span>
#             </div>
#             <div class="step-item">
#                 <span><span class="step-icon">{step3}</span> Normalising note numbers & object keys</span>
#                 <span class="step-meta">case · whitespace</span>
#             </div>
#             <div class="step-item">
#                 <span><span class="step-icon">{step4}</span> Matching on the 3-part composite key</span>
#                 <span class="step-meta">note + ref name + ref type</span>
#             </div>
#             <div class="step-item">
#                 <span><span class="step-icon">{step5}</span> Assigning scope and appending columns</span>
#                 <span class="step-meta">2 columns</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     render_steps()
#     time.sleep(0.3)

#     if user_file.name.endswith(".csv"):
#         fresh_df = pd.read_csv(user_file)
#     else:
#         fresh_df = pd.read_excel(user_file)

#     row_count = len(fresh_df)
#     progress_bar.progress(20)
#     render_steps(step1="✅", row_count=f"{row_count:,}")
#     time.sleep(0.3)

#     progress_bar.progress(40)
#     render_steps(step1="✅", step2="✅", row_count=f"{row_count:,}")
#     time.sleep(0.3)

#     progress_bar.progress(60)
#     render_steps(step1="✅", step2="✅", step3="🔵", row_count=f"{row_count:,}")
    
#     # Process Logic Execution
#     fresh_cols = list(fresh_df.columns)
#     col_f_note = find_column(fresh_cols, ["ossnotenumber", "ossnote", "notenumber", "note num", "note"])
#     col_f_type = find_column(fresh_cols, ["reference object type", "refernce object type", "sapobjecttype", "object type", "obj type", "type"])
#     col_f_name = find_column(fresh_cols, ["reference object name", "referenced object", "refernce object", "reference object", "sapobjectname", "obj name", "object name", "name"])
#     col_f_msg = find_column(fresh_cols, ["check message", "check_message", "message", "msg"])

#     if None in (col_f_note, col_f_name, col_f_type):
#         st.error("❌ Column Layout Error: Could not locate columns for Note Number, Reference Object Name, and Reference Object Type.")
#         if st.button("⬅️ Try Another File"):
#             st.session_state["step"] = "upload"
#             st.rerun()
#     else:
#         progress_bar.progress(80)
#         render_steps(step1="✅", step2="✅", step3="✅", step4="🔵", row_count=f"{row_count:,}")
        
#         scopes_list = []
#         match_status_list = []

#         for idx, row in fresh_df.iterrows():
#             note_val = clean_val(row[col_f_note])
#             name_val = clean_val(row[col_f_name])
#             type_val = clean_val(row[col_f_type])
#             msg_val = clean_val(row[col_f_msg]) if col_f_msg else ""

#             has_db_op = any(op in msg_val for op in DB_OPERATIONS)

#             # RULE 1: Hard Override
#             if note_val == "1912445":
#                 assigned_scope = "HCC/HPO"
#                 status = "Matched"

#             # RULE 2: Direct Technical Notes
#             elif note_val in DIRECT_TECHNICAL_NOTES:
#                 assigned_scope = "Technical"
#                 status = "Matched"

#             # RULE 3: Special Note 2198647
#             elif note_val == "2198647" and has_db_op:
#                 if "VBFA" in name_val:
#                     assigned_scope = "Technical"
#                     status = "Matched"
#                 elif any(obj in name_val for obj in ["VBUP", "VBUK"]):
#                     assigned_scope = "Functional"
#                     status = "Matched"
#                 else:
#                     fresh_key = (note_val, name_val, type_val)
#                     if fresh_key in master_lookup:
#                         assigned_scope = master_lookup[fresh_key]
#                         status = "Matched"
#                     else:
#                         assigned_scope = "New / Unmapped Note"
#                         status = "Not Found"

#             # RULE 4: Specific DB-Operation Notes Override List
#             elif note_val in DB_OPERATION_NOTES and has_db_op:
#                 assigned_scope = DB_OPERATION_NOTES[note_val]
#                 status = "Matched"

#             # DEFAULT: Master Database Lookup
#             else:
#                 fresh_key = (note_val, name_val, type_val)
#                 if fresh_key in master_lookup:
#                     assigned_scope = master_lookup[fresh_key]
#                     status = "Matched"
#                 else:
#                     assigned_scope = "New / Unmapped Note"
#                     status = "Not Found"

#             scopes_list.append(assigned_scope)
#             match_status_list.append(status)

#         output_df = fresh_df.copy()
#         output_df["Scope"] = scopes_list
#         output_df["Match_Status"] = match_status_list

#         progress_bar.progress(100)
#         render_steps(step1="✅", step2="✅", step3="✅", step4="✅", step5="✅", row_count=f"{row_count:,}")
        
#         # Display "Please wait" message when all steps are finished
#         wait_placeholder.markdown('<div class="wait-message">⏳ Please wait, loading dashboard...</div>', unsafe_allow_html=True)

#         # Save results and prepare file name: Scoped_<original_name>
#         st.session_state["processed_df"] = output_df
#         export_filename = f"Scoped_{user_file.name}"
        
#         if user_file.name.endswith(".csv"):
#             st.session_state["export_data"] = output_df.to_csv(index=False).encode("utf-8")
#             st.session_state["mime_type"] = "text/csv"
#         else:
#             towrite = io.BytesIO()
#             with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
#                 output_df.to_excel(writer, index=False)
#             st.session_state["export_data"] = towrite.getvalue()
#             st.session_state["mime_type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

#         st.session_state["export_name"] = export_filename

#         time.sleep(1.2)
#         st.session_state["step"] = "dashboard"
#         st.rerun()

# # STEP 3 & 4: DASHBOARD & EXPORT VIEW
# elif st.session_state["step"] in ["dashboard", "export_modal"]:
#     output_df = st.session_state["processed_df"]
#     total_rows = len(output_df)

#     tech_count = len(output_df[output_df["Scope"].str.upper() == "TECHNICAL"])
#     func_count = len(output_df[output_df["Scope"].str.upper() == "FUNCTIONAL"])
#     hcc_count = len(output_df[output_df["Scope"].str.upper() == "HCC/HPO"])
#     unmapped_count = len(output_df[output_df["Scope"].str.contains("New / Unmapped", case=False, na=False)])

#     matched_pct = round(((tech_count + func_count + hcc_count) / total_rows) * 100, 1) if total_rows > 0 else 0

#     col_title, col_btn = st.columns([3, 1])
#     with col_title:
#         st.markdown(f'<div class="main-heading">Just over {matched_pct:.0f}% of this extract is matched</div>', unsafe_allow_html=True)
#     with col_btn:
#         if st.button("📥 Export Scoped File", use_container_width=True):
#             st.session_state["step"] = "export_modal"
#             st.rerun()

#     # Metric Cards Grid
#     st.markdown(f"""
#     <div class="metric-grid">
#         <div class="metric-card card-technical">
#             <div class="metric-label">Matched · Technical</div>
#             <div class="metric-value">{tech_count:,}</div>
#             <div class="metric-subtext">{round((tech_count/total_rows)*100, 1) if total_rows else 0}% of extract</div>
#         </div>
#         <div class="metric-card card-functional">
#             <div class="metric-label">Matched · Functional</div>
#             <div class="metric-value">{func_count:,}</div>
#             <div class="metric-subtext">{round((func_count/total_rows)*100, 1) if total_rows else 0}% of extract</div>
#         </div>
#         <div class="metric-card card-hcc">
#             <div class="metric-label">Matched · HCC/HPO</div>
#             <div class="metric-value">{hcc_count:,}</div>
#             <div class="metric-subtext">Automated classification</div>
#         </div>
#         <div class="metric-card card-unmapped">
#             <div class="metric-label">Unmapped · Unmarked</div>
#             <div class="metric-value">{unmapped_count:,}</div>
#             <div class="metric-subtext">Needs your review</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Filter Options
#     filter_option = st.radio(
#         "Filter View By Scope:",
#         ["All", "Technical", "Functional", "HCC/HPO", "Unmapped"],
#         horizontal=True
#     )

#     filtered_df = output_df.copy()
#     if filter_option == "Technical":
#         filtered_df = output_df[output_df["Scope"].str.upper() == "TECHNICAL"]
#     elif filter_option == "Functional":
#         filtered_df = output_df[output_df["Scope"].str.upper() == "FUNCTIONAL"]
#     elif filter_option == "HCC/HPO":
#         filtered_df = output_df[output_df["Scope"].str.upper() == "HCC/HPO"]
#     elif filter_option == "Unmapped":
#         filtered_df = output_df[output_df["Scope"].str.contains("New / Unmapped", case=False, na=False)]

#     st.dataframe(filtered_df, use_container_width=True, height=360)

#     # EXPORT SECTION ANCHOR & MODAL
#     if st.session_state["step"] == "export_modal":
#         st.markdown('<div id="export-section"></div>', unsafe_allow_html=True)
#         st.markdown("---")
#         st.markdown(f"""
#         <div class="export-card">
#             <div class="export-badge">✓</div>
#             <h2 style="margin:0; font-weight:700;">Your scoped file is ready.</h2>
#             <p style="color:#718096; font-size:0.9rem;">Every original column and row is exactly as you sent it. We only added two columns at the end.</p>
#             <div class="export-meta-box">
#                 <div style="font-weight:bold; font-family:monospace; margin-bottom:8px;">{st.session_state["export_name"]}</div>
#                 <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#4a5568;">
#                     <span><b>ROWS:</b> {total_rows:,}</span>
#                     <span><b>ORIGINAL COLS:</b> {len(output_df.columns)-2}</span>
#                     <span><b>APPENDED:</b> Scope, Match_Status</span>
#                 </div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         c1, c2 = st.columns([1, 1])
#         with c1:
#             st.download_button(
#                 label="📥 Download File",
#                 data=st.session_state["export_data"],
#                 file_name=st.session_state["export_name"],
#                 mime=st.session_state["mime_type"],
#                 use_container_width=True
#             )
#         with c2:
#             if st.button("⬅️ Back to Review", use_container_width=True):
#                 st.session_state["step"] = "dashboard"
#                 st.rerun()

#         st.components.v1.html(
#             """
#             <script>
#                 window.parent.document.getElementById('export-section').scrollIntoView({behavior: 'smooth'});
#             </script>
#             """,
#             height=0
#         )


import os
import io
import time
import streamlit as st
import pandas as pd

# Define local master file path
HARDCODED_MASTER_PATH = "master_data.xlsx"

# -------------------------------------------------------------
# Custom Override Rules Configuration
# -------------------------------------------------------------
DIRECT_TECHNICAL_NOTES = {
    "2199837", "2215424", "2228241", "2348023", "2438006",
    "2438110", "2438131", "2610650", "2628699", "2628704",
    "2628706", "3320010", "2228242", "2669781", "2669857",
    "2670006"
}

DB_OPERATIONS = ["DELETE", "MODIFY", "UPDATE", "SELECT UPDATE", "WRITE"]

DB_OPERATION_NOTES = {
    "2768887": "Technical",
    "2431747": "Functional",
    "2389136": "Functional",
    "2265093": "Functional",
    "1976487": "Functional",
    "2354768": "Functional",
    "2378796": "Technical",
    "2270387": "Functional",
    "2337368": "Functional",
    "2226048": "Functional",
    "2226072": "Functional",
    "2220005": "Technical",
    "2332591": "Functional",
    "2206980": "Functional",
    "2270388": "Technical",
    "2870766": "Functional",
}

# -------------------------------------------------------------
# Streamlit Page Config & Custom Design System
# -------------------------------------------------------------
st.set_page_config(
    page_title="OSS Note Scope Segregator",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    /* Dark Theme Base */
    .stApp {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }
    
    /* Top Header Bar */
    .top-header {
        background-color: #111111;
        padding: 12px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #2a2a2a;
        margin-bottom: 30px;
    }
    .brand-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-subtitle {
        color: #888888;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .version-badge {
        background-color: #24282e;
        color: #9bb0a5;
        border: 1px solid #343a40;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-family: monospace;
    }

    /* Button Styling */
    div.stButton > button,
    div.stDownloadButton > button,
    div[data-testid="stDownloadButton"] > button {
        background-color: #26292f !important;
        border: 1px solid #4a4e58 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div.stButton > button,
    div.stButton > button *,
    div.stButton > button p,
    div.stButton > button span,
    div.stDownloadButton > button,
    div.stDownloadButton > button *,
    div.stDownloadButton > button p,
    div.stDownloadButton > button span,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stDownloadButton"] > button * {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    div.stButton > button:hover,
    div.stDownloadButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #32363e !important;
        border-color: #616775 !important;
    }

    /* File Uploader Outer Box */
    section[data-testid="stFileUploader"] {
        background-color: #111111 !important;
        border: 2px dashed #333333 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-top: 10px !important;
    }
    section[data-testid="stFileUploader"] button {
        background-color: #26292f !important;
        border: 1px solid #4a4e58 !important;
        border-radius: 6px !important;
    }
    section[data-testid="stFileUploader"] button,
    section[data-testid="stFileUploader"] button * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    section[data-testid="stFileUploader"] button:hover {
        background-color: #32363e !important;
    }

    section[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stFileUploader"] span,
    section[data-testid="stFileUploader"] small,
    section[data-testid="stFileUploader"] div {
        color: #cccccc !important;
        font-weight: 600 !important;
    }

    /* User Guide Container */
    .user-guide-container {
        background-color: #111111;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 15px;
        margin-bottom: 25px;
    }
    .user-guide-header {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .guide-step-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 12px;
        color: #d1d5db;
        font-size: 0.92rem;
        line-height: 1.5;
    }
    .guide-step-row:last-child {
        margin-bottom: 0;
    }
    .guide-badge {
        background-color: #26292f;
        border: 1px solid #4a4e58;
        color: #ffffff;
        font-weight: 700;
        border-radius: 50%;
        min-width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
    }

    /* Page Headings */
    .main-heading {
        font-size: 2.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 10px;
    }
    .sub-heading {
        color: #cccccc;
        font-size: 1rem;
        margin-bottom: 20px;
    }

    /* Metric Cards Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-top: 20px;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #111111;
        border-radius: 8px;
        padding: 18px;
        border-top: 3px solid #333;
    }
    .card-technical { border-top-color: #0d5c46; }
    .card-functional { border-top-color: #2b6cb0; }
    .card-hcc { border-top-color: #b7791f; }
    .card-unmapped { border-top-color: #9b2c2c; }

    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #a0aec0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 5px 0;
    }
    .metric-subtext {
        font-size: 0.8rem;
        color: #718096;
    }

    /* Step Checklist Box */
    .step-box {
        background-color: #111111;
        border-radius: 10px;
        padding: 20px 30px;
        border: 1px solid #2d3748;
        margin-top: 20px;
    }
    .step-item {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #1a202c;
        font-size: 0.95rem;
    }
    .step-item:last-child { border-bottom: none; }
    .step-icon { margin-right: 10px; }
    .step-meta { color: #a0aec0; font-family: monospace; }

    /* Please Wait Banner */
    .wait-message {
        background-color: #1c251e;
        border: 1px solid #2d5a35;
        color: #4ade80;
        padding: 14px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        font-size: 1.05rem;
        margin-top: 20px;
    }

    /* Radio Filter Labels */
    div[data-testid="stRadio"] > label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label * {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Export Card Styling */
    .export-card {
        background-color: #ffffff;
        color: #1a202c !important;
        border-radius: 12px;
        padding: 30px;
        max-width: 600px;
        margin: 30px auto 10px auto;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .export-card * { color: #1a202c !important; }
    .export-badge {
        background-color: #e6fffa;
        color: #234e52 !important;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .export-meta-box {
        background-color: #f7fafc;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
        border: 1px solid #e2e8f0;
    }

    /* Hide standard Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Helper functions
def clean_val(val):
    if pd.isna(val):
        return ""
    if isinstance(val, (int, float)):
        return str(int(val))
    return str(val).strip().upper()

def find_column(columns, keywords_priority):
    clean_cols = [str(c).strip().lower() for c in columns]
    for kw in keywords_priority:
        for idx, c in enumerate(clean_cols):
            if kw in c:
                return columns[idx]
    return None

# -------------------------------------------------------------
# Cached Master File Lookup
# -------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_master_lookup(file_path):
    lookup_3part = {}
    note_fallback = {}
    
    if os.path.exists(file_path):
        try:
            # keep_default_na=False stops Pandas from turning 'NA' strings into NaN
            master_df = pd.read_excel(file_path, keep_default_na=False)
            m_cols = list(master_df.columns)

            col_m_note = find_column(m_cols, ["ossnotenumber", "ossnote", "notenumber", "note num", "note", "sap no"])
            col_m_type = find_column(m_cols, ["reference object type", "refernce object type", "sapobjecttype", "object type", "obj type", "type"])
            col_m_name = find_column(m_cols, ["reference object name", "referenced object", "refernce object", "reference object", "sapobjectname", "obj name", "object name", "name"])
            col_m_scope = find_column(m_cols, ["functional assessment", "scope", "cat", "track"])
            col_m_sst = find_column(m_cols, ["sst action", "sst_action", "automated", "sst", "action"])
            col_m_comments = find_column(m_cols, ["comments", "comment", "notes"])

            if col_m_note and col_m_name and col_m_type and col_m_scope:
                for _, row in master_df.iterrows():
                    clean_note = clean_val(row[col_m_note])
                    clean_name = clean_val(row[col_m_name])
                    clean_type = clean_val(row[col_m_type])

                    if not clean_note:
                        continue

                    key = (clean_note, clean_name, clean_type)
                    
                    scope_val = str(row[col_m_scope]).strip() if row[col_m_scope] is not None else ""
                    sst_val = str(row[col_m_sst]).strip() if col_m_sst and row[col_m_sst] is not None else ""
                    comment_val = str(row[col_m_comments]).strip() if col_m_comments and row[col_m_comments] is not None else ""

                    # Primary 3-part composite lookup
                    if key not in lookup_3part or lookup_3part[key]["scope"] in ["", "NAN"]:
                        lookup_3part[key] = {
                            "scope": scope_val,
                            "sst_action": sst_val,
                            "comments": comment_val
                        }

                    # Secondary Note-only fallback lookup
                    if clean_note:
                        if clean_note not in note_fallback or note_fallback[clean_note]["scope"] in ["", "NAN"]:
                            note_fallback[clean_note] = {
                                "scope": scope_val,
                                "sst_action": sst_val,
                                "comments": comment_val
                            }

        except Exception as e:
            st.error(f"Error reading master dataset: {e}")
            
    return lookup_3part, note_fallback

master_lookup, note_fallback_lookup = load_master_lookup(HARDCODED_MASTER_PATH)

# Top Header Bar
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.markdown(
        f"""
        <div class="top-header">
            <div class="brand-title">
                <span>🟩🟧<br>🟦🟥</span>
                <div>
                    OSS Note Scope Segregator
                    <div class="brand-subtitle">SMARTSHIFT PRE-SALES</div>
                </div>
            </div>
            <div class="version-badge">
                🟢 {HARDCODED_MASTER_PATH} · v14
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with header_col2:
    if st.session_state.get("step") in ["dashboard", "export_modal"]:
        if st.button("🔄 Upload New File", use_container_width=True):
            st.session_state["step"] = "upload"
            if "processed_df" in st.session_state:
                del st.session_state["processed_df"]
            st.rerun()

# -------------------------------------------------------------
# Flow Management
# -------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state["step"] = "upload"

# STEP 1: FILE UPLOAD SCREEN
if st.session_state["step"] == "upload":
    st.markdown('<div class="main-heading">Drop in your ATC extract — we\'ll scope every row.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-heading">No setup, no configuration. We match each finding against the master reference on Note Number + Reference Object, then hand back your file untouched with new columns.</div>', unsafe_allow_html=True)

    # USER GUIDE
    st.markdown(
        """
        <div class="user-guide-container">
            <div class="user-guide-header">📖 User Guide</div>
            <div class="guide-step-row">
                <span class="guide-badge">1</span>
                <div><b>Upload File:</b> Upload your extracted Excel/CSV sheet using the box below.</div>
            </div>
            <div class="guide-step-row">
                <span class="guide-badge">2</span>
                <div><b>Automated Matching:</b> This scope tool will match the uploaded file data with the master reference sheet.</div>
            </div>
            <div class="guide-step-row">
                <span class="guide-badge">3</span>
                <div><b>Scope Categorization:</b> It will assign object functional assessment as <b>Technical</b>, <b>Functional</b>, <b>HCC/HPO</b>, or <b>Unmapped</b> based on OSS Note Number, Reference Object Name, Object Type (and Check Message column for a few unique note numbers) with a separate count of each.</div>
            </div>
            <div class="guide-step-row">
                <span class="guide-badge">4</span>
                <div><b>Export Scoped Data:</b> You can download your extracted scoped file and use it for your project review.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # File Uploader
    user_file = st.file_uploader("", type=["csv", "xlsx"], key="triplet_uploader")

    if user_file is not None:
        st.session_state["user_file"] = user_file
        st.session_state["step"] = "processing"
        st.rerun()

# STEP 2: PROCESSING SIMULATION
elif st.session_state["step"] == "processing":
    user_file = st.session_state["user_file"]
    
    st.markdown(f'<div class="sub-heading">{user_file.name}</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-heading">Normalising note numbers & object keys...</div>', unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    wait_placeholder = st.empty()

    def render_steps(step1="⚪", step2="⚪", step3="⚪", step4="⚪", step5="⚪", row_count="..."):
        status_placeholder.markdown(f"""
        <div class="step-box">
            <div class="step-item">
                <span><span class="step-icon">{step1}</span> Reading your extract</span>
                <span class="step-meta">{row_count} rows</span>
            </div>
            <div class="step-item">
                <span><span class="step-icon">{step2}</span> Loading master reference</span>
                <span class="step-meta">v14 · {len(master_lookup)} notes</span>
            </div>
            <div class="step-item">
                <span><span class="step-icon">{step3}</span> Normalising note numbers & object keys</span>
                <span class="step-meta">case · whitespace</span>
            </div>
            <div class="step-item">
                <span><span class="step-icon">{step4}</span> Matching on the 3-part composite key</span>
                <span class="step-meta">note + ref name + ref type</span>
            </div>
            <div class="step-item">
                <span><span class="step-icon">{step5}</span> Assigning functional assessment and appending columns</span>
                <span class="step-meta">4 columns</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_steps()
    time.sleep(0.3)

    if user_file.name.endswith(".csv"):
        fresh_df = pd.read_csv(user_file, keep_default_na=False)
    else:
        fresh_df = pd.read_excel(user_file, keep_default_na=False)

    row_count = len(fresh_df)
    progress_bar.progress(20)
    render_steps(step1="✅", row_count=f"{row_count:,}")
    time.sleep(0.3)

    progress_bar.progress(40)
    render_steps(step1="✅", step2="✅", row_count=f"{row_count:,}")
    time.sleep(0.3)

    progress_bar.progress(60)
    render_steps(step1="✅", step2="✅", step3="🔵", row_count=f"{row_count:,}")
    
    # Process Logic Execution
    fresh_cols = list(fresh_df.columns)
    col_f_note = find_column(fresh_cols, ["ossnotenumber", "ossnote", "notenumber", "note num", "note", "sap no"])
    col_f_type = find_column(fresh_cols, ["reference object type", "refernce object type", "sapobjecttype", "object type", "obj type", "type"])
    col_f_name = find_column(fresh_cols, ["reference object name", "referenced object", "refernce object", "reference object", "sapobjectname", "obj name", "object name", "name"])
    col_f_msg = find_column(fresh_cols, ["check message", "check_message", "message", "msg"])

    if None in (col_f_note, col_f_name, col_f_type):
        st.error("❌ Column Layout Error: Could not locate columns for Note Number, Reference Object Name, and Reference Object Type.")
        if st.button("⬅️ Try Another File"):
            st.session_state["step"] = "upload"
            st.rerun()
    else:
        progress_bar.progress(80)
        render_steps(step1="✅", step2="✅", step3="✅", step4="🔵", row_count=f"{row_count:,}")
        
        assessment_list = []
        match_status_list = []
        automated_list = []
        comments_list = []

        for idx, row in fresh_df.iterrows():
            note_val = clean_val(row[col_f_note])
            name_val = clean_val(row[col_f_name])
            type_val = clean_val(row[col_f_type])
            msg_val = clean_val(row[col_f_msg]) if col_f_msg else ""

            has_db_op = any(op in msg_val for op in DB_OPERATIONS)
            fresh_key = (note_val, name_val, type_val)

            # -------------------------------------------------------------
            # RULE 0: Blank Note Number Check
            # -------------------------------------------------------------
            if not note_val or note_val == "":
                assigned_assessment = "HCC/HPO"
                status = "Matched"
                automated_val = "#N/A"
                comment_val = ""

            # -------------------------------------------------------------
            # RULE 1: Exact 3-Part Key Master Match (FIRST PRIORITY)
            # -------------------------------------------------------------
            elif fresh_key in master_lookup and master_lookup[fresh_key].get("scope") not in ["", "NAN"]:
                master_entry = master_lookup[fresh_key]
                assigned_assessment = master_entry["scope"]
                status = "Matched"
                automated_val = master_entry["sst_action"]
                comment_val = master_entry["comments"]

            # -------------------------------------------------------------
            # RULE 2: Special Note 2198647 Override
            # -------------------------------------------------------------
            elif note_val == "2198647" and has_db_op:
                if "VBFA" in name_val:
                    assigned_assessment = "Technical"
                    status = "Matched"
                    master_entry = note_fallback_lookup.get(note_val, {})
                    automated_val = master_entry.get("sst_action", "")
                    comment_val = master_entry.get("comments", "")
                elif any(obj in name_val for obj in ["VBUP", "VBUK"]):
                    assigned_assessment = "Functional"
                    status = "Matched"
                    automated_val = "NA"
                    comment_val = note_fallback_lookup.get(note_val, {}).get("comments", "")
                elif note_val in note_fallback_lookup and note_fallback_lookup[note_val].get("scope") not in ["", "NAN"]:
                    master_entry = note_fallback_lookup[note_val]
                    assigned_assessment = master_entry["scope"]
                    status = "Matched"
                    automated_val = master_entry["sst_action"]
                    comment_val = master_entry["comments"]
                else:
                    assigned_assessment = "New / Unmapped Note"
                    status = "Not Found"
                    automated_val = ""
                    comment_val = ""

            # -------------------------------------------------------------
            # RULE 3: Direct Technical Notes
            # -------------------------------------------------------------
            elif note_val in DIRECT_TECHNICAL_NOTES:
                assigned_assessment = "Technical"
                status = "Matched"
                master_entry = note_fallback_lookup.get(note_val, {})
                automated_val = master_entry.get("sst_action", "")
                comment_val = master_entry.get("comments", "")

            # -------------------------------------------------------------
            # RULE 4: Special Note 1912445
            # -------------------------------------------------------------
            elif note_val == "1912445":
                assigned_assessment = "HCC/HPO"
                status = "Matched"
                master_entry = note_fallback_lookup.get(note_val, {})
                automated_val = master_entry.get("sst_action", "")
                comment_val = master_entry.get("comments", "")

            # -------------------------------------------------------------
            # RULE 5: DB-Operation Override Notes
            # -------------------------------------------------------------
            elif note_val in DB_OPERATION_NOTES and has_db_op:
                assigned_assessment = DB_OPERATION_NOTES[note_val]
                status = "Matched"
                master_entry = note_fallback_lookup.get(note_val, {})
                automated_val = master_entry.get("sst_action", "")
                comment_val = master_entry.get("comments", "")

            # -------------------------------------------------------------
            # RULE 6: Secondary Note-Level Fallback Match in Master Sheet
            # -------------------------------------------------------------
            elif note_val in note_fallback_lookup and note_fallback_lookup[note_val].get("scope") not in ["", "NAN"]:
                master_entry = note_fallback_lookup[note_val]
                assigned_assessment = master_entry["scope"]
                status = "Matched"
                automated_val = master_entry["sst_action"]
                comment_val = master_entry["comments"]

            else:
                assigned_assessment = "New / Unmapped Note"
                status = "Not Found"
                automated_val = ""
                comment_val = ""

            # STRICT RULE: Force Automated to "NA" whenever Functional Assessment is "Functional"
            if assigned_assessment.upper() == "FUNCTIONAL":
                automated_val = "NA"

            assessment_list.append(assigned_assessment)
            match_status_list.append(status)
            automated_list.append(automated_val)
            comments_list.append(comment_val)

        output_df = fresh_df.copy()
        output_df["Functional Assessment"] = assessment_list
        output_df["Match_Status"] = match_status_list
        output_df["Automated"] = automated_list
        output_df["Comments"] = comments_list

        progress_bar.progress(100)
        render_steps(step1="✅", step2="✅", step3="✅", step4="✅", step5="✅", row_count=f"{row_count:,}")
        
        # Display "Please wait" message
        wait_placeholder.markdown('<div class="wait-message">⏳ Please wait, loading dashboard...</div>', unsafe_allow_html=True)

        # Save results and prepare file name: Scoped_<original_name>
        st.session_state["processed_df"] = output_df
        export_filename = f"Scoped_{user_file.name}"
        
        if user_file.name.endswith(".csv"):
            st.session_state["export_data"] = output_df.to_csv(index=False).encode("utf-8")
            st.session_state["mime_type"] = "text/csv"
        else:
            towrite = io.BytesIO()
            with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
                output_df.to_excel(writer, index=False)
            st.session_state["export_data"] = towrite.getvalue()
            st.session_state["mime_type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        st.session_state["export_name"] = export_filename

        time.sleep(1.2)
        st.session_state["step"] = "dashboard"
        st.rerun()

# STEP 3 & 4: DASHBOARD & EXPORT VIEW
elif st.session_state["step"] in ["dashboard", "export_modal"]:
    output_df = st.session_state["processed_df"]
    total_rows = len(output_df)

    tech_count = len(output_df[output_df["Functional Assessment"].str.upper() == "TECHNICAL"])
    func_count = len(output_df[output_df["Functional Assessment"].str.upper() == "FUNCTIONAL"])
    hcc_count = len(output_df[output_df["Functional Assessment"].str.upper() == "HCC/HPO"])
    unmapped_count = len(output_df[output_df["Functional Assessment"].str.contains("New / Unmapped", case=False, na=False)])

    matched_pct = round(((tech_count + func_count + hcc_count) / total_rows) * 100, 1) if total_rows > 0 else 0

    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown(f'<div class="main-heading">Just over {matched_pct:.0f}% of this extract is matched</div>', unsafe_allow_html=True)
    with col_btn:
        if st.button("📥 Export Scoped File", use_container_width=True):
            st.session_state["step"] = "export_modal"
            st.rerun()

    # Metric Cards Grid
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card card-technical">
            <div class="metric-label">Matched · Technical</div>
            <div class="metric-value">{tech_count:,}</div>
            <div class="metric-subtext">{round((tech_count/total_rows)*100, 1) if total_rows else 0}% of extract</div>
        </div>
        <div class="metric-card card-functional">
            <div class="metric-label">Matched · Functional</div>
            <div class="metric-value">{func_count:,}</div>
            <div class="metric-subtext">{round((func_count/total_rows)*100, 1) if total_rows else 0}% of extract</div>
        </div>
        <div class="metric-card card-hcc">
            <div class="metric-label">Matched · HCC/HPO</div>
            <div class="metric-value">{hcc_count:,}</div>
            <div class="metric-subtext">Automated classification</div>
        </div>
        <div class="metric-card card-unmapped">
            <div class="metric-label">Unmapped · Unmarked</div>
            <div class="metric-value">{unmapped_count:,}</div>
            <div class="metric-subtext">Needs your review</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter Options
    filter_option = st.radio(
        "Filter View By Assessment:",
        ["All", "Technical", "Functional", "HCC/HPO", "Unmapped"],
        horizontal=True
    )

    filtered_df = output_df.copy()
    if filter_option == "Technical":
        filtered_df = output_df[output_df["Functional Assessment"].str.upper() == "TECHNICAL"]
    elif filter_option == "Functional":
        filtered_df = output_df[output_df["Functional Assessment"].str.upper() == "FUNCTIONAL"]
    elif filter_option == "HCC/HPO":
        filtered_df = output_df[output_df["Functional Assessment"].str.upper() == "HCC/HPO"]
    elif filter_option == "Unmapped":
        filtered_df = output_df[output_df["Functional Assessment"].str.contains("New / Unmapped", case=False, na=False)]

    st.dataframe(filtered_df, use_container_width=True, height=360)

    # EXPORT SECTION ANCHOR & MODAL
    if st.session_state["step"] == "export_modal":
        st.markdown('<div id="export-section"></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"""
        <div class="export-card">
            <div class="export-badge">✓</div>
            <h2 style="margin:0; font-weight:700;">Your scoped file is ready.</h2>
            <p style="color:#718096; font-size:0.9rem;">Every original column and row is exactly as you sent it. We added four new columns at the end.</p>
            <div class="export-meta-box">
                <div style="font-weight:bold; font-family:monospace; margin-bottom:8px;">{st.session_state["export_name"]}</div>
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#4a5568;">
                    <span><b>ROWS:</b> {total_rows:,}</span>
                    <span><b>ORIGINAL COLS:</b> {len(output_df.columns)-4}</span>
                    <span><b>APPENDED:</b> Functional Assessment, Match_Status, Automated, Comments</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.download_button(
                label="📥 Download File",
                data=st.session_state["export_data"],
                file_name=st.session_state["export_name"],
                mime=st.session_state["mime_type"],
                use_container_width=True
            )
        with c2:
            if st.button("⬅️ Back to Review", use_container_width=True):
                st.session_state["step"] = "dashboard"
                st.rerun()

        st.components.v1.html(
            """
            <script>
                window.parent.document.getElementById('export-section').scrollIntoView({behavior: 'smooth'});
            </script>
            """,
            height=0
        )
