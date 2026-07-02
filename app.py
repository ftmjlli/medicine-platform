import streamlit as st

st.set_page_config(page_title="BMI Buddy 🎉", page_icon="⚖️", layout="centered")

# ---------- FUN, COLORFUL STYLING ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #FFEEAD 0%, #FFCC99 50%, #FF9AA2 100%);
}
h1 {
    text-align: center;
    font-size: 44px !important;
    text-shadow: 2px 2px 0px #fff;
}
.result-card {
    background: white;
    border-radius: 25px;
    padding: 30px;
    text-align: center;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
    margin-top: 20px;
    margin-bottom: 20px;
}
.big-emoji { font-size: 80px; }
.bmi-number { font-size: 50px; font-weight: bold; }
.stButton>button {
    background: linear-gradient(90deg, #FF6B6B, #FFD93D);
    color: white;
    font-size: 22px;
    font-weight: bold;
    border-radius: 15px;
    padding: 12px 30px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("⚖️ BMI Buddy 🎉")
st.markdown(
    "<p style='text-align:center; font-size:20px;'>Let's find your BMI and get some fun, "
    "easy tips to feel your best! 💪🥗</p>",
    unsafe_allow_html=True
)

# ---------- UNIT TOGGLES ----------
col1, col2 = st.columns(2)
with col1:
    weight_unit = st.radio("Weight unit", ["kg", "lb"], horizontal=True)
with col2:
    height_unit = st.radio("Height unit", ["cm", "ft/in"], horizontal=True)

st.markdown("### 🧍 Tell us about you")

weight = st.number_input(f"Your weight ({weight_unit})", min_value=1.0, max_value=500.0, value=70.0 if weight_unit == "kg" else 154.0, step=0.5)

if height_unit == "cm":
    height = st.number_input("Your height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
else:
    col_ft, col_in = st.columns(2)
    with col_ft:
        feet = st.number_input("Feet", min_value=1, max_value=8, value=5, step=1)
    with col_in:
        inches = st.number_input("Inches", min_value=0, max_value=11, value=7, step=1)

calculate = st.button("🎯 Calculate My BMI!")

# ---------- BMI DATA: category info, stickers, tips ----------
BMI_INFO = {
    "underweight": {
        "range": "Below 18.5",
        "emoji": "🐥",
        "sticker": "🍕🥑🥜",
        "title": "Little Featherweight!",
        "caption": "You're light as a feather! Let's add some healthy fuel. 🐥",
        "color": "#74B9FF",
        "diet": [
            "🥑 Add healthy fats: avocado, nuts, olive oil",
            "🍚 Eat more whole grains like rice, oats, bread",
            "🥛 Add a glass of milk or a smoothie between meals",
            "🍗 Include protein at every meal: eggs, chicken, beans",
            "🍽️ Eat smaller meals more often (5-6 times a day)",
        ],
        "exercise": [
            "🏋️ Light strength training 2-3x a week to build muscle",
            "🧘 Yoga or stretching to stay flexible",
            "🚶 Gentle walks — no need to overdo cardio",
            "😴 Prioritize good sleep for muscle recovery",
        ],
    },
    "normal": {
        "range": "18.5 - 24.9",
        "emoji": "🌟",
        "sticker": "🥗🏃🎉",
        "title": "Balanced Superstar!",
        "caption": "You're right in the healthy zone — amazing job! 🌟",
        "color": "#55EFC4",
        "diet": [
            "🥗 Keep enjoying a colorful mix of fruits and veggies",
            "💧 Stay hydrated — aim for 8 glasses of water a day",
            "🍎 Snack smart: fruit, nuts, yogurt",
            "🍽️ Keep portions balanced and varied",
        ],
        "exercise": [
            "🏃 30 minutes of activity most days keeps you thriving",
            "🚴 Mix it up: walking, cycling, dancing, swimming",
            "🏋️ Add light strength training twice a week",
            "🧘 Don't forget to stretch and rest too!",
        ],
    },
    "overweight": {
        "range": "25 - 29.9",
        "emoji": "🐻",
        "sticker": "🥦🚶🍎",
        "title": "Cozy Bear Mode!",
        "caption": "A few small tweaks and you'll feel lighter and stronger! 🐻",
        "color": "#FFEAA7",
        "diet": [
            "🥦 Fill half your plate with veggies at every meal",
            "🍭 Cut back on sugary drinks and snacks",
            "🍽️ Try smaller plates to naturally reduce portions",
            "🥩 Choose lean proteins: chicken, fish, tofu, beans",
            "🍞 Swap white bread/rice for whole grain versions",
        ],
        "exercise": [
            "🚶 Start with a brisk 20-30 minute walk daily",
            "🪜 Take the stairs instead of the elevator",
            "🚴 Try cycling or swimming — easy on the joints",
            "🏋️ Add light strength training 2x a week",
        ],
    },
    "obese": {
        "range": "30 and above",
        "emoji": "🐘",
        "sticker": "🥕💪🌿",
        "title": "Gentle Giant Journey!",
        "caption": "Every step counts — let's build healthy habits together! 🐘",
        "color": "#FF7675",
        "diet": [
            "🥕 Focus on whole foods: vegetables, fruits, lean protein",
            "🚫 Reduce fried and processed foods gradually",
            "💧 Drink water instead of soda or juice",
            "🍽️ Eat slowly and stop when comfortably full",
            "👩‍⚕️ A dietitian can build a plan tailored just for you",
        ],
        "exercise": [
            "🚶 Start small: 10-15 minute walks, build up slowly",
            "🏊 Swimming is gentle and great for joints",
            "🪑 Try chair exercises or gentle stretching to start",
            "👨‍⚕️ Check with a doctor before starting new workouts",
        ],
    },
}


def get_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"


if calculate:
    # Convert to metric
    weight_kg = weight if weight_unit == "kg" else weight * 0.453592
    if height_unit == "cm":
        height_m = height / 100
    else:
        total_inches = feet * 12 + inches
        height_m = total_inches * 0.0254

    if height_m <= 0:
        st.error("Please enter a valid height 📏")
    else:
        bmi = weight_kg / (height_m ** 2)
        category = get_category(bmi)
        info = BMI_INFO[category]

        # Fun celebration effect
        if category == "normal":
            st.balloons()
        else:
            st.snow()

        st.markdown(f"""
        <div class="result-card" style="border: 4px solid {info['color']};">
            <div class="big-emoji">{info['emoji']}</div>
            <h2>{info['title']}</h2>
            <div class="bmi-number" style="color:{info['color']};">{bmi:.1f}</div>
            <p style="font-size:18px;">{info['caption']}</p>
            <p style="font-size:30px;">{info['sticker']}</p>
            <p style="font-size:14px; color:gray;">Category range: {info['range']}</p>
        </div>
        """, unsafe_allow_html=True)

        # BMI scale visual
        st.markdown("### 📊 Where you stand on the scale")
        st.progress(min(bmi / 40, 1.0))
        st.caption("Scale: 0 ————————————— 40+ BMI")

        col_diet, col_ex = st.columns(2)
        with col_diet:
            st.markdown("### 🥗 Easy Diet Tips")
            for tip in info["diet"]:
                st.markdown(f"- {tip}")
        with col_ex:
            st.markdown("### 🏃 Easy Exercise Tips")
            for tip in info["exercise"]:
                st.markdown(f"- {tip}")

        st.divider()
        st.caption(
            "⚠️ BMI is a simple screening tool and doesn't account for muscle mass, age, or body "
            "composition. It's not a diagnosis. For personalized advice, please talk to a doctor "
            "or dietitian. 💛"
        )
