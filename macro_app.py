import streamlit as st
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="💪 Macro & Calorie Calculator", page_icon="🔥", layout="centered")

# تنسيق CSS بسيط
st.markdown("""
    <style>
        body {background-color: #f8f9fa;}
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }
        h1 {text-align: center; color: #2c3e50;}
        .stButton>button {
            background-color: #2ecc71;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 24px;
            transition: 0.3s;
        }
        .stButton>button:hover {background-color: #27ae60;}
    </style>
""", unsafe_allow_html=True)

# العنوان
st.title("🔥 Total Daily Energy & Macro Calculator")
st.write("احسب سعراتك واحتياجك من البروتين، الدهون، والكارب بناءً على بياناتك وهدفك 🎯")

# إدخال البيانات
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("🚻 النوع:", ["ذكر", "أنثى"])
    age = st.number_input("🎂 العمر:", min_value=10, max_value=100, step=1)
    height = st.number_input("📏 الطول (سم):", min_value=100.0, max_value=250.0, step=0.1)
with col2:
    weight = st.number_input("🏋️‍♂️ الوزن (كجم):", min_value=30.0, max_value=200.0, step=0.1)
    activity = st.selectbox("🏃‍♂️ مستوى النشاط:", [
        "قليل جدًا (بدون تمارين)",
        "خفيف (تمارين 1-3 أيام/أسبوع)",
        "متوسط (تمارين 3-5 أيام/أسبوع)",
        "عالي (تمارين 6-7 أيام/أسبوع)",
        "عنيف جدًا (نشاط يومي + عمل مجهد)"
    ])
    goal = st.selectbox("🎯 الهدف:", ["ضخامة (Bulking)", "ثبات (Maintenance)", "تنشيف (Cutting)"])

# حساب الـ BMR (معدل الأيض الأساسي)
if gender == "ذكر":
    BMR = 10 * weight + 6.25 * height - 5 * age + 5
else:
    BMR = 10 * weight + 6.25 * height - 5 * age - 161

# مضاعف النشاط
activity_factors = {
    "قليل جدًا (بدون تمارين)": 1.2,
    "خفيف (تمارين 1-3 أيام/أسبوع)": 1.375,
    "متوسط (تمارين 3-5 أيام/أسبوع)": 1.55,
    "عالي (تمارين 6-7 أيام/أسبوع)": 1.725,
    "عنيف جدًا (نشاط يومي + عمل مجهد)": 1.9
}
TDEE = BMR * activity_factors[activity]

# تعديل الهدف
if goal == "ضخامة (Bulking)":
    calories = TDEE + 300
    protein_factor = 1.6
    fat_ratio = 0.25
elif goal == "ثبات (Maintenance)":
    calories = TDEE
    protein_factor = 1.8
    fat_ratio = 0.3
else:  # تنشيف
    calories = TDEE - 300
    protein_factor = 2.0
    fat_ratio = 0.25

# زر الحساب
if st.button("احسب النتائج 💥"):
    # حساب الماكروز
    protein_g = weight * protein_factor
    fat_g = (calories * fat_ratio) / 9
    carbs_g = (calories - (protein_g * 4 + fat_g * 9)) / 4

    protein_cal = protein_g * 4
    fat_cal = fat_g * 9
    carbs_cal = carbs_g * 4

    # عرض النتائج
    st.markdown("## 🧮 النتائج:")
    st.success(f"**السعرات اليومية:** {calories:.0f} kcal")
    st.info(f"**Protein:** {protein_g:.1f} g ({protein_cal:.0f} kcal)")
    st.warning(f"**Fat:** {fat_g:.1f} g ({fat_cal:.0f} kcal)")
    st.write(f"**Carbs:** {carbs_g:.1f} g ({carbs_cal:.0f} kcal)")

    st.write(f"📊 *نسبة الماكروز:* بروتين {protein_cal/calories*100:.1f}% | دهون {fat_cal/calories*100:.1f}% | كارب {carbs_cal/calories*100:.1f}%")

    # رسم بياني دائري
    labels = ['Protein', 'Fat', 'Carbs']
    values = [protein_cal, fat_cal, carbs_cal]
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title("🔸 توزيع السعرات بين الماكروز")
    st.pyplot(fig)

    # إنشاء صورة نصية للتحميل
    img = Image.new('RGB', (650, 420), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((50, 40), f"Goal: {goal}", fill=(0, 0, 0))
    d.text((50, 70), f"Weight: {weight} kg", fill=(0, 0, 0))
    d.text((50, 100), f"Calories: {calories:.0f} kcal", fill=(0, 0, 0))
    d.text((50, 130), f"Protein: {protein_g:.1f} g", fill=(0, 0, 0))
    d.text((50, 160), f"Fat: {fat_g:.1f} g", fill=(0, 0, 0))
    d.text((50, 190), f"Carbs: {carbs_g:.1f} g", fill=(0, 0, 0))
    img_file = "Macro_Results.jpg"
    img.save(img_file)

    st.image(img, caption="📋 نتائجك في صورة جاهزة")
    with open(img_file, "rb") as file:
        st.download_button("📥 تحميل الصورة", data=file, file_name="Macro_Results.jpg", mime="image/jpeg")
