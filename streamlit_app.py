import streamlit as st
import json
import random
import os

# 파일 경로
FILE_PATH = "problems.json"

# 문제 불러오기
if not os.path.exists(FILE_PATH):
    st.error("❌ problems.json 파일이 없습니다. 파일을 업로드하거나 경로를 확인하세요.")
    st.stop()

with open(FILE_PATH, "r", encoding="utf-8") as f:
    problems = json.load(f)

# 단원과 난이도 옵션
units = sorted(set(p['단원'] for p in problems))
difficulties = ["easy", "medium", "hard"]

# UI 구성
st.set_page_config(page_title="AI 수학 튜터", layout="centered")
st.title("📘 AI 기반 수학 학습 피드백 플랫폼")

# 사이드바 선택
st.sidebar.header("🔍 문제 선택 조건")
selected_unit = st.sidebar.selectbox("단원", units)
selected_difficulty = st.sidebar.radio("난이도", difficulties)

# 필터링된 문제 무작위 선택
filtered = [p for p in problems if p['단원'] == selected_unit and p['난이도'] == selected_difficulty]
problem = random.choice(filtered) if filtered else None

# 문제 표시
if problem:
    st.markdown("---")
    st.subheader("❓ 문제")
    st.markdown(f"**{problem['문제']}**")

    # 정답 입력
    st.markdown("---")
    st.subheader("✏️ 정답을 입력하세요")
    col1, col2 = st.columns([3, 1])
    user_answer = col1.text_input("", key="answer")
    with col2:
        if st.button("√"): st.session_state.answer += "√"
        if st.button("^2"): st.session_state.answer += "²"

    # 사고 과정 입력
    st.markdown("---")
    st.subheader("🧠 사고 과정 입력")
    user_thinking = st.text_area("당신의 사고 흐름을 설명해보세요")

    # 채점 및 피드백
    if st.button("🧪 채점하기"):
        correct = problem['정답'].strip().lower()
        user = user_answer.strip().lower()
        st.markdown("---")
        st.subheader("📝 채점 결과")
        if user == correct:
            st.success("정답입니다! 🎉")
        else:
            st.error("오답입니다.")
            st.markdown(f"**📌 오답 피드백:** {problem.get('오답피드백', '풀이를 다시 확인해보세요.')}")

        st.markdown(f"**📖 AI 해설:** {problem.get('AI사고', 'AI 해설을 준비 중입니다.')}")

        # 개념 영상 링크 (있을 경우만 표시)
        if problem.get("개념영상"):
            st.markdown("---")
            st.subheader("🎬 개념 영상")
            st.video(problem["개념영상"])

    # 사고 비교
    if st.button("🤖 AI 사고와 비교하기"):
        st.markdown("---")
        st.subheader("🔍 AI 사고 흐름 복기")
        st.info(problem.get("AI사고", "AI의 사고 흐름을 불러올 수 없습니다."))

        prompt = problem.get("AI질문") or f"이 문제 해결 과정에서 핵심 개념은 무엇인가요? ({problem.get('AI사고', '')})"
        st.markdown(f"**💭 사고 유도 질문:** {prompt}")

else:
    st.warning("선택한 조건에 맞는 문제가 없습니다. 다른 단원이나 난이도를 선택해보세요.")
