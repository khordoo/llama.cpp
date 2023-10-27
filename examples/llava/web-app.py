import os
import argparse
import subprocess
import streamlit as st
from PIL import Image

parser = argparse.ArgumentParser(description='LLaVa GUI using Llama.cpp')
parser.add_argument('--mml-model-path', action='append', default='models/ggml-model-q4_k.gguf',
                    help="Define the local path to your gguf model")
parser.add_argument('--mproj-path', action='append', default='models/mmproj-model-f16.gguf',
                    help="Define the local path model f16 path")
parser.add_argument('--temp', action='append', default='0.1',
                    help="Define the temperature for llm")

try:
    args = parser.parse_args()
except SystemExit as e:
    # This exception will be raised if --help or invalid command line arguments
    # are used. Currently streamlit prevents the program from exiting normally
    # so we have to do a hard exit.
    os._exit(e.code)

image_path = '../../media/llama-leader.jpeg'
default_image = Image.open(image_path)

st.set_page_config(layout="wide", page_title="LlaVA")

st.write("## LLaVA-GUI: Large Language and Vision Assistant")
left_col, _ = st.columns(2)
st.sidebar.write("## Upload an image:")

uploaded_image = st.sidebar.file_uploader("uploader", type=["jpg", "jpeg"], label_visibility='hidden')
inference_result_box = st.sidebar.empty()

if uploaded_image:
    left_col.image(uploaded_image)
    image_path = os.path.join("./", uploaded_image.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
else:
    left_col.image(default_image)

user_question = left_col.text_input(label='user_query', placeholder="Ask your question about the image",
                                    label_visibility='hidden')

st.markdown("""
   <style>
   div.stButton > button:first-child {
       background-color: #FF8C00;
       color:#ffffff;
   }
   div.stButton > button:hover {
       background-color: #FFA500;
       color:#ffffff;
       }
   </style>""", unsafe_allow_html=True)

send_btn = left_col.button("Send")
loading_placeholder = st.empty()


def run_llava(user_question, image_path):
    """
    Runs LLaVA using llama.cpp
    """
    command = ["./llava", "-m", args.mml_model_path, "--mmproj", args.mproj_path, "--temp",
               args.temp, "--image", image_path, "-p", user_question]
    lines = []
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
        while True:
            line = process.stdout.readline()
            if 'llama_print_timings' in line:
                st.sidebar.write(lines[-1])
                process.communicate()
                break
            lines.append(line)
            if not line:
                process.communicate()
                break  # No more data is being generated
    process.wait()


if send_btn:
    with loading_placeholder:
        with st.spinner("Generating..."):
            if not uploaded_image:
                st.warning('Please upload an image first', icon="⚠️")
            else:
                run_llava(user_question, image_path)
        st.success('Done!')

st.markdown('#')
with st.expander("Terms of use"):
    st.write(
        """By using this service, users are required to agree to the following terms:
        The service is a research preview intended for non-commercial use only.
        It only provides limited safety measures and may generate offensive content.
        It must not be used for any illegal, harmful, violent, racist, or sexual purposes.
        For an optimal experience, please use desktop computers for this demo, as mobile devices may compromise its quality.
        """)
