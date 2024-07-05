import streamlit as st
import streamlit.components.v1 as components  # Add this import for custom HTML/JavaScript
import json  # Add this import
import pyperclip 

def get_quickrod_prepend():
    return "/quickRod\n# Task: You will be given a template rod below. Use the template only for structure, formatting, language and style. Use the contents of your analysis for the content of the ROD you will create. Remember to include citations of the Digest in your final rod.\n\n# Template\n"

def home_page():
    st.title("ROD Generator")
    st.write("Select the type of ROD you want to generate:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Regular ROD"):
            st.session_state.rod_type = "regular"
            st.rerun()

    with col2:
        if st.button("Reconsideration ROD", disabled=True):
            st.info("Reconsideration ROD is not active yet.")

    if st.session_state.rod_type == "regular":
        st.subheader("Regular ROD Types")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("VL ROD"):
                st.session_state.rod_subtype = "vl"
                st.session_state.step = 1
                st.rerun()
            if st.button("Dismissal ROD"):
                st.session_state.rod_subtype = "dismissal"
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Antedate ROD"):
                st.session_state.rod_subtype = "antedate"
                st.session_state.step = 1
                st.rerun()
            if st.button("Avail ROD"):
                st.session_state.rod_subtype = "avail"
                st.session_state.step = 1
                st.rerun()

def main():
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = "home"
        st.session_state.inputs = [""] * 5
        st.session_state.final_prompt = ""
        st.session_state.rod_type = ""
        st.session_state.rod_subtype = ""

    # Home page
    if st.session_state.step == "home":
        home_page()

    # Step 1: /readDigest
    elif st.session_state.step == 1:
        st.subheader(f"Step 1: /readDigest for {st.session_state.rod_subtype.upper()} ROD")
        st.session_state.inputs[0] = st.text_area("Paste your text here:", height=200, key="step1")
        if st.button("Next"):
            st.session_state.step = 1.5
            st.rerun()

    # Step 1.5: Display "/readDigest ...continued"
    elif st.session_state.step == 1.5:
        st.subheader("Step 1.5: Copy the following text")
        continued_text = f"/readDigest\n# Relevant Facts\n{st.session_state.inputs[0]}"
        st.text_area("Text to copy:", value=continued_text, height=200, key="step1_5", disabled=True)
        
        # Create a custom HTML button with JavaScript to handle copying
        copy_button_html = f"""
        <button onclick="copyToClipboard()">Copy to Clipboard</button>
        <script>
        function copyToClipboard() {{
            const text = {json.dumps(continued_text)};
            navigator.clipboard.writeText(text).then(function() {{
                alert('Copied to clipboard!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
        </script>
        """
        components.html(copy_button_html, height=50)

        st.info("Click the 'Copy to Clipboard' button to copy the text for the next step.")
        if st.button("Next"):
            st.session_state.step = 2
            st.rerun()

    # Step 2: /rationale
    elif st.session_state.step == 2:
        st.subheader("Step 2: /rationale")
        rationale_text = "/rationale"
        st.text_input("Copy this text:", value=rationale_text, key="rationale_text", disabled=True)
        
        # Create a custom HTML button with JavaScript to handle copying
        copy_button_html = f"""
        <button onclick="copyToClipboard()">Copy to Clipboard</button>
        <script>
        function copyToClipboard() {{
            const text = {json.dumps(rationale_text)};
            navigator.clipboard.writeText(text).then(function() {{
                alert('Copied to clipboard!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
        </script>
        """
        components.html(copy_button_html, height=50)
        
        if st.button("Next"):
            st.session_state.step = 3
            st.rerun()

    # Step 3: Similar ROD input
    elif st.session_state.step == 3:
        st.subheader("Step 3: Similar ROD")
        st.session_state.inputs[2] = st.text_area("Enter a similar ROD:", height=200, key="step3", value=st.session_state.inputs[2])
        if st.button("Next"):
            st.session_state.step = 4
            st.rerun()

    # Step 4: /quickRod
    elif st.session_state.step == 4:
        st.subheader("Step 4: /quickRod")
        prepended_value = get_quickrod_prepend()
        full_text = prepended_value + st.session_state.inputs[2]
        st.session_state.inputs[3] = st.text_area("Enter template ROD:", height=300, key="step4", value=full_text)
        
        # Create a custom HTML button with JavaScript to handle copying
        copy_button_html = f"""
        <button onclick="copyToClipboard()">Copy to Clipboard</button>
        <script>
        function copyToClipboard() {{
            const text = {json.dumps(full_text)};
            navigator.clipboard.writeText(text).then(function() {{
                alert('Copied to clipboard!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
        </script>
        """
        components.html(copy_button_html, height=50)
        if st.button("Next"):
            st.session_state.step = 5
            st.rerun()

    # # Step 5: Final step and generate prompt
    # elif st.session_state.step == 5:
    #     st.subheader("Step 5: Final Input")
    #     st.text_area("Enter any additional input:", height=200, key="step5", value=st.session_state.inputs[4], on_change=update_input, args=(4,))
    #     if st.button("Generate Final Prompt"):
    #         generate_final_prompt()
    #         st.session_state.step = 6
    #         st.rerun()

    # # Display final prompt
    # if st.session_state.step == 6:
    #     st.subheader("Generated Prompt:")
    #     st.text_area("", value=st.session_state.final_prompt, height=400, disabled=True)
    #     if st.button("Start Over"):
    #         st.session_state.step = 1
    #         st.session_state.inputs = [""] * 5
    #         st.session_state.final_prompt = ""
    #         st.rerun()

    # Add a "Back to Home" button at the end of each step
    if st.session_state.step != "home":
        if st.button("Back to Home"):
            st.session_state.step = "home"
            st.session_state.rod_type = ""
            st.session_state.rod_subtype = ""
            st.rerun()

def update_input(step):
    if step == 3:
        # Save the entire input, including the prepended value
        st.session_state.inputs[step] = st.session_state[f"step{step+1}"]
    elif step == 4:
        # Remove the prepended value before saving
        prepended_value = get_quickrod_prepend()
        full_text = st.session_state[f"step{step}"]
        if full_text.startswith(prepended_value):
            st.session_state.inputs[step] = full_text[len(prepended_value):]
        else:
            st.session_state.inputs[step] = full_text
    else:
        st.session_state.inputs[step] = st.session_state[f"step{step+1}"]

def generate_final_prompt():
    prompt = f"/readDigest\n{st.session_state.inputs[0]}\n\n"
    prompt += f"/rationale\n{st.session_state.inputs[1]}\n\n"
    prompt += f"Similar ROD:\n{st.session_state.inputs[2]}\n\n"
    prompt += st.session_state.inputs[3]  # This now includes both the prepended value and user input
    prompt += f"\n\n{st.session_state.inputs[4]}"
    st.session_state.final_prompt = prompt

if __name__ == "__main__":
    main()