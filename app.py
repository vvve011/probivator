"""
Cloak Buster Link Builder
A Streamlit tool to generate realistic Google Ads URLs for testing cloaking filters.
"""

import streamlit as st
import random
import string
from urllib.parse import urlencode, urlparse, urlunparse

# ============================================================================
# HELPER FUNCTIONS - Realistic Hash Generation
# ============================================================================

BASE64_CHARS = string.ascii_letters + string.digits + "-_"


def generate_gclid() -> str:
    """
    Generate realistic Google Click ID.
    Format: Cj0KCQi + 80-100 random base64-like characters
    """
    prefix = "Cj0KCQi"
    suffix_length = random.randint(80, 100)
    suffix = "".join(random.choices(BASE64_CHARS, k=suffix_length))
    return prefix + suffix


def generate_wbraid() -> str:
    """
    Generate realistic iOS Web attribution parameter.
    Format: CjwKCAjw + 30-50 random base64-like characters
    """
    prefix = "CjwKCAjw"
    suffix_length = random.randint(30, 50)
    suffix = "".join(random.choices(BASE64_CHARS, k=suffix_length))
    return prefix + suffix


def generate_gbraid() -> str:
    """
    Generate realistic iOS App attribution parameter.
    Format: CjwKCAjw + 30-50 random base64-like characters
    """
    prefix = "CjwKCAjw"
    suffix_length = random.randint(30, 50)
    suffix = "".join(random.choices(BASE64_CHARS, k=suffix_length))
    return prefix + suffix


def generate_campid() -> str:
    """Generate random 10-digit campaign ID."""
    return "".join(random.choices(string.digits, k=10))


def build_url(base_url: str, params: dict) -> str:
    """Build the final URL with query parameters."""
    # Filter out empty values
    filtered_params = {k: v for k, v in params.items() if v}
    
    if not filtered_params:
        return base_url
    
    # Parse base URL and append params
    parsed = urlparse(base_url)
    query_string = urlencode(filtered_params)
    
    # Handle existing query params
    if parsed.query:
        query_string = parsed.query + "&" + query_string
    
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        query_string,
        parsed.fragment
    ))


def generate_js_injection(url: str) -> str:
    """Generate the JavaScript injection code."""
    return f'''document.body.innerHTML = '<a href="{url}" style="font-size:50px;display:block;margin-top:200px;text-align:center;color:blue;text-decoration:underline;">CLICK HERE</a>';'''


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables with defaults."""
    defaults = {
        "base_url": "https://google.com",
        "add_gclid": False,
        "add_wbraid": False,
        "add_gbraid": False,
        "add_gad_source": False,
        "campid": generate_campid(),
        "keyword": "",
        "placement": "",
        "gclid_value": generate_gclid(),
        "wbraid_value": generate_wbraid(),
        "gbraid_value": generate_gbraid(),
        "generated_url": "",
        "generated_js": "",
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_all():
    """Clear all session state and reset to defaults."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def regenerate_hashes():
    """Regenerate all hash values."""
    st.session_state.gclid_value = generate_gclid()
    st.session_state.wbraid_value = generate_wbraid()
    st.session_state.gbraid_value = generate_gbraid()


