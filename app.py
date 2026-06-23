import os
import json
import requests
import streamlit as st

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="3D Asset Prompt Architect",
    page_icon="🎨",
    layout="wide",
)

# Advanced Custom CSS for Fast Floating Elements & Deep Vibrant Gradient Theme
st.markdown("""
    <style>
    /* New Vibrant Deep Purple & Cyberpunk Magenta Gradient Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1e112a 0%, #0d0714 100%);
        overflow-x: hidden;
    }
    
    /* Neon Pink & Cyan Glowing Header */
    h1 {
        color: #FF007F;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        text-align: center;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.6), 0 0 40px rgba(0, 255, 204, 0.4);
        margin-bottom: 5px;
    }
    
    /* High-Speed Visible Floating Elements (Super Fast Movement) */
    .stApp::before {
        content: "🧠 🤖 🐍 🚀 🏎️ ✏️ 📱 🎨 💻 ☄️";
        font-size: 35px;
        position: fixed;
        top: -100px;
        left: 0;
        width: 100%;
        height: 200%;
        word-spacing: 120px;
        line-height: 200px;
        opacity: 0.35; /* অপাসিটি বাড়ানো হয়েছে যাতে স্পষ্ট দেখা যায় */
        pointer-events: none;
        animation: fastFloatBackground 8s linear infinite; /* স্পিড বাড়ানো হয়েছে (২৫ সেকেন্ড থেকে ৮ সেকেন্ড) */
        white-space: normal;
        z-index: 0;
    }
    
    @keyframes fastFloatBackground {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(150px) rotate(5deg); }
        100% { transform: translateY(300px) rotate(0deg); }
    }

    /* Glassmorphism Containers to make Background Elements Visible */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(26, 15, 38, 0.65) !important; /* আধা-স্বচ্ছ ব্যাকগ্রাউন্ড যাতে পেছনের জিনিস নড়াচড়া করলে বোঝা যায় */
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 10px;
    }

    /* Premium Glowing Input Boxes */
    textarea, input, select {
        background-color: #261736 !important;
        border: 2px solid #3d2354 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
    }
    textarea:focus, select:focus {
        border-color: #FF007F !important;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.6) !important;
    }
    
    /* Ultra-Premium Interactive Button with Radiant Glow */
    .stButton>button {
        background: linear-gradient(135deg, #FF007F 0%, #7000FF 50%, #00FFCC 100%) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: bold !important;
        letter-spacing: 1px;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 30px !important;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4) !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(255, 0, 127, 0.8), 0 0 40px rgba(112, 0, 255, 0.5) !important;
    }
    
    /* Custom Styling for Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #261736 !important;
        border-radius: 8px 8px 0px 0px;
        color: #ffffff !important;
        padding: 10px 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Header Section ---
st.markdown("<h1>🎨 3D ASSET PROMPT ARCHITECT ENGINES</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FFCC; font-weight: 600; letter-spacing: 1px;'>Next-Gen AI Prompt Generator for 3D Artists & Creators</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. Left Sidebar (Advanced Control Panel) ---
with st.sidebar:
    st.markdown("<h2 style='color: #FF007F; text-shadow: 0 0 10px rgba(255,0,127,0.3);'>🛠️ Control Panel</h2>", unsafe_allow_html=True)
    st.write("Configure your rendering parameters:")
    
    ai_model = st.selectbox(
        "Target AI Generator:",
        ["Midjourney v6", "Stable Diffusion XL (SDXL)", "DALL-E 3"]
    )
    
    render_style = st.selectbox(
        "Base 3D Style:",
        ["Pixar Animation Style 3D", "1/7 Scale PVC Figurine", "Hyper-realistic 3D Caricature", "Blender Cycles Tech Render"]
    )
    
    lighting = st.selectbox(
        "Lighting Setup:",
        ["Cinematic Rim Light", "Cyberpunk Neon Volumetric", "Studio Soft Box", "Dramatic Chiaroscuro", "Global Illumination"]
    )
    
    material_list = st.multiselect(
        "Material Textures (Multiple):",
        ["Subsurface Scattering (Skin)", "Matte Vinyl Plastic", "Glossy PVC Ceramic", "Polished Metallic Chrome", "Carbon Fiber", "Frosted Glass"],
        default=["Subsurface Scattering (Skin)"]
    )
    
    aspect_ratio = st.radio(
        "Aspect Ratio (Layout):",
        ["1:1 (Square)", "16:9 (Landscape)", "9:16 (Vertical/Reels)", "4:5 (Instagram)"]
    )
    
    st.write("---")
    st.caption("Selected settings will be automatically injected into the prompt structure.")

# --- 4. Main Panel (User Input & Dashboard) ---
col1, col2 = st.columns([2, 1])

with col1:
    user_concept = st.text_area(
        "💡 Describe your basic 3D Character or Object idea:",
        placeholder="e.g., A cybersecurity hacker coding on a glowing laptop, sitting next to a futuristic mechanical cat...",
        height=130
    )
    
    generate_btn = st.button("🚀 ARCHITECT PROMPT", use_container_width=True)

with col2:
    st.markdown("<h4 style='color: #FF007F;'>💡 Quick Tips:</h4>", unsafe_allow_html=True)
    st.info("1. **Aspect Ratio** directly impacts composition. Use **9:16** for mobile-first content like Shorts, Reels, or TikToks.\n\n"
            "2. When creating human figures or figurines, keep **Subsurface Scattering** selected to achieve ultra-realistic skin depth.", icon="ℹ️")

# --- 5. Universal & Error-Free API Engine ---
def generate_advanced_prompts_raw(idea, target_ai, style, light, materials, aspect):
    
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
    
    if api_key == "YOUR_GEMINI_API_KEY_HERE" or not api_key:
        return "ERROR_KEY: Please configure your Gemini API Key in Streamlit Secrets or Environment Variables."
        
    ar_mapping = {"1:1 (Square)": "--ar 1:1", "16:9 (Landscape)": "--ar 16:9", "9:16 (Vertical/Reels)": "--ar 9:16", "4:5 (Instagram)": "--ar 4:5"}
    ar_suffix = ar_mapping.get(aspect, "--ar 1:1")
    materials_str = ", ".join(materials)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    full_query = (
        f"You are a premium 3D Asset Prompt Architect. Your job is to generate two distinct variations of a high-fidelity 3D prompt "
        f"and one negative prompt based on the user's constraints.\n\n"
        f"Create a master-level image generation prompt package for {target_ai}.\n"
        f"Core Concept: {idea}\n"
        f"Base Render Style: {style}\n"
        f"Lighting Configuration: {light}\n"
        f"Material Properties: {materials_str}\n\n"
        f"Format output EXACTLY like this (do not include any other extra text or conversational chatter):\n"
        f"VARIATION_1: [Cinematic 3D prompt here including constraints and append '{ar_suffix}']\n"
        f"VARIATION_2: [Alternative unique composition 3D prompt here and append '{ar_suffix}']\n"
        f"NEGATIVE: [Negative prompt to avoid bad anatomy, low quality, flat 2D look]"
    )
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": full_query}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"ERROR_API: Server responded with status code {response.status_code}. Please try again."
    except Exception as e:
        return f"ERROR_API: Connection error. Details: {e}"

# --- 6. Output Dashboard Display ---
if generate_btn:
    if not user_concept.strip():
        st.warning("Please type your core idea inside the '💡' input box first.")
    else:
        st.write("---")
        with st.spinner("Architecting premium 3D prompt variations..."):
            raw_output = generate_advanced_prompts_raw(
                user_concept, ai_model, render_style, lighting, material_list, aspect_ratio
            )
            
            if "ERROR_KEY" in raw_output:
                st.error(raw_output)
            elif "ERROR_API" in raw_output:
                st.error(raw_output)
            else:
                v1, v2, neg = "", "", ""
                for line in raw_output.split("\n"):
                    if line.startswith("VARIATION_1:"):
                        v1 = line.replace("VARIATION_1:", "").strip()
                    elif line.startswith("VARIATION_2:"):
                        v2 = line.replace("VARIATION_2:", "").strip()
                    elif line.startswith("NEGATIVE:"):
                        neg = line.replace("NEGATIVE:", "").strip()
                
                if not v1: v1 = raw_output
                
                tab1, tab2, tab3 = st.tabs(["🔥 Variation 1 (Cinematic)", "🎬 Variation 2 (Dynamic)", "🚫 Negative Prompt"])
                
                with tab1:
                    st.markdown("<p style='color: #00FFCC;'><b>Cinematic & Highly Detailed Prompt:</b></p>", unsafe_allow_html=True)
                    st.code(v1, language="text")
                with tab2:
                    st.markdown("<p style='color: #0099FF;'><b>Dynamic Composition/Alternative Prompt:</b></p>", unsafe_allow_html=True)
                    st.code(v2, language="text")
                with tab3:
                    st.markdown("<p style='color: #FF3366;'><b>Negative Prompt (Exclude deformities & artifacts):</b></p>", unsafe_allow_html=True)
                    st.code(neg, language="text")
                    
                st.success("✨ Premium prompt configurations successfully generated!")

# --- 7. Premium Custom Footer Credits ---
st.write("---")
footer_html = """
<div style="text-align: center; color: #ffffff; font-size: 14px; margin-top: 30px; padding: 12px; background: rgba(38, 23, 54, 0.8); border-radius: 10px; border: 1px solid rgba(255, 0, 127, 0.3);">
    Developed with ⚡ by 
    <a href="https://www.facebook.com/iambsouvik" target="_blank" style="color: #00FFCC; text-decoration: none; font-weight: bold; text-shadow: 0 0 8px rgba(0,255,204,0.5);">
        B souvik
    </a>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
