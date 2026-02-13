"""
Cloak Buster Link Builder
A Streamlit tool to generate realistic Google Ads URLs for testing cloaking filters.
"""

import streamlit as st
import random
import string
from urllib.parse import urlencode, urlparse, urlunparse

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

BASE64_CHARS = string.ascii_letters + string.digits + "-_"


def generate_gclid() -> str:
    prefix = "Cj0KCQi"
    suffix = "".join(random.choices(BASE64_CHARS, k=random.randint(80, 100)))
    return prefix + suffix


def generate_wbraid() -> str:
    prefix = "CjwKCAjw"
    suffix = "".join(random.choices(BASE64_CHARS, k=random.randint(30, 50)))
    return prefix + suffix


def generate_gbraid() -> str:
    prefix = "CjwKCAjw"
    suffix = "".join(random.choices(BASE64_CHARS, k=random.randint(30, 50)))
    return prefix + suffix


def generate_campid() -> str:
    return "".join(random.choices(string.digits, k=10))


def build_url(base_url: str, params: dict) -> str:
    filtered_params = {k: v for k, v in params.items() if v}
    if not filtered_params:
        return base_url
    parsed = urlparse(base_url)
    query_string = urlencode(filtered_params)
    if parsed.query:
        query_string = parsed.query + "&" + query_string
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, query_string, parsed.fragment))


def generate_js_injection(url: str) -> str:
    return f'''document.body.innerHTML = '<a href="{url}" style="font-size:50px;display:block;margin-top:200px;text-align:center;color:blue;text-decoration:underline;">CLICK HERE</a>';'''


# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    defaults = {
        "base_url": "https://google.com",
        "add_gclid": True,  # Default ON
        "add_wbraid": False,
        "add_gbraid": False,
        "add_gad_source": True,  # Default ON
        "campid": generate_campid(),
        "keyword": "",
        "placement": "",
        "gclid_value": generate_gclid(),
        "wbraid_value": generate_wbraid(),
        "gbraid_value": generate_gbraid(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def regenerate_hashes():
    st.session_state.gclid_value = generate_gclid()
    st.session_state.wbraid_value = generate_wbraid()
    st.session_state.gbraid_value = generate_gbraid()
    st.rerun()


def build_current_url() -> str:
    params = {}
    if st.session_state.add_gclid:
        params["gclid"] = st.session_state.gclid_value
    if st.session_state.add_wbraid:
        params["wbraid"] = st.session_state.wbraid_value
    if st.session_state.add_gbraid:
        params["gbraid"] = st.session_state.gbraid_value
    if st.session_state.add_gad_source:
        params["gad_source"] = "1"
    if st.session_state.campid:
        params["campid"] = st.session_state.campid
    if st.session_state.keyword:
        params["keyword"] = st.session_state.keyword
    if st.session_state.placement:
        params["placement"] = st.session_state.placement
    return build_url(st.session_state.base_url, params)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(page_title="Cloak Buster", page_icon="🔗", layout="centered")
    init_session_state()
    
    st.markdown("<h2 style='margin-bottom:0'>🔗 Cloak Buster Link Builder</h2>", unsafe_allow_html=True)
    
    # Base URL
    st.text_input("Base URL", value=st.session_state.base_url, key="base_url", label_visibility="collapsed", placeholder="https://example.com")
    
    # Toggles - compact 4 columns
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.checkbox("gclid", value=st.session_state.add_gclid, key="add_gclid")
    with c2:
        st.checkbox("wbraid", value=st.session_state.add_wbraid, key="add_wbraid")
    with c3:
        st.checkbox("gbraid", value=st.session_state.add_gbraid, key="add_gbraid")
    with c4:
        st.checkbox("gad_source", value=st.session_state.add_gad_source, key="add_gad_source")
    
    # Custom params - compact 3 columns
    p1, p2, p3 = st.columns(3)
    with p1:
        st.text_input("campid", value=st.session_state.campid, key="campid")
    with p2:
        st.text_input("keyword", value=st.session_state.keyword, key="keyword")
    with p3:
        st.text_input("placement", value=st.session_state.placement, key="placement")
    
    # Buttons - same row
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("🔄 Generate New Hashes", use_container_width=True):
            regenerate_hashes()
    with btn2:
        if st.button("🗑️ Reset All", type="secondary", use_container_width=True):
            reset_all()
    
    # Auto-generate URL
    final_url = build_current_url()
    js_code = generate_js_injection(final_url)
    
    # Output
    st.code(final_url, language="text")
    st.code(js_code, language="javascript")


if __name__ == "__main__":
    main()