def generate_link():
    """Build the final URL and JS code based on current settings."""
    # Regenerate hashes on each generate
    regenerate_hashes()
    
    params = {}
    
    # Add Google Ads parameters if enabled
    if st.session_state.add_gclid:
        params["gclid"] = st.session_state.gclid_value
    
    if st.session_state.add_wbraid:
        params["wbraid"] = st.session_state.wbraid_value
    
    if st.session_state.add_gbraid:
        params["gbraid"] = st.session_state.gbraid_value
    
    if st.session_state.add_gad_source:
        params["gad_source"] = "1"
    
    # Add custom parameters
    if st.session_state.campid:
        params["campid"] = st.session_state.campid
    
    if st.session_state.keyword:
        params["keyword"] = st.session_state.keyword
    
    if st.session_state.placement:
        params["placement"] = st.session_state.placement
    
    # Build URL
    final_url = build_url(st.session_state.base_url, params)
    st.session_state.generated_url = final_url
    st.session_state.generated_js = generate_js_injection(final_url)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="Cloak Buster Link Builder",
        page_icon="🔗",
        layout="centered"
    )
    
    # Initialize session state
    init_session_state()
    
    # ========== HEADER ==========
    st.title("🔗 Cloak Buster Link Builder")
    st.markdown("Generate realistic Google Ads URLs for testing cloaking filters.")
    
    # Red RESET ALL button
    st.markdown("""
        <style>
        div.stButton > button[kind="secondary"]:first-child {
            background-color: #ff4b4b;
            color: white;
            border: none;
        }
        div.stButton > button[kind="secondary"]:first-child:hover {
            background-color: #ff3333;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col_reset, col_spacer = st.columns([1, 4])
    with col_reset:
        if st.button("🗑️ RESET ALL", type="secondary", use_container_width=True):
            reset_all()
    
    st.divider()
    
    # ========== INPUT SECTION ==========
    st.subheader("📝 Configuration")
    
    # Base URL
    st.session_state.base_url = st.text_input(
        "Base URL",
        value=st.session_state.base_url,
        placeholder="https://example.com"
    )
    
    # Parameter Toggles
    st.markdown("**Google Ads Parameters:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.add_gclid = st.checkbox(
            "Add gclid (Google Click ID)",
            value=st.session_state.add_gclid
        )
        st.session_state.add_wbraid = st.checkbox(
            "Add wbraid (iOS Web)",
            value=st.session_state.add_wbraid
        )
    
    with col2:
        st.session_state.add_gbraid = st.checkbox(
            "Add gbraid (iOS App)",
            value=st.session_state.add_gbraid
        )
        st.session_state.add_gad_source = st.checkbox(
            "Add gad_source (Fixed: 1)",
            value=st.session_state.add_gad_source
        )
    
    # UTM / Custom Parameters
    st.markdown("**Custom Parameters:**")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.session_state.campid = st.text_input(
            "campid",
            value=st.session_state.campid,
            placeholder="Campaign ID"
        )
    
    with col4:
        st.session_state.keyword = st.text_input(
            "keyword",
            value=st.session_state.keyword,
            placeholder="Target keyword"
        )
    
    with col5:
        st.session_state.placement = st.text_input(
            "placement",
            value=st.session_state.placement,
            placeholder="Placement"
        )
    
    st.divider()
    
    # ========== GENERATE BUTTONS ==========
    col_gen1, col_gen2 = st.columns(2)
    
    with col_gen1:
        if st.button("🚀 Generate Link", type="primary", use_container_width=True):
            generate_link()
    
    with col_gen2:
        if st.button("🔄 Generate New Hashes Only", use_container_width=True):
            regenerate_hashes()
            if st.session_state.generated_url:
                generate_link()
    
    # ========== OUTPUT SECTION ==========
    if st.session_state.generated_url:
        st.divider()
        st.subheader("📤 Output")
        
        # Final URL
        st.markdown("**Final URL:**")
        st.code(st.session_state.generated_url, language="text")
        
        # JS Injection Code
        st.markdown("**JS Injection Code:**")
        st.code(st.session_state.generated_js, language="javascript")
        
        # Hash details (collapsible)
        with st.expander("🔍 View Generated Hashes"):
            if st.session_state.add_gclid:
                st.text(f"gclid: {st.session_state.gclid_value}")
            if st.session_state.add_wbraid:
                st.text(f"wbraid: {st.session_state.wbraid_value}")
            if st.session_state.add_gbraid:
                st.text(f"gbraid: {st.session_state.gbraid_value}")


if __name__ == "__main__":
    main()
