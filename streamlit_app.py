import streamlit as st
import streamlit.components.v1 as components
import json

# Add this dictionary at the top of the file, after the imports
gpt_dict = {
    "vl": "https://chatgpt.com/g/g-5Pagxlhnj-vl-gpt-4-0",
    "avail": "https://chatgpt.com/g/g-tC5BSvbVG-avail-gpt-4-0",
    "dismissal": "https://chatgpt.com/g/g-oYlLPnpwS-misconduct-gpt-4-0",
    "antedate": "https://chatgpt.com/g/g-dt0gMdHGf-antedate-gpt-4-0"
}
def get_quickrod_prepend():
    return "/quickRod\n# Task: You will be given a template rod below. Use the template only for structure, formatting, language and style. Use the contents of your analysis for the content of the ROD you will create. Remember to include citations of the Digest in your final rod.\n\n# Template\n"

def home_page():
    st.title("ROD Generator")
    st.write("Select the type of ROD you want to generate:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Regular ROD"):
            st.session_state.rod_type = "regular"

    with col2:
        if st.button("Reconsideration ROD", disabled=True):
            st.info("Reconsideration ROD is not active yet.")

    if st.session_state.rod_type == "regular":
        st.subheader("Regular ROD Types")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("VL ROD"):
                st.session_state.rod_subtype = "vl"
            if st.button("Dismissal ROD"):
                st.session_state.rod_subtype = "dismissal"
        with col2:
            if st.button("Antedate ROD"):
                st.session_state.rod_subtype = "antedate"
            if st.button("Avail ROD"):
                st.session_state.rod_subtype = "avail"

        # Store the GPT link in session state when a ROD subtype is selected
        if st.session_state.rod_subtype:
            st.session_state.gpt_link = gpt_dict.get(st.session_state.rod_subtype)

        # Add a "Start" button to proceed to the next step
        if st.button("Start"):
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
        st.session_state.gpt_link = ""  # New session state variable for GPT link

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
        continued_text = f"/readDigest\n Guidelines: \n - Take your time  \n - Think through each step, use chain of thought reasoning based on the facts provided below. \n - Use your knowledge base to provide citations \n --- \n # Relevant Facts\n{st.session_state.inputs[0]}"
        st.text_area("Text to copy:", value=continued_text, height=200, key="step1_5", disabled=True)
        
        # Display the GPT link
        if st.session_state.gpt_link:
            st.markdown(f"[Click here to open GPT for {st.session_state.rod_subtype.upper()} ROD]({st.session_state.gpt_link})")
            st.info("The link will open in a new tab. Please click it to proceed.")

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
        <div id="copyStatus"></div>
        <script>
        function copyToClipboard() {{
            const text = {json.dumps(rationale_text)};
            const textArea = document.createElement("textarea");
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {{
                document.execCommand('copy');
                document.getElementById("copyStatus").innerHTML = "Copied to clipboard!";
            }} catch (err) {{
                document.getElementById("copyStatus").innerHTML = "Failed to copy. Please try again or copy manually.";
                console.error('Could not copy text: ', err);
            }}
            document.body.removeChild(textArea);
        }}
        </script>
        """
        components.html(copy_button_html, height=70)
        
        st.info("Click the 'Copy to Clipboard' button to copy the text for the next step.")
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