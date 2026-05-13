# 🎨 Image Generator with Hugging Face and Streamlit

A powerful Streamlit web application for AI image generation, editing, and style transfer — powered by state-of-the-art models from Hugging Face.

## ✨ Features

- **7 AI Models for Generation** — ranked by speed and quality
- **Image Editing (img2img)** — modify your generated image with natural language instructions
- **Style Transfer** — upload a reference image, AI analyzes its style, and applies it to your generation
- **Vision-Powered Style Analysis** — uses Qwen2.5-VL or Llama Vision to understand artistic styles
- **Edit History & Revert** — browse previous versions and revert to any point
- **One-Click Download** — save generated images as PNG
- **Multi-Provider Support** — routes through fal-ai, replicate, and wavespeed for maximum compatibility

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Hugging Face account with an API token ([get one here](https://huggingface.co/settings/tokens))
- Git (for deployment)

> **Important:** Your HF token must have **"Make calls to inference providers"** permission enabled.

### Installation (Local)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd HF_Test
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Hugging Face token**
   
   Create a `.streamlit/secrets.toml` file in your project folder:
   ```toml
   HF_TOKEN = "your_huggingface_token_here"
   ```
   
   Or create a `.env` file in the project root:
   ```
   HF_TOKEN=your_token_here
   ```

5. **Run the app**
   ```bash
   streamlit run main.py
   ```
   
   The app will open in your browser at `http://localhost:8501`

## 🎯 How to Use

### 1. Generate an Image (Text-to-Image)

1. **Select a Model** from the sidebar dropdown (ranked by quality/speed)
2. **Enter your prompt** describing what you want to generate
3. **Click "🚀 Generate Image"**
4. **Download** your image with the "📥 Download Image" button

### 2. Edit Your Image (Image-to-Image)

After generating an image, the **"✏️ Edit This Image"** section appears:

1. **Describe the changes** you want (e.g., "Make the sky purple", "Add sunglasses", "Change to watercolor style")
2. **Adjust advanced options** (optional):
   - **Transformation Strength** — low = subtle changes, high = dramatic
   - **Negative prompt** — describe what to avoid
   - **Guidance Scale** — how strictly to follow your prompt
3. **Select a model + provider** for editing
4. **Click "🎨 Apply Changes"**

> The AI uses your existing image as a starting point and modifies it based on your instructions — it's not generating from scratch.

### 3. Style Transfer

Transfer the artistic style from any reference image onto your generated image:

1. **Upload a reference image** (the image whose style you want to copy)
2. **Click "🔍 Analyze Style"** — a vision AI model examines the reference and describes its artistic style
3. **Review/edit the style description** — you can tweak the analysis before applying
4. **Adjust the strength slider** — how dramatically to apply the style
5. **Click "🖌️ Apply Style"** — the style is applied to your generated image

**How it works under the hood:**
- A vision-language model (Qwen2.5-VL or Llama Vision) analyzes the reference image's color palette, art technique, lighting, mood, texture, and visual patterns
- The style description is combined with your original prompt
- The image-to-image model transforms your generated image to match the reference style

### 4. Edit History & Revert

Every edit and style transfer is saved to history:
- **Browse previous versions** in the "🕐 Edit History" section
- **Click "↩️ Revert to this version"** to go back to any previous state

## 📊 Available Models

### Text-to-Image Generation

| Rank | Model | Speed | Quality | Best For |
|------|-------|-------|---------|----------|
| #1 | FLUX.1-schnell | ⚡ Very Fast | 🎨 Excellent | Quick generations, high quality |
| #2 | FLUX.1-dev | 🐢 Slow | 🌟 Outstanding | Best results, detailed prompts |
| #3 | Stable Diffusion 3 | ⚡ Fast | 🎨 Excellent | Balanced performance |
| #4 | Stable Diffusion XL | ⚡ Fast | 👍 Good | Reliable, general purpose |
| #5 | Kandinsky 3 | ⚡ Fast | 👍 Good | Unique artistic style |
| #6 | Playground v2.5 | ⚡ Fast | 👍 Good | Aesthetic focused |
| #7 | DreamShaper | ⚡ Fast | 👍 Good | Versatile and creative |

### Image-to-Image Editing & Style Transfer

These models support taking an existing image and modifying it:

| Model | Provider | Use Case |
|-------|----------|----------|
| FLUX.2-dev | fal-ai | ⭐ Recommended — best quality editing |
| FLUX.1-Kontext-dev | fal-ai | Great context-aware editing |
| Qwen Image Edit 2511 | fal-ai | Strong general-purpose editing |
| FLUX.2-klein-9B | replicate | Lighter, faster edits |
| Qwen Image Edit 2509 | wavespeed | Alternative provider option |

### Vision Models (Style Analysis)

Used automatically for analyzing reference image styles:

| Model | Purpose |
|-------|---------|
| Qwen2.5-VL-72B-Instruct | Primary — best style understanding |
| Qwen2.5-VL-32B-Instruct | Fallback — lighter but still capable |
| Llama-3.2-11B-Vision-Instruct | Fallback — widely available |

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub

1. Create a new repository on [GitHub](https://github.com/new)
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

### Step 2: Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository and branch (`main`)
4. Set main file path to `main.py`
5. Click **"Deploy"**

### Step 3: Add Your Secrets

1. After deployment, click the **⋮** menu (top right)
2. Select **Settings** → **Secrets**
3. Add your token:
   ```toml
   HF_TOKEN = "your_huggingface_token_here"
   ```
4. The app will redeploy automatically

**Your app is now live!** 🎉

## 📋 Requirements

All dependencies are listed in `requirements.txt`:
- `streamlit` — Web app framework
- `huggingface-hub` — Hugging Face Inference API client
- `python-dotenv` — Environment variables
- `Pillow` — Image processing

## ⚙️ Configuration

### Environment Variables

The app looks for your HF token in this order:
1. **Streamlit Secrets** (`.streamlit/secrets.toml`) — Recommended for deployment
2. **Environment Variables** (`.env`) — For local development

### HF Token Permissions

Your token needs these permissions at [hf.co/settings/tokens](https://huggingface.co/settings/tokens):
- ✅ **Make calls to inference providers** — Required for all features
- ✅ **Read access to public gated repos** — For accessing gated models

## 🐛 Troubleshooting

### "HF_TOKEN not found"
- Make sure `.streamlit/secrets.toml` exists with your token
- Or create `.env` file with `HF_TOKEN=your_token`

### Image editing fails with "not supported for task image-to-image"
- The model you selected doesn't support image-to-image on that provider
- Use one of the verified model+provider combos from the dropdown (FLUX.2-dev via fal-ai is recommended)

### Style analysis fails
- Vision models may be temporarily unavailable
- The app tries 3 different vision models automatically
- Try again after a few seconds

### Image generation is slow
- Try model #1 (FLUX.1-schnell) for faster results
- Use shorter, more specific prompts

### "Some providers may require a paid plan"
- Some inference providers charge per request
- Check your HF billing at [hf.co/settings/billing](https://huggingface.co/settings/billing)

## 📝 Tips for Better Results

### Prompt Tips
- **Be specific** — "A golden retriever wearing sunglasses on a beach at sunset" > "dog"
- **Include art style** — "oil painting", "cyberpunk", "watercolor", "photograph"
- **Mention lighting** — "soft lighting", "dramatic shadows", "golden hour"
- **Add atmosphere** — "dreamy", "moody", "vibrant", "serene"

### Editing Tips
- **Low strength (0.2–0.4)** — for subtle tweaks like color adjustments
- **Medium strength (0.5–0.7)** — for noticeable changes like style shifts
- **High strength (0.8–1.0)** — for dramatic transformations

### Style Transfer Tips
- Use reference images with a **clear, distinctive style** (e.g., Van Gogh paintings, anime screenshots, neon photography)
- **Edit the style description** before applying — you can emphasize or remove specific aspects
- **Start with lower strength** and increase gradually

### Example Prompts
- "A futuristic city at night with flying cars, neon lights, cyberpunk style"
- "A serene Japanese garden with koi fish, cherry blossoms, soft morning light"
- "Portrait of an alien astronaut, detailed, sci-fi, professional lighting"

## 🤝 Contributing

Feel free to improve this project! You can:
- Add more models as they become available
- Improve the UI and add new features
- Add prompt history and favorites
- Create preset prompt templates

## 📜 License

This project uses Hugging Face models which have their own licenses. Check their documentation for details.

## 🔗 Useful Links

- [Hugging Face Hub](https://huggingface.co)
- [Streamlit Docs](https://docs.streamlit.io)
- [Get API Token](https://huggingface.co/settings/tokens)
- [HF Inference Providers](https://huggingface.co/docs/inference-providers)
- [Deploy to Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

## ❓ FAQ

**Q: Can I use this for commercial purposes?**
A: Check the individual model licenses on Hugging Face.

**Q: Why is generation sometimes slow?**
A: Model servers may be under heavy load. Try again or use a faster model (#1 or #3).

**Q: Can I run this offline?**
A: No, it requires an internet connection to access Hugging Face models via inference providers.

**Q: How much does this cost?**
A: Streamlit Cloud hosting is free. Hugging Face provides free credits but some providers may charge per request.

**Q: What's the difference between Edit and Style Transfer?**
A: **Edit** lets you describe changes in words (e.g., "make the sky red"). **Style Transfer** analyzes a reference image's visual style and applies it to your image automatically.

**Q: Why do I need to select a provider for editing?**
A: Not all providers support image-to-image. The app lists only verified model+provider combos that actually work.

---

**Enjoy creating beautiful AI-generated images! 🎨✨**

For questions or issues, check the troubleshooting section or create an issue on GitHub.
