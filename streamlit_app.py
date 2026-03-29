import streamlit as st
import os

# ==========================================
# 0. 網頁初始設定
# ==========================================
st.set_page_config(page_title="狀態與情緒能量量測系統", page_icon="⚖️", layout="centered")

st.markdown("""
<style>
    .big-font { font-size:1.2rem !important; font-weight: bold; color: #2c3e50; margin-bottom: 0.5rem; }
    .question-box { border: 1px solid #ddd; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; background-color: #fcfcfc; }
    .stRadio div[role="radiogroup"] { flex-direction: row !important; }
    .stRadio label { font-weight: normal; margin-right: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 安全密碼驗證邏輯
# ==========================================
def check_password():
    CORRECT_PASSWORD = os.environ.get("APP_PASSWORD", "1qaz@WSX#EDC")
    if st.session_state["password_input"] == CORRECT_PASSWORD:
        st.session_state["password_correct"] = True
    else:
        st.session_state["password_correct"] = False
        st.error("🔒 密碼錯誤，請重新輸入。")

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("⚖️ 生命狀態量測系統")
    st.markdown("---")
    st.markdown("### 歡迎來到深度自我覺察旅程\n請輸入專屬通關密碼以存取測驗。")
    st.text_input("存取密碼", type="password", on_change=check_password, key="password_input")
    st.stop()

# ==========================================
# 2. 資料定義與輔助函數
# ==========================================
score_options = [1, 2, 3, 4, 5]
score_display = {1: "1:完全不符合", 2: "2:很少符合", 3: "3:部分符合", 4: "4:大多符合", 5: "5:完全符合"}

def get_grade_info(total_score, aspect):
    if 46 <= total_score <= 50:
        grade, ee_text, rq_text = 5, "超越共鳴，豐盛連結", "我們關係，獨立合一"
    elif 39 <= total_score <= 45:
        grade, ee_text, rq_text = 4, "積極有序，全神貫注", "支持關係，相互成就"
    elif 32 <= total_score <= 38:
        grade, ee_text, rq_text = 3, "平穩包容，順勢自覺", "功能關係，合作互惠"
    elif 23 <= total_score <= 31:
        grade, ee_text, rq_text = 2, "緊張焦慮，急躁疲憊", "消耗關係，安全匱乏"
    elif 10 <= total_score <= 22:
        grade, ee_text, rq_text = 1, "麻木無力，行動癱瘓", "鬆脫關係，失去自我"
    else:
        return 0, "分數異常"
    return grade, ee_text if aspect == "EE" else rq_text

questions_data = {
    "EE": [
        "我能快速覺察到情緒的起伏，並清楚知道自己內心真正「想要」的是什麼。",
        "我常常能感受到內在的豐盛與充實，容易產生對生活的感恩與滿足。",
        "挑戰任務來臨時，我能看見成長機會，並享受解決過程帶來的掌控感。",
        "即使遭遇挫折，我會立即提醒自己不陷入被害者心態，並主動尋找解決方案。",
        "情緒波動時，我能快速地將注意力轉回當下，帶著更加自律而專注的狀態，繼續手邊的任務。",
        "在被誤解或指責的瞬間，我能安住於傾聽，展現柔軟，讓辯解與反擊的衝動自然消融。",
        "我能維持自身內在秩序，並自然帶動周圍氛圍從低氣壓轉向積極或安寧。",
        "當周圍充滿批判或憤怒時，我能保持內心安定，不被輕易捲入情緒風暴。",
        "當負面情緒升起時，我不會進行自我批判或向外對抗，而是以單純的覺知，允許情緒自然流動。",
        "遇到衝突時，我的語氣、表情和肢體始終保持平和，態度從容穩定，不易被現場混亂影響。"
    ],
    "RQ": [
        "當立場不同時，我不會讓認知差異轉化為對關係的攻擊或疏離。",
        "在功能性的合作中，我能盡責尊重、步履一致，避免個人干擾整體。",
        "在重要的人面前，我感到安全，能夠自然地展現脆弱，不需刻意戴上面具。",
        "我能敏銳地感受他人的善意，並且在多數時刻我都是敞開的。",
        "面對矛盾，我傾向訴說出想法並連結溝通，幾乎不會出現逃避、討好或事後諸葛。",
        "內心深信，即使我尚未成功，身旁仍有願意支持並祝福我的人。",
        "對他人的付出，我常能感受到喜悅流動，事後能量增強，鮮少感到委屈或疲憊。",
        "在關係中，我大多時候不需包裝掩飾，能自然地信任對方不會傷害我。",
        "在日常工作生活或利益往來之外，我的人際圈中，仍能時常體驗到心靈共鳴的時刻。",
        "我能自然地創造並維持彼此深度同頻，享受那種無需言語便能心意相通的默契時刻。"
    ]
}

# ==========================================
# 3. 測驗表單
# ==========================================
st.title("📊 生命狀態 (Life State) 深度量測")
st.markdown("---")

with st.expander("🧐 測評規則 - 請憑直覺回答問題", expanded=True):
    st.markdown("""
    請依據您目前的真實**現狀**評分：
    * **5分：** 完全符合
    * **4分：** 大多符合
    * **3分：** 部分符合
    * **2分：** 很少符合
    * **1分：** 完全不符合
    
    💡 **這不是選「你希望成為/理想中/認同的樣子」，而是選「你當下最符合的狀態」。真實作答，而非「表演式」作答，這不是面試。**
    
    💡 **此分數反映此刻狀態，無好壞之分，唯有真實才有力量**
    
    """)    

with st.form("assessment_form"):
    score_inputs = {"EE": [], "RQ": []}
    st.header("第一部分：情緒能量狀態自測 (EE)")
    st.markdown("---")
    for i, q_text in enumerate(questions_data["EE"]):
        st.markdown(f'<div class="question-box"><div class="big-font"> EE.{i+1:02d} {q_text}</div>', unsafe_allow_html=True)
        score = st.radio("請選擇評分", options=score_options, format_func=lambda x: score_display[x], horizontal=True, key=f"EE_Q{i+1}", label_visibility="collapsed")
        score_inputs["EE"].append(score)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("第二部分：關係品質狀態自測 (RQ)")
    st.markdown("---")
    for i, q_text in enumerate(questions_data["RQ"]):
        st.markdown(f'<div class="question-box"><div class="big-font"> RQ.{i+1:02d} {q_text}</div>', unsafe_allow_html=True)
        score = st.radio("請選擇評分", options=score_options, format_func=lambda x: score_display[x], horizontal=True, key=f"RQ_Q{i+1}", label_visibility="collapsed")
        score_inputs["RQ"].append(score)
        st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("送出並看深度分析結果")
    if submitted:
        st.session_state['total_ee'] = sum(score_inputs["EE"])
        st.session_state['total_rq'] = sum(score_inputs["RQ"])
        st.session_state['has_submitted'] = True

# ==========================================
# 4. 結果顯示與深度分析
# ==========================================
if st.session_state.get('has_submitted', False):
    total_score_ee = st.session_state['total_ee']
    total_score_rq = st.session_state['total_rq']
    
    ee_grade, ee_text = get_grade_info(total_score_ee, "EE")
    rq_grade, rq_text = get_grade_info(total_score_rq, "RQ")
    life_state_s = ee_grade * rq_grade
    
    st.markdown("---")
    if submitted:
        st.balloons()  
        
    st.markdown("## 🎯 您的測評結果深度報告")
    col_ee, col_rq = st.columns(2)
    with col_ee:
        st.metric(label="情緒能量總分 (EE)", value=f"{total_score_ee} / 50")
        st.info(f"### EE級分：{ee_grade} 分\n**狀態落點：{ee_text}**")
    with col_rq:
        st.metric(label="關係品質總分 (RQ)", value=f"{total_score_rq} / 50")
        st.success(f"### RQ級分：{rq_grade} 分\n**狀態落點：{rq_text}**")
        
    st.markdown("---")
    st.header(f"🧮 生命狀態 (S) 指數: {life_state_s}")
    
    def get_life_state_desc(ee, rq):
        if ee <= 2 and rq <= 2: return "無力停滯", "🪫", "#95a5a6", "目前內在無動力且關係安全匱乏。您可能感到全身麻木無力、行動癱瘓，請優先給予自己最大的包容與接納，關注最基礎的身心安頓，而非強求改變。"
        elif ee >= 4 and rq >= 4: return "圓滿流動", "✅", "#27ae60", "您的生命能量如圓滿流動的活水，內在積極有序、全神貫注，關係則支持祝福、獨立合一。這是一個能同時利益自身與周圍人的狀態，請享受這一刻的豐盛。"
        elif ee == 3 and rq == 3: return "3x3 平衡協作 (中心點)", "☯️", "#3498db", "您處於生命狀態的唯一中心點，呈現一種動態的平衡。您能以平穩的自覺與他人合作互惠。這是一個穩定、能同時觀照內外的中道狀態。"
        else:
            if ee > rq: return "高能消耗", "⚠️", "#f1c40f", "您內在能量極高且積極，但關係品質可能未能在同頻上，導致關係在無形中消耗您的能量。請檢視關係中的獨立性與信任，找出「對抗」或「疏離」的源頭。"
            elif ee < rq: return "蓄能發展", "🏗️", "#9b59b6", "您能創造深度同頻、相互支持的關係網，但此刻內在可能較感焦慮、疲憊。您可能更傾向利用外部支持系統鏈結溝通、逃避內在矛盾。這是一個蓄能期，請在安全關係中，轉而關照自身的情緒流動。"
            else: return "動態失衡", "🟡", "#f1c40f", "生命充滿了變化與挑戰。此刻您的能量與關係雖然可能不如您意，但也同時呈現出一種獨特的現狀，唯有接受並觀察它，才能找出向前的方向。"
    
    label, icon, color, desc = get_life_state_desc(ee_grade, rq_grade)
    st.markdown(f"<div style='border: 2px solid {color}; padding: 1.5rem; border-radius: 15px; margin-top: 1rem; background-color: #fcfcfc;'><h3 style='color: {color};'>{icon} 狀態落點分類：{label}</h3><p style='font-size: 1.1rem; color: #2c3e50; font-weight: bold;'>{""}</p></div>", unsafe_allow_html=True)
    st.markdown("---")

    # ==========================================
    # 5. 5x5 生命狀態落點矩陣圖
    # ==========================================
    st.markdown("### 🗺️ 生命狀態 5x5 落點矩陣圖")
    st.markdown("💡 閃爍的紅點代表您目前的狀態落點。圖表僅針對您所在的區域進行上色。")

    def get_life_state_grid_html(user_e, user_r, special_choice=None):
        def get_region(e, r):
            if e >= 4 and r >= 4: return "red"
            elif e <= 2 and r <= 2: return "brown"
            elif e == 3 and r == 3: return "center"
            elif e > r: return "green"
            elif e < r: return "blue"
            return "none"
            
        user_region = get_region(user_e, user_r)
        colors = {"red": "#B06B6B", "brown": "#72615D", "green": "#A6BA71", "blue": "#7685A9", "center": "#FFFFFF", "inactive": "#F4F6F7"}

        html = ""
        html += "<style>"
        html += "@keyframes pulse { 0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 65, 54, 0.7); } 70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(255, 65, 54, 0); } 100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 65, 54, 0); } }"
        html += ".life-grid { border-collapse: collapse; margin: 0 auto; width: 100%; max-width: 650px; font-family: sans-serif; text-align: center; border: none; }"
        html += ".life-grid td { border: 1px solid #fff; width: 16%; height: 85px; position: relative; vertical-align: middle; }"
        html += ".marker { width: 18px; height: 18px; background-color: #FF4136; border: 2px solid #FFF; border-radius: 50%; margin: 5px auto; box-shadow: 0 0 8px rgba(0,0,0,0.8); animation: pulse 1.5s infinite; }"
        html += ".label-text { font-weight: bold; font-size: 0.95rem; }"
        html += ".letter-text { font-size: 1.8rem; font-family: 'Georgia', serif; font-style: italic; text-shadow: 1px 1px 0 #fff, -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff; margin-bottom: -5px; }"
        html += ".score-th { background-color: #8E9CA0 !important; color: white !important; border: 1px solid #fff !important; padding: 8px; font-size: 1.1rem; text-align: center; }"
        html += ".title-th { background-color: #8E9CA0 !important; color: white !important; border: 1px solid #fff !important; font-size: 1.5rem; letter-spacing: 5px; vertical-align: middle; }"
        html += ".filler-th { background-color: #8E9CA0 !important; border: 1px solid #fff !important; }"
        html += "</style>"
        
        html += '<div style="width:100%; overflow-x:auto;"><table class="life-grid">'
        html += '<tr><th colspan="2" class="filler-th"></th><th colspan="5" class="title-th">關係</th></tr>'
        html += '<tr><th colspan="2" class="filler-th"></th><th class="score-th">1分</th><th class="score-th">2分</th><th class="score-th">3分</th><th class="score-th">4分</th><th class="score-th">5分</th></tr>'

        for e in range(5, 0, -1):
            html += "<tr>"
            if e == 5: html += '<th rowspan="5" class="title-th">情<br><br>緒</th>'
            html += f'<th class="score-th">{e}分</th>'
            
            for r in range(1, 6):
                cell_region = get_region(e, r)
                is_active = (cell_region == user_region)
                bg_color = colors[cell_region] if is_active else colors["inactive"]
                if cell_region == "center": bg_color = colors["center"]
                
                text_style = "color: #FFE699; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);" if is_active else "color: #C0C0C0; text-shadow: none;"
                cell_content = ""
                
                if e == 4 and r == 5: cell_content += f'<div class="label-text" style="{text_style}">圓滿流動</div>'
                elif e == 2 and r == 2: cell_content += f'<div class="label-text" style="{text_style}">無力停滯</div>'
                elif e == 4 and r == 2: cell_content += f'<div class="label-text" style="{text_style}">高能消耗</div>'
                elif e == 2 and r == 4: cell_content += f'<div class="label-text" style="{text_style}">蓄能發展</div>'
                
                if e == 3 and r == 3:
                    if is_active and special_choice:
                        if special_choice == "A": cell_content += '<div class="letter-text" style="color:#C0392B;">A</div><div class="label-text" style="color:#555;">高能消耗</div>'
                        elif special_choice == "B": cell_content += '<div class="letter-text" style="color:#2980B9;">B</div><div class="label-text" style="color:#555;">蓄能發展</div>'
                        elif special_choice == "C": cell_content += '<div class="letter-text" style="color:#27AE60;">C</div><div class="label-text" style="color:#555;">平衡協作</div>'
                    else:
                        center_text_style = "color: #555;" if is_active else "color: #C0C0C0;"
                        cell_content += f'<div style="font-weight:bold; {center_text_style} font-size:1.1rem; margin-top:5px;">3 x 3</div><div class="label-text" style="{center_text_style}">平衡協作</div>'
                
                if e == user_e and r == user_r:
                    cell_content = f'<div class="marker" title="您的落點: 情緒{e}分, 關係{r}分"></div>' + cell_content
                
                html += f'<td style="background-color: {bg_color};">{cell_content}</td>'
            html += "</tr>"
        html += "</table></div>"
        return html

    current_choice = st.session_state.get("special_q_final", None)
    st.markdown(get_life_state_grid_html(ee_grade, rq_grade, current_choice), unsafe_allow_html=True)
    st.markdown("---")

    # ==========================================
    # 6. 3x3 特別覺察題
    # ==========================================
    if ee_grade == 3 and rq_grade == 3:
        st.header("🕵️‍♂️ 深度覺察：3x3 中心點的偏差方向")
        st.markdown("您的狀態正處於「情緒‧關係」的中心點。這是一個非常細微的動態平衡位置。為了幫助您更精確地觀察自己，請您感覺此刻更偏向哪一種結構？")
        st.info("""
        **A.** 「我覺得自己內在能量還算穩定，有很多想法，但常常覺得無人分享。『孤軍奮戰』的感覺讓我感到空轉與浪費讓我嚴重耗損，沒有人會支持我的想法。」
        
        **B.** 「我覺得自己的狀態還不穩定。但我很幸運，身邊有家人朋友的陪伴和支持，讓我覺得安全。有他們在，我會越來越好；沒有他們，我應該更難熬。」
        
        **C.** 「我現在這樣就很好了。這樣清靜的生活就是我想要的，沒有太多意外跟打擾。大家按規矩辦事，互不干擾。維持現狀就是最好的策略。」
        """)
        
        special_choice = st.radio("請選擇最符合您目前感受的一項：", options=["A", "B", "C"], index=None, horizontal=True, key="special_q_final")
        
        if special_choice == "A":
            st.warning("💡 **分析 A：** 您的偏差方向傾向「高能消耗」。您有想法、有能量，但受挫於關係網的支持力不足，請練習在關係中訴說想法、連結溝通。")
        elif special_choice == "B":
            st.success("💡 **分析 B：** 您的偏差方向傾向「蓄能發展」。您的關係品質提供了安全，但內在能量仍不夠安定，請在安全的關係中，試著不逃避內在矛盾，關注自我情緒流動。")
        elif special_choice == "C":
            st.info("💡 **分析 C：** 您的偏差方向傾向「維持現狀」。您更在意自身秩序的安寧，這對目前的您是安全的，但當環境有意外時，您可能需要思考如何在自身秩序之外維持關係彈性。")