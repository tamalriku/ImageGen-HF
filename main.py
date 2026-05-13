import os
import base64
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
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = None
if "selected_model_id" not in st.session_state:
    st.session_state.selected_model_id = None
if "selected_model_name" not in st.session_state:
    st.session_state.selected_model_name = None
if "style_description" not in st.session_state:
    st.session_state.style_description = None
if "reference_image_bytes" not in st.session_state:
    st.session_state.reference_image_bytes = None

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
    st.session_state.current_prompt = None
    st.session_state.selected_model_id = None
    st.session_state.selected_model_name = None
    st.rerun()

if generate_button:
    if not prompt.strip():
        st.warning("Please enter a prompt!")
    else:
        with st.spinner(f"Generating image with {selected_model_name}..."):
            try:
                image = client.text_to_image(prompt, model=selected_model_id)
                st.session_state.generated_image = image
                st.session_state.current_prompt = prompt
                st.session_state.selected_model_id = selected_model_id
                st.session_state.selected_model_name = selected_model_name
            except Exception as e:
                st.error(f"Error generating image: {str(e)})")

# Display image if it exists
if st.session_state.generated_image:
    st.image(st.session_state.generated_image, caption=f"Generated with {st.session_state.selected_model_name}")
    
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
    
    # ── Edit & Regenerate Image (image-to-image) ──
    st.divider()
    st.subheader("✏️ Edit This Image")
    st.caption(
        "Describe how you'd like to change the generated image. "
        "The AI will use the current image as a starting point and apply your edits."
    )

    # Show context about the current image
    st.markdown(f"**Original prompt:** {st.session_state.current_prompt}")
    st.markdown(f"**Model used:** {st.session_state.selected_model_name}")

    # Edit prompt
    edit_prompt = st.text_area(
        "Describe the changes you want:",
        placeholder="e.g. 'Make the sky purple and add northern lights' or 'Change the style to watercolor painting'",
        height=100,
        key="edit_prompt_area",
    )

    # Advanced options in an expander
    with st.expander("⚙️ Advanced Options"):
        # Strength slider — how much the image should change
        strength = st.slider(
            "Transformation Strength",
            min_value=0.1,
            max_value=1.0,
            value=0.65,
            step=0.05,
            help="Low = subtle changes (keeps more of the original). High = dramatic changes.",
            key="strength_slider",
        )

        # Negative prompt
        negative_prompt = st.text_input(
            "Negative prompt (what to avoid):",
            placeholder="e.g. 'blurry, low quality, distorted'",
            key="negative_prompt_input",
        )

        # Guidance scale
        guidance_scale = st.slider(
            "Guidance Scale",
            min_value=1.0,
            max_value=20.0,
            value=7.5,
            step=0.5,
            help="How closely to follow the prompt. Higher = stricter adherence.",
            key="guidance_scale_slider",
        )

    # Provider + model combinations that ACTUALLY support image-to-image
    # (verified from https://huggingface.co/models?pipeline_tag=image-to-image&inference_provider=all)
    img2img_options = [
        ("FLUX.2-dev via fal-ai (Recommended)", "fal-ai", "black-forest-labs/FLUX.2-dev"),
        ("FLUX.1-Kontext-dev via fal-ai", "fal-ai", "black-forest-labs/FLUX.1-Kontext-dev"),
        ("Qwen Image Edit via fal-ai", "fal-ai", "Qwen/Qwen-Image-Edit-2511"),
        ("FLUX.2-klein-9B via replicate", "replicate", "black-forest-labs/FLUX.2-klein-9B"),
        ("Qwen Image Edit via wavespeed", "wavespeed", "Qwen/Qwen-Image-Edit-2509"),
    ]
    option_names = [o[0] for o in img2img_options]

    selected_idx = st.selectbox(
        "Model + Provider for editing:",
        range(len(option_names)),
        format_func=lambda i: option_names[i],
        key="edit_model_select",
    )
    _, edit_provider, edit_model_id = img2img_options[selected_idx]

    # Edit button
    if st.button("🎨 Apply Changes", use_container_width=True, key="apply_edit_btn"):
        if not edit_prompt.strip():
            st.warning("Please describe the changes you want to make!")
        else:
            # Convert current image to raw bytes for the API
            img_buffer = BytesIO()
            st.session_state.generated_image.save(img_buffer, format="PNG")
            img_bytes = img_buffer.getvalue()

            with st.spinner(f"Editing image via {edit_provider}..."):
                edited_image = None

                try:
                    img2img_client = InferenceClient(
                        provider=edit_provider,
                        api_key=hf_token,
                    )
                    # Pass image as raw bytes (first positional arg)
                    edited_image = img2img_client.image_to_image(
                        img_bytes,
                        prompt=edit_prompt,
                        model=edit_model_id,
                        strength=strength,
                        guidance_scale=guidance_scale,
                    )
                except Exception as e:
                    st.error(
                        f"❌ Image editing failed with **{edit_provider}** + **{edit_model_id}**\n\n"
                        f"**Error:** {str(e)}\n\n"
                        f"💡 **Tips:**\n"
                        f"- Try a different Model + Provider combo from the dropdown\n"
                        f"- Make sure your HF token has 'Inference Providers' permission enabled at "
                        f"[hf.co/settings/tokens](https://hf.co/settings/tokens)\n"
                        f"- Some providers may require a paid plan"
                    )

                if edited_image is not None:
                    # Store old image in history before overwriting
                    if "image_history" not in st.session_state:
                        st.session_state.image_history = []
                    st.session_state.image_history.append({
                        "image": st.session_state.generated_image,
                        "prompt": st.session_state.current_prompt,
                    })

                    st.session_state.generated_image = edited_image
                    st.session_state.current_prompt = edit_prompt
                    st.session_state.selected_model_name = option_names[selected_idx]
                    st.session_state.selected_model_id = edit_model_id
                    st.success("✅ Image edited successfully!")
                    st.rerun()

    # ── Style Transfer ──
    st.divider()
    st.subheader("🖌️ Style Transfer")
    st.caption(
        "Upload a reference image to analyze its artistic style, "
        "then apply that style to your generated image."
    )

    # Reference image uploader
    ref_image_file = st.file_uploader(
        "Upload a reference image:",
        type=["png", "jpg", "jpeg", "webp"],
        key="ref_image_uploader",
    )

    if ref_image_file is not None:
        ref_bytes = ref_image_file.getvalue()
        ref_pil = Image.open(BytesIO(ref_bytes))

        # Show reference image preview
        st.image(ref_pil, caption="Reference Image", width=300)

        # --- Analyze Style button ---
        if st.button("🔍 Analyze Style", use_container_width=True, key="analyze_style_btn"):
            with st.spinner("Analyzing the style of the reference image..."):
                try:
                    # Encode image as base64 data URL for the vision model
                    ref_b64 = base64.b64encode(ref_bytes).decode("utf-8")
                    mime_type = ref_image_file.type or "image/png"
                    data_url = f"data:{mime_type};base64,{ref_b64}"

                    # Use a vision model to analyze the style
                    style_messages = [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": data_url},
                                },
                                {
                                    "type": "text",
                                    "text": (
                                        "Analyze the artistic style of this image in detail. "
                                        "Describe the following aspects in a concise paragraph that can be used "
                                        "as a style prompt for image generation:\n"
                                        "- Color palette (specific colors, warm/cool tones, saturation)\n"
                                        "- Art technique (oil painting, watercolor, digital art, photography, etc.)\n"
                                        "- Lighting (soft, dramatic, natural, neon, etc.)\n"
                                        "- Mood/atmosphere (dreamy, dark, vibrant, serene, etc.)\n"
                                        "- Texture and detail level\n"
                                        "- Any distinctive visual elements or patterns\n\n"
                                        "Output ONLY the style description as a single paragraph, nothing else. "
                                        "Start with 'In the style of...'"
                                    ),
                                },
                            ],
                        }
                    ]

                    # Try vision models in order of preference
                    vision_models = [
                        "Qwen/Qwen2.5-VL-72B-Instruct",
                        "Qwen/Qwen2.5-VL-32B-Instruct",
                        "meta-llama/Llama-3.2-11B-Vision-Instruct",
                    ]
                    style_text = None
                    for vm in vision_models:
                        if style_text is not None:
                            break
                        try:
                            response = client.chat_completion(
                                model=vm,
                                messages=style_messages,
                                max_tokens=300,
                            )
                            style_text = response.choices[0].message.content
                        except Exception:
                            continue

                    if style_text:
                        st.session_state.style_description = style_text
                        st.session_state.reference_image_bytes = ref_bytes
                        st.rerun()
                    else:
                        st.error("Could not analyze style. No vision model available.")
                except Exception as e:
                    st.error(f"Error analyzing style: {str(e)}")

        # Show style analysis result if available
        if st.session_state.style_description:
            st.success("✅ Style analyzed!")
            style_prompt = st.text_area(
                "Detected style (you can edit this):",
                value=st.session_state.style_description,
                height=120,
                key="style_prompt_area",
            )

            # Style strength
            style_strength = st.slider(
                "Style Transfer Strength",
                min_value=0.1,
                max_value=1.0,
                value=0.70,
                step=0.05,
                help="How strongly to apply the style. Low = subtle, High = dramatic.",
                key="style_strength_slider",
            )

            # Model selection for style transfer (reuse img2img models)
            style_transfer_options = [
                ("FLUX.2-dev via fal-ai", "fal-ai", "black-forest-labs/FLUX.2-dev"),
                ("FLUX.1-Kontext-dev via fal-ai", "fal-ai", "black-forest-labs/FLUX.1-Kontext-dev"),
                ("Qwen Image Edit via fal-ai", "fal-ai", "Qwen/Qwen-Image-Edit-2511"),
            ]
            st_option_names = [o[0] for o in style_transfer_options]

            st_selected_idx = st.selectbox(
                "Model for style transfer:",
                range(len(st_option_names)),
                format_func=lambda i: st_option_names[i],
                key="style_model_select",
            )
            _, st_provider, st_model_id = style_transfer_options[st_selected_idx]

            # Apply Style button
            if st.button("🖌️ Apply Style", use_container_width=True, key="apply_style_btn"):
                # Build the style transfer prompt
                full_style_prompt = (
                    f"{st.session_state.current_prompt}. {style_prompt}"
                )

                # Convert generated image to bytes
                gen_buffer = BytesIO()
                st.session_state.generated_image.save(gen_buffer, format="PNG")
                gen_bytes = gen_buffer.getvalue()

                with st.spinner(f"Applying style via {st_provider}..."):
                    try:
                        style_client = InferenceClient(
                            provider=st_provider,
                            api_key=hf_token,
                        )
                        styled_image = style_client.image_to_image(
                            gen_bytes,
                            prompt=full_style_prompt,
                            model=st_model_id,
                            strength=style_strength,
                        )

                        # Save to history before overwriting
                        if "image_history" not in st.session_state:
                            st.session_state.image_history = []
                        st.session_state.image_history.append({
                            "image": st.session_state.generated_image,
                            "prompt": st.session_state.current_prompt,
                        })

                        st.session_state.generated_image = styled_image
                        st.session_state.current_prompt = full_style_prompt
                        st.session_state.selected_model_name = st_option_names[st_selected_idx]
                        st.session_state.selected_model_id = st_model_id
                        st.success("✅ Style applied successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(
                            f"❌ Style transfer failed with **{st_provider}** + **{st_model_id}**\n\n"
                            f"**Error:** {str(e)}\n\n"
                            f"💡 Try a different model from the dropdown."
                        )

    # Show edit history if it exists
    if "image_history" in st.session_state and st.session_state.image_history:
        st.divider()
        st.subheader("🕐 Edit History")
        st.caption("Previous versions of your image (most recent first)")
        for i, entry in enumerate(reversed(st.session_state.image_history)):
            with st.expander(f"Version {len(st.session_state.image_history) - i}: \"{entry['prompt'][:60]}...\""):
                st.image(entry["image"], use_container_width=True)
                st.caption(f"Prompt: {entry['prompt']}")
                if st.button(
                    "↩️ Revert to this version",
                    key=f"revert_btn_{i}",
                    use_container_width=True,
                ):
                    st.session_state.generated_image = entry["image"]
                    st.session_state.current_prompt = entry["prompt"]
                    st.rerun()