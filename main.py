import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(page_title="Image Generator", layout="wide")
st.title("🎨 Image Generator with Hugging Face")

# Initialize session state
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# Get API key from secrets or environment
hf_token = st.secrets.get("HF_TOKEN") or os.environ.get("HF_TOKEN")

if not hf_token:
    st.error("❌ HF_TOKEN not found. Please set it in Streamlit secrets.")
    st.stop()

client = InferenceClient(
    provider="auto",
    api_key=hf_token,
)

# Available models with rankings and descriptions
models_data = [
    {
        "rank": 1,
        "name": "FLUX.1-schnell",
        "id": "black-forest-labs/FLUX.1-schnell",
        "speed": "⚡ Very Fast",
        "quality": "🎨 Excellent",
        "description": "Ultra-fast, high quality. Best for quick generations."
    },
    {
        "rank": 2,
        "name": "FLUX.1-dev",
        "id": "black-forest-labs/FLUX.1-dev",
        "speed": "🐢 Slow",
        "quality": "🌟 Outstanding",
        "description": "Highest quality but slower. Best results for detailed prompts."
    },
    {
        "rank": 3,
        "name": "Stable Diffusion 3 Medium",
        "id": "stabilityai/stable-diffusion-3-medium",
        "speed": "⚡ Fast",
        "quality": "🎨 Excellent",
        "description": "Great balance of speed and quality."
    },
    {
        "rank": 4,
        "name": "Stable Diffusion XL",
        "id": "stabilityai/stable-diffusion-xl-base-1.0",
        "speed": "⚡ Fast",
        "quality": "👍 Good",
        "description": "Reliable and widely used model."
    },
    {
        "rank": 5,
        "name": "Kandinsky 3",
        "id": "kandinsky-community/kandinsky-3",
        "speed": "⚡ Fast",
        "quality": "👍 Good",
        "description": "Unique artistic style."
    },
    {
        "rank": 6,
        "name": "Playground v2.5",
        "id": "playgroundai/playground-v2.5-1024px-aesthetic",
        "speed": "⚡ Fast",
        "quality": "👍 Good",
        "description": "Aesthetic focused model."
    },
    {
        "rank": 7,
        "name": "DreamShaper",
        "id": "Lykon/dreamshaper-8",
        "speed": "⚡ Fast",
        "quality": "👍 Good",
        "description": "Versatile and creative."
    }
]

# Create model display options
model_options = [f"#{d['rank']} - {d['name']} ({d['speed']} | {d['quality']})" for d in models_data]
model_info = {f"#{d['rank']} - {d['name']} ({d['speed']} | {d['quality']})": d for d in models_data}

# Sidebar
with st.sidebar:
    st.header("Settings")
    selected_option = st.selectbox("Select Model", model_options)
    selected_model_data = model_info[selected_option]
    selected_model_id = selected_model_data["id"]
    selected_model_name = selected_model_data["name"]
    
    # Show model description
    with st.expander("ℹ️ Model Info"):
        st.markdown(f"**{selected_model_data['name']}**")
        st.write(f"📊 Speed: {selected_model_data['speed']}")
        st.write(f"🎨 Quality: {selected_model_data['quality']}")
        st.write(f"💡 {selected_model_data['description']}")

# Main content
prompt = st.text_area("Enter your prompt:", value="Astronaut riding a horse on the moon with earth in the background", height=100)

col1, col2 = st.columns(2)
with col1:
    generate_button = st.button("🚀 Generate Image", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.session_state.generated_image = None
    st.rerun()

if generate_button:
    if not prompt.strip():
        st.warning("Please enter a prompt!")
    else:
        with st.spinner(f"Generating image with {selected_model_name}..."):
            try:
                image = client.text_to_image(prompt, model=selected_model_id)
                st.session_state.generated_image = image
            except Exception as e:
                st.error(f"Error generating image: {str(e)}")

# Display image if it exists
if st.session_state.generated_image:
    st.image(st.session_state.generated_image, caption=f"Generated with {selected_model_name}")
    
    # Convert PIL image to bytes for download
    img_byte_arr = BytesIO()
    st.session_state.generated_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    st.download_button(
        label="📥 Download Image",
        data=img_byte_arr.getvalue(),
        file_name="generated_image.png",
        mime="image/png",
        use_container_width=True
    )