import streamlit as st
import requests

st.set_page_config(page_title="Medicine Info Lookup", page_icon="💊", layout="centered")

st.title("💊 Medicine Information Lookup")
st.write(
    "Type the name of a medicine (brand or generic) to see what it's for, "
    "how to take it, and common side effects."
)

medicine_name = st.text_input(
    "Medicine name", placeholder="e.g., Advil, Ibuprofen, Tylenol, Amoxicillin"
)
search_clicked = st.button("Search", type="primary")


@st.cache_data(show_spinner=False)
def fetch_medicine_info(name: str):
    """Query the OpenFDA drug label API for a given medicine name."""
    url = "https://api.fda.gov/drug/label.json"
    # Try brand name, then generic name, then active substance
    queries = [
        f'openfda.brand_name:"{name}"',
        f'openfda.generic_name:"{name}"',
        f'openfda.substance_name:"{name}"',
    ]
    for q in queries:
        params = {"search": q, "limit": 1}
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results"):
                    return data["results"][0]
        except requests.RequestException:
            continue
    return None


def get_field(result, field):
    """OpenFDA fields are usually lists of strings — grab the first one."""
    val = result.get(field)
    if isinstance(val, list) and val:
        return val[0]
    return None


if search_clicked or medicine_name:
    if not medicine_name.strip():
        st.warning("Please enter a medicine name.")
    else:
        with st.spinner("Looking up medicine information..."):
            result = fetch_medicine_info(medicine_name.strip())

        if not result:
            st.error(
                f"No information found for '{medicine_name}'. "
                "Try the generic name, or double-check the spelling."
            )
        else:
            openfda = result.get("openfda", {})
            brand = openfda.get("brand_name", [medicine_name])[0]
            generic = openfda.get("generic_name", [""])[0]

            title = brand
            if generic and generic.lower() != brand.lower():
                title += f" ({generic})"
            st.subheader(title)

            purpose = get_field(result, "purpose") or get_field(
                result, "indications_and_usage"
            )
            if purpose:
                st.markdown("### 🩺 What it is / what it's for")
                st.write(purpose)

            dosage = get_field(result, "dosage_and_administration")
            if dosage:
                st.markdown("### 📋 How to take it")
                st.write(dosage)

            adverse = get_field(result, "adverse_reactions")
            if adverse:
                st.markdown("### ⚠️ Common side effects")
                st.write(adverse)

            warnings = get_field(result, "warnings") or get_field(
                result, "warnings_and_cautions"
            )
            if warnings:
                st.markdown("### 🚫 Warnings")
                st.write(warnings)

            stop_use = get_field(result, "stop_use")
            if stop_use:
                st.markdown("### 🛑 When to stop use / seek medical help")
                st.write(stop_use)

            if not any([purpose, dosage, adverse, warnings, stop_use]):
                st.info("Found a record, but it didn't contain detailed label text.")

st.divider()
st.caption(
    "⚠️ This tool pulls general information from FDA drug labeling data and is "
    "**not a substitute for professional medical advice**. Always check with a "
    "doctor or pharmacist about your specific medication and situation."
)
