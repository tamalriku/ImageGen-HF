# 🎨 Image Generator with Hugging Face and Streamlit

A user-friendly Streamlit web application that generates stunning images using state-of-the-art AI models from Hugging Face.

## ✨ Features

- **7 Powerful AI Models** to choose from, ranked by speed and quality
- **Real-time Image Generation** with visual loading indicators
- **One-Click Download** - Save generated images instantly
- **Model Information** - See speed, quality, and use-case recommendations
- **Beautiful UI** - Clean, intuitive interface with emojis for easy navigation
- **Fast Performance** - Quick image generation with responsive design

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Hugging Face account with an API token
- Git (for deployment)

### Installation (Local)

1. **Clone or download this repository**
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
   
   Get your token from: https://huggingface.co/settings/tokens

5. **Run the app locally**
   ```bash
   streamlit run main.py
   ```
   
   The app will open in your browser at `http://localhost:8501`

## 🎯 How to Use

1. **Select a Model** - Choose from the dropdown in the sidebar (ranked by quality/speed)
2. **View Model Info** - Click "Model Info" to see details about the selected model
3. **Enter Your Prompt** - Describe what you want to generate
4. **Generate** - Click the "🚀 Generate Image" button
5. **Download** - Click the "📥 Download Image" button to save your image

## 📊 Available Models

All models are ranked for your convenience:

| Rank | Model | Speed | Quality | Best For |
|------|-------|-------|---------|----------|
| #1 | FLUX.1-schnell | ⚡ Very Fast | 🎨 Excellent | Quick generations, high quality |
| #2 | FLUX.1-dev | 🐢 Slow | 🌟 Outstanding | Best results, detailed prompts |
| #3 | Stable Diffusion 3 | ⚡ Fast | 🎨 Excellent | Balanced performance |
| #4 | Stable Diffusion XL | ⚡ Fast | 👍 Good | Reliable, general purpose |
| #5 | Kandinsky 3 | ⚡ Fast | 👍 Good | Unique artistic style |
| #6 | Playground v2.5 | ⚡ Fast | 👍 Good | Aesthetic focused |
| #7 | DreamShaper | ⚡ Fast | 👍 Good | Versatile and creative |

**Recommendation:** Start with #1 (FLUX.1-schnell) for a good balance of speed and quality. Use #2 (FLUX.1-dev) for your best results on important prompts.

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub

1. Create a new repository on [GitHub](https://github.com/new)
2. Initialize git and push your code:
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
2. Select **Settings**
3. Go to **Secrets**
4. Add your token:
   ```toml
   HF_TOKEN = "your_huggingface_token_here"
   ```
5. The app will redeploy automatically

**Your app is now live!** Share the URL with anyone. 🎉

## 📋 Requirements

All dependencies are listed in `requirements.txt`:
- `streamlit` - Web app framework
- `transformers` - ML models library
- `langchain` - LLM framework
- `langchain-huggingface` - Hugging Face integration
- `python-dotenv` - Environment variables
- `Pillow` - Image processing
- `huggingface-hub` - Hugging Face API client

## ⚙️ Configuration

### Environment Variables

The app looks for your HF token in this order:
1. **Streamlit Secrets** (`.streamlit/secrets.toml`) - Recommended for deployment
2. **Environment Variables** (`.env`) - For local development

### Local Development (.env)

Create a `.env` file in the project root:
```
HF_TOKEN=your_token_here
```

**Note:** This file is ignored by git (see `.gitignore`) - your token won't be committed!

## 🐛 Troubleshooting

### "streamlit command not found"
```bash
# Install streamlit
pip install streamlit
# Or reinstall all requirements
pip install -r requirements.txt
```

### "HF_TOKEN not found"
- Make sure `.streamlit/secrets.toml` exists with your token
- Or create `.env` file with `HF_TOKEN=your_token`

### Image generation is slow
- Try model #1 (FLUX.1-schnell) for faster results
- Use shorter, more specific prompts

### "No such file or directory: main.py"
- Make sure you're in the project directory
- Check that `main.py` exists

### Image doesn't display after download
- Try refreshing the page (F5)
- Regenerate the image

## 📝 Tips for Better Results

- **Be specific** - "A cute golden retriever wearing sunglasses on a beach" works better than "dog"
- **Include style** - Add art styles like "oil painting", "cyberpunk", "watercolor"
- **Mention lighting** - "soft lighting", "dramatic shadows", "golden hour"
- **Use descriptive words** - More details = better results
- **Try different models** - Each has a unique style

### Example Prompts:
- "A futuristic city at night with flying cars, neon lights, cyberpunk style"
- "A serene Japanese garden with koi fish, cherry blossoms, soft morning light"
- "Portrait of an alien astronaut, detailed, sci-fi, professional lighting"

## 🤝 Contributing

Feel free to improve this project! You can:
- Add more models
- Improve the UI
- Add features like prompt history
- Create preset prompt templates

## 📜 License

This project uses Hugging Face models which have their own licenses. Check their documentation for details.

## 🔗 Useful Links

- [Hugging Face Hub](https://huggingface.co)
- [Streamlit Docs](https://docs.streamlit.io)
- [Get API Token](https://huggingface.co/settings/tokens)
- [Deploy to Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)

## ❓ FAQ

**Q: Can I use this for commercial purposes?**
A: Check the individual model licenses on Hugging Face.

**Q: Why is generation sometimes slow?**
A: Model servers may be under heavy load. Try again or use a faster model (#1 or #3).

**Q: Can I run this offline?**
A: No, it requires internet connection to access Hugging Face models.

**Q: How much does this cost?**
A: Streamlit Cloud hosting is free! Hugging Face may have rate limits for free tier.

**Q: How do I update the models?**
A: Edit `main.py` and modify the `models_data` list. Push to GitHub and it auto-deploys.

---

**Enjoy creating beautiful AI-generated images! 🎨✨**

For questions or issues, check the troubleshooting section or create an issue on GitHub.
