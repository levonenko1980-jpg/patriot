import streamlit as st
import os
import base64
from data import documents # Импортируем нашу полную базу данных

# 1. Настройка страницы
st.set_page_config(page_title="Партизанская летопись Гомельщины", page_icon="📖", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

current_folder = os.path.dirname(__file__) if __file__ else os.getcwd()

bg_file = os.path.join(current_folder, "background.jpg")
if os.path.exists(bg_file):
    bin_str = get_base64_of_bin_file(bg_file)
    st.markdown(f'<style>.stApp {{background-image: linear-gradient(rgba(255,255,255,0.15), rgba(255,255,255,0.15)), url("data:image/jpg;base64,{bin_str}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;}}</style>', unsafe_allow_html=True)

st.markdown('<style>html, body, [data-testid="stWidgetLabel"], .stMarkdown p, h1, h2, h3, h4, h5 {font-family: "Segoe UI", sans-serif !important;}</style>', unsafe_allow_html=True)

left_logo_path = os.path.join(current_folder, "left_logo.png")
logo_path = os.path.join(current_folder, "logo.png")
left_img_html, right_img_html = "", ""

if os.path.exists(left_logo_path):
    left_img_html = f'<img src="data:image/png;base64,{get_base64_of_bin_file(left_logo_path)}" style="height: 120px; margin-right: 25px; margin-top: 10px;">'
if os.path.exists(logo_path):
    right_img_html = f'<img src="data:image/png;base64,{get_base64_of_bin_file(logo_path)}" style="height: 120px; margin-left: 25px; margin-top: 10px;">'

st.markdown(f'<div style="display: flex; align-items: center; justify-content: center; width: 100%; margin-bottom: 20px; text-align: center;">{left_img_html}<div><h2 style="margin: 0; padding: 0; line-height: 1.15em; font-size: 2.1em; color: #111;">ИИ-платформа «Партизанская летопись Гомельщины»</h2><h5 style="margin: 5px 0 0 0; padding: 0; color: #333;">Проект для республиканского конкурса «ПАТРИОТ.by»</h5></div>{right_img_html}</div>', unsafe_allow_html=True)

st.markdown("""<div style="background-color: rgba(255, 255, 255, 0.95); padding: 12px 20px; border-radius: 6px; border-left: 5px solid #43A047; color: #222; margin-bottom: 15px; font-size: 0.95em; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><b>Учреждение образования:</b> ГУО "Средняя школа №1 г.п. Корма" &nbsp;|&nbsp; <b>Разработчик:</b> учащийся 10 "А" класса Дроздов Денис Александрович &nbsp;|&nbsp; <b>Руководитель:</b> Левоненко Татьяна Александровна, учитель информатики</div>""", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.header("💬 Вопрос к экскурсоводу")
    user_query = st.text_input("Введите тему для анализа архива историко-культурного наследия края:", placeholder="Например: Кожар, Бородин, Газета, Корма, Лоев, Жлобин...")
    
    # Флаг, который определяет, был ли найден хоть один документ
    has_answer = False
    
    if user_query:
        query_part = user_query.lower()[:4]
        found = False
        
        # Временно выводим заголовок ответа
        st.success("🎙️ Ответ экскурсовода:")
        for doc in documents:
            if query_part in doc["title"].lower() or query_part in doc["text"].lower():
                with st.chat_message("assistant", avatar="📖"):
                    st.markdown(f"**{doc['title']} ({doc['date']})**")
                    st.write(doc["text"])
                    if doc["image_name"]:
                        img_path = os.path.join(current_folder, doc["image_name"])
                        if os.path.exists(img_path):
                            st.image(img_path, caption=f"Архивный снимок: {doc['title']}")
                found = True
                has_answer = True # Фиксируем, что ответ на экране есть
                
        if not found:
            st.warning("В архиве нет совпадений. Попробуйте слова: Кожар, Бородин, Газета, Корма, Лоев, Жлобин.")
            has_answer = True # Даже если совпадений нет, предупреждение на экране, карту скрываем
            
    # КАРТА ОТОБРАЖАЕТСЯ ТОЛЬКО ЕСЛИ НЕТ ОТВЕТА ЭКСКУРСОВОДА
    if not has_answer:
        # Добавляем пустые отступы, чтобы изначально опустить карту пониже
        st.write("")
        st.write("")
        st.write("")
        st.markdown("##### 📍 Картографический анализ партизанских соединений БССР:")
        map_path = os.path.join(current_folder, "map.png")
        if os.path.exists(map_path):
            st.image(map_path, caption="Карта: Партизанские бригады и соединения на оккупированной территории Беларуси (1942—1944 гг.)")
        else:
            st.warning("Файл карты 'map.png' не найден в папке проекта. Пожалуйста, проверьте имя файла.")

with col2:
    st.header("⏳ Лента времени")
    for item in sorted(documents, key=lambda x: x['date']):
        st.markdown(f'<div style="background-color: rgba(255, 255, 255, 0.95); padding: 15px 20px; border-radius: 8px; border-left: 6px solid #43A047; box-shadow: 0 3px 5px rgba(0,0,0,0.05); margin-bottom: 15px;"><span style="background: linear-gradient(90deg, #C8102E 50%, #43A047 50%); color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.85em; font-weight: bold; display: inline-block; margin-bottom: 5px;">{item["date"]}</span><h3 style="margin: 5px 0; color: #111; font-family: \'Georgia\', serif; font-weight: bold;">{item["title"]}</h3><p style="color: #333; font-size: 0.95em; line-height: 1.45em; margin: 0;">{item["text"]}</p></div>', unsafe_allow_html=True)

st.write("")
st.divider()
st.subheader("🔗 Электронные информационные ресурсы проекта:")
st.markdown("В основу нашей платформы легли подлинные материалы совместного интернет-проекта **Белорусского телеграфного агентства (БЕЛТА)** и **Белорусского государственного музея истории Великой Отечественной войны**, а также данные регионального исследования **«Партизанское движение на территории Гомельщины»**.")

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    st.link_button("Проект «Партизанская летопись» (БЕЛТА) ↗️", "https://belta.by")
with btn_col2:
    st.link_button("Исследование «Партизанское движение на Гомельщине» ↗️", "https://github.io")
