import time
from google import genai
import streamlit as st

# Configure page layout
st.set_page_config(
    page_title="Beauty Creator Suite",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------
# 🎨 LUXURY UI, CUSTOM CSS & STREAMLIT MENU HIDING
# -------------------------------------------------------------------
st.markdown(
    """
<style>
    /* Hide Streamlit Header & Footer for Clean SaaS Look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Background & Font */
    .stApp {
        background-color: #0e1117;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Title Styling */
    h1 {
        background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Subheader & Captions */
    p, .stCaption {
        color: #cbd5e1;
    }

    /* Custom Input Containers / Cards */
    div[data-testid="stForm"], .css-1r6slb0, .stTabs {
        background-color: #161b22;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #30363d;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #21262d;
        border-radius: 8px;
        color: #ffffff;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid #30363d;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%) !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* Custom Buttons (Gradient Luxury Look) */
    .stButton > button {
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        border: none;
        box-shadow: 0 4px 14px rgba(255, 117, 140, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 117, 140, 0.6);
    }

    /* Expander Box */
    .streamlit-expanderHeader {
        background-color: #1f242d;
        border-radius: 8px;
        color: #ff7eb3 !important;
        font-weight: 600;
    }

    /* Success / Warning Banners */
    .stAlert {
        border-radius: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# 🔄 HELPER FUNCTION WITH MULTI-MODEL FALLBACK & RETRY (FIXES 503 ERROR)
# -------------------------------------------------------------------
def generate_ai_response(client, prompt):
  """Tries gemini-2.5-flash first.

  If Google returns a 503, automatically falls back to gemini-1.5-flash and
  gemini-2.0-flash.
  """
  models_to_try = [
      "gemini-3.8-flash",
      "gemini-3.6-flash"
  ]

  for model_name in models_to_try:
    try:
      response = client.models.generate_content(
          model=model_name, contents=prompt,
          config={
              "temperature": 0.7,  # Faster, more direct output
              "max_output_tokens": 1000,  # Limits token generation length for quick delivery
          },
      )
      return response.text
    except Exception as e:
      error_msg = str(e)
      # If model is unavailable or overloaded (503), switch to next model silently
      if "503" in error_msg or "UNAVAILABLE" in error_msg:
        time.sleep(1)
        continue
      raise e

  raise Exception(
      "Google AI servers are busy. Please try again after some time."
      " clusters."
  )


# -------------------------------------------------------------------
# APP HEADER
# -------------------------------------------------------------------
st.title("💄 Beauty Creator Suite")
st.markdown(
    "### *The Ultimate AI Content & PR Engine for Elite Beauty Influencers*"
)
st.caption(
    "✨ Generate viral Instagram reel scripts, FTC-compliant captions, and"
    " high-converting brand PR pitches in seconds."
)

# Quick App Installation Guide Expander
with st.expander(
    "📱💻 Click Here: How to Install Beauty Creator Suite as an App on Your"
    " Phone or Laptop"
):
  st.markdown("""
    ---
    ### 💻 **On Laptops & Desktops (Windows / Mac)**
    * **Chrome & Edge:** Click the **Install Icon** `[+]` in your browser address bar at the top right and click **Install**.
    * **Mac (Safari):** Click **File** in the top Mac menu bar > Select **Add to Dock**.
    
    ---
    ### 📱 **On Smartphones & Tablets**
    * **iPhone / iPad (Safari):** Tap the **Share** button (box with arrow) > Tap **Add to Home Screen**.
    * **Android (Chrome):** Tap the **3-Dots on your browser (eg, Chrome), not the dashboard 3-Dots** > Tap **Install and create shortcut**.
    
    *Result: Opens instantly like a native mobile/desktop app without browser tabs!*
    """)

# Retrieve Gemini API Key from Streamlit Secrets or manual fallback
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
  with st.sidebar:
    st.warning("⚠️ Secret API key missing. Enter temporary key below:")
    api_key = st.text_input("Gemini API Key", type="password")

st.markdown("---")

tab1, tab2 = st.tabs(
    ["🎥 New Product Script & Captions", "📩 Brand PR Pitch Generator"]
)

# -------------------------------------------------------------------
# TAB 1: PRODUCT LAUNCH & CAPTIONS
# -------------------------------------------------------------------
with tab1:
  st.subheader("📦 Enter Product Launch Brief")

  col1, col2 = st.columns(2)
  with col1:
    prod_name = st.text_input(
        "Product Name & Brand",
        placeholder="e.g. Plum Rice Water & Niacinamide Serum",
    )
    skin_target = st.text_input(
        "Target Skin Type / Tone",
        placeholder="e.g. Dull, textured skin / All skin types",
    )
    vibe = st.selectbox(
        "Reel Style",
        [
            "Problem-Solution Reel",
            "Unboxing & First Impressions",
            "GRWM Routine",
            "Deep Dive Review",
        ],
    )

  with col2:
    uvp = st.text_input(
        "Key USP / What makes it unique?",
        placeholder="e.g. Brightens skin, fades dark spots, 100% vegan",
    )
    key_ingredients = st.text_input(
        "Key Ingredients & Claims",
        placeholder="e.g. 10% Niacinamide, Japanese Rice Water",
    )

  pr_brief = st.text_area(
      "📄 Paste PR Launch Document / Brand Guidelines (Optional)",
      placeholder=(
          "Paste full product details, launch rules, mandatory disclosures, or"
          " website text..."
      ),
      height=100,
  )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("🚀 Generate Viral Reel Script & SEO Captions"):
    if not api_key:
      st.error("Please provide a Gemini API Key to continue.")
    elif not prod_name:
      st.warning("Please enter at least the product name.")
    else:
      client = genai.Client(api_key=api_key)
      prompt = f"""
            You are a top social media strategist for luxury beauty influencers on Instagram.
            
            ### PRODUCT BRIEF:
            - Product Name: {prod_name}
            - Target Skin Type: {skin_target}
            - Reel Style: {vibe}
            - Key USP: {uvp}
            - Key Ingredients/Claims: {key_ingredients}
            - Additional Context: {pr_brief if pr_brief else 'None provided.'}

            ### GENERATE THE FOLLOWING IN CLEAN, HIGH-END MARKDOWN FORMAT:

            1. 🎬 **3 VIRAL HOOK OPTIONS (0-3 SECONDS)**
               - High-converting visual/spoken hooks designed to stop the scroll instantly.

            2. 🎥 **FULL 30-SECOND REEL SCRIPT**
               - Line-by-line breakdown with **Visual Action Cue** and **Voiceover Line**.
               - Emphasize texture showing, application, and core USP ({uvp}).

            3. 📝 **HIGH-CONVERTING INSTAGRAM CAPTION**
               - Aesthetic, engaging caption formatted with clean line breaks and emojis.
               - Includes hook, benefits, step-by-step skin application, and a strong CTA.

            4. 🏷️ **30 STRATEGIC INSTAGRAM HASHTAGS**
               - Grouped cleanly into Niche Skincare, Product Type, Skin Concerns, and Indian Beauty Trends.

            5. ⚖️ **ASCI / FTC DISCLOSURE STATEMENT**
               - Ready-to-copy standard disclaimer tag for sponsored/PR content in India.
            """

      with st.spinner("✨ Crafting high-converting creator campaign..."):
        try:
          res_text = generate_ai_response(client, prompt)
          st.success("🎉 Campaign Generated Successfully!")
          st.markdown("---")
          st.markdown(res_text)
        except Exception as e:
          st.error(
              "⚠️ Google's AI servers are currently experiencing high demand"
              " (503 Unavailable)."
          )
          if st.button("🔄 Click to Retry Generation"):
            st.rerun()

# -------------------------------------------------------------------
# TAB 2: BRAND PR PITCH
# -------------------------------------------------------------------
with tab2:
  st.subheader("✉️ Pitch Cosmetic Brands for PR Packages")

  col_a, col_b = st.columns(2)
  with col_a:
    creator_name = st.text_input(
        "Your Creator Name / IG Handle", placeholder="e.g. @glowwithananya"
    )
    niche = st.text_input(
        "Your Niche & Follower Count",
        placeholder="e.g. Skincare for Acne-Prone Skin, 15k Followers",
    )
  with col_b:
    target_brand = st.text_input(
        "Target Brand Name", placeholder="e.g. Minimalist, Plum, Nykaa, Dot & Key"
    )
    collab_type = st.selectbox(
        "Pitch Objective",
        [
            "PR Gifting Package",
            "Paid Brand Partnership",
            "Long-term Ambassadorship",
        ],
    )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("✨ Draft High-Converting PR Pitch"):
    if not api_key:
      st.error("Please provide a Gemini API Key.")
    elif not creator_name or not target_brand:
      st.warning("Please fill in your creator name and target brand.")
    else:
      client = genai.Client(api_key=api_key)
      prompt = f"""
            Write a professional, persuasive PR outreach email and Instagram DM from beauty creator '{creator_name}' ({niche}) pitching to '{target_brand}' for a '{collab_type}'.
            Make it high-converting, professional, value-driven, and tailored to beauty brand PR managers.
            """
      with st.spinner("✨ Drafting professional brand pitch..."):
        try:
          res_text = generate_ai_response(client, prompt)
          st.success("🎉 PR Pitch Drafted Successfully!")
          st.markdown("---")
          st.markdown(res_text)
        except Exception as e:
          st.error(
              "⚠️ Google's AI servers are currently experiencing high demand"
              " (503 Unavailable)."
          )
          if st.button("🔄 Click to Retry Pitch Generation"):
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>MagaSum"
    " Beauty Creator Suite &bull; Empowering Creators Worldwide</div>",
    unsafe_allow_html=True,
)