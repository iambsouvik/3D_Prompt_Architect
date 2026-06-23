import os
import json
import requests
import streamlit as st

# --- 1. Page Configuration & Custom Theme ---
st.set_page_config(
    page_title="3D Asset Prompt Architect",
    page_icon="🎨",
    layout="wide",
)

# Custom CSS for Premium Dark/Neon Cyberpunk Aesthetic
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #00FFCC;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        text-align: center;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
    }
    .stButton>button {
        background: linear-gradient(45deg, #00FFCC, #0099FF);
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Header Section ---
st.markdown("<h1>🎨 3D ASSET PROMPT ARCHITECT ENGINES</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Next-Gen AI Prompt Generator for 3D Artists & Creators</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. Left Sidebar (Advanced Control Panel) ---
with st.sidebar:
    st.markdown("<h2 style='color: #00FFCC;'>🛠️ Control Panel</h2>", unsafe_allow_html=True)
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
        height=120
    )
    
    generate_btn = st.button("🚀 ARCHITECT PROMPT", use_container_width=True)

with col2:
    st.markdown("<h4 style='color: #0099FF;'>💡 Quick Tips:</h4>", unsafe_allow_html=True)
    st.info("1. **Aspect Ratio** directly impacts composition. Use **9:16** for mobile-first content like Shorts, Reels, or TikToks.\n\n"
            "2. When creating human figures or figurines, keep **Subsurface Scattering** selected to achieve ultra-realistic skin depth.", icon="ℹ️")

# --- 5. Library-Free Direct API Engine (FIXED URL VERSION) ---
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
    
    # ⚡ একদম স্ট্যান্ডার্ড মডেল এবং নিখুঁত v1beta এন্ডপয়েন্ট ইউআরএল (Fixes 404)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    system_instruction = (
        "You are a premium 3D Asset Prompt Architect. Generate two distinct variations of a high-fidelity 3D prompt "
        "and one negative prompt based on the user's constraints. Do not include extra chatting, just follow the template structure."
    )
    
    full_query = (
        f"{system_instruction}\n\n"
        f"Create a master-level image generation prompt package for {target_ai}.\n"
        f"Core Concept: {idea}\n"
        f"Base Render Style: {style}\n"
        f"Lighting Configuration: {light}\n"
        f"Material Properties: {materials_str}\n\n"
        f"Format output EXACTLY like this:\n"
        f"VARIATION_1: [Cinematic 3D prompt here including constraints and append '{ar_suffix}']\n"
        f"VARIATION_2: [Alternative unique composition 3D prompt here and append '{ar_suffix}']\n"
        f"NEGATIVE: [Negative prompt to avoid bad anatomy, low quality, flat 2D look]"
    )
    
    headers = {'Content-Type': 'application/json'}
    # v1beta-তে পেলোডের ভেতরেই টেক্সট হিসেবে পুশ করা সবচেয়ে নিরাপদ ও স্টেবল
    payload = {
        "contents": [{"parts": [{"text": full_query}]}],
        "generationConfig": {"temperature": 0.7}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"ERROR_API: Request failed with API Status Code: {response.status_code}. Please try again."
    except Exception as e:
        return f"ERROR_API: Failed to establish connection. Details: {e}"

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
<div style="text-align: center; color: #666666; font-size: 14px; margin-top: 30px; padding: 10px;">
    Developed with ⚡ by 
    <a href="https://www.facebook.com/iambsouvik" target="_blank" style="color: #00FFCC; text-decoration: none; font-weight: bold; border-bottom: 1px dashed #00FFCC;">
        B souvik
    </a>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
