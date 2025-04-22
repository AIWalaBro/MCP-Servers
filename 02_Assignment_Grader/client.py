import streamlit as st
import requests
import os
import tempfile
import time

st.set_page_config(
    page_title="Assignment Grader",
    page_icon="📝",
    layout="wide",)

# main title
st.title("Assignment Grader")
st.markdown("This is a simple assignment grader that uses the MCP server to grade your assignments.")

# sidebar for user input
st.sidebar.title("User Input")
st.sidebar.info("""This is assignment grader using FastMCP and OpenAI. " 
                Uplaod assignment in PDF or DOCX format. set your grading rubric,
                and get instant AI-Powereed graders with detailed feedback""")

# create a tab
tab1, tab2 , tab3 = st.tabs(["Upload Assignment", "Grading Assignment", "Results"])

# for tab1 ceate a file uploader
with tab1:
    st.header("Upload Assignment")

    # file upload
    uploaded_file = st.file_uploader("choose a file", type=["pdf", "docx"], key="file_uploader")

    # write logic after file upload
    if uploaded_file is not None:
        # save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splittext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            file_path = temp_file.name

            st.session_state['file_path'] = file_path
            st.session_state['file_name'] = uploaded_file.name

            # Parse the file to extract text
            if st.button("Process Document"):
                with st.spinner("Processing document..."):
                    result = call_mcp_tool("parse_file", {"file_path": file_path})

                    if result is None:
                        st.error("Failed to process document. Check server connection.")
                    elif isinstance(result, str):
                        # If result is  string, its either the document text or an error message.
                        st.session_state['document_text'] = result
                        st.success("Document processed successfully!")
                        st.info(f"Document contains {len(result.split())} words")

                        # show preview of the document text
                        with st.expander("Preview Document Text"):
                            st.text(result[:1000] + ("..." if len(result) > 1000 else ""))

                    else:
                        # if result is dict, might be error information
                        st.session_state['document_text'] = str(result)
                        st.success(f"Document processed successfully!")

                        # show preview
                        with st.expander("Preview Document Text"):
                            st.json(result, expanded=True)



#  TAB 2 - Grading Assignment
with tab2:
    st.header("Grading Configuration")

    # Rubric Input

    st.subheader("Grading Rubric")
    rubric = st.text_area(
        "Enter your grading rubric here. This will be used to grade the assignment. "
        "Please provide a detailed rubric for better results.",
        height=200,
        help="specify the criteria for grading the assignment. ",
        value="content (40%): The assignment should cover the topic in detail.\n"
              "Structure (20%): The assignment should be clear and easy to understand.\n"
              "Analysis (30%): The assignment should show creativity and originality.\n"
              "grammar and style (10%): The assignment should be free of grammatical errors."
    )

    # plagarism check option
    check_plagiarism_option = st.checkbox("Check for Plagiarism", value=True, help="Check the assignment for plagiarism using AI.")

    if "document_text" in st.session_state and st.button("Grade Assignment"):
        # store rubric session state
        st.session_state['rubric'] = rubric

        with st.spinner("Grading in progress.."):
            # optional plgarism checcker
            if check_plagiarism_option:
                st.info("Checking for plagiarism...")
                plagiarism_result = call_mcp_tool("check_plagiarism", {"text": st.session_state['document_text']})
                st.session_state['plagiarism_result'] = plagiarism_result
                if plagiarism_result is None:
                    st.warning()
