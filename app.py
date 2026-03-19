import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

st.set_page_config(
    page_title="서울시 상수도 노후화 분석",
    page_icon="💧",
    layout="wide"
)

# -----------------------------
# 데이터 정의
# -----------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    data = [
        ["종로구", 44, 85, 0.35, 0.18, 0.12, 0.03, 7],
        ["중구", 38, 78, 0.29, 0.20, 0.10, 0.02, 6],
        ["강북구", 46, 88, 0.38, 0.17, 0.13, 0.03, 9],
        ["관악구", 42, 83, 0.34, 0.18, 0.12, 0.03, 8],
        ["서초구", 18, 30, 0.11, 0.34, 0.03, 0.01, 0],
        ["강남구", 20, 33, 0.12, 0.33, 0.04, 0.01, 1],
        ["송파구", 22, 38, 0.13, 0.32, 0.04, 0.01, 1],
        ["은평구", 36, 72, 0.27, 0.23, 0.09, 0.02, 5],
        ["구로구", 32, 67, 0.24, 0.24, 0.08, 0.02, 4],
        ["영등포구", 40, 81, 0.32, 0.19, 0.11, 0.03, 7],
    ]
    columns = ["지역구", "사용연수", "부식도", "탁도", "잔류염소", "철", "망간", "민원"]
    return pd.DataFrame(data, columns=columns)


df = load_data()

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.title("메뉴")
page = st.sidebar.radio(
    "페이지 선택",
    ["개요", "데이터", "상관관계", "추가 분석", "정책 시사점"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "본 앱은 서울시 상수도 노후화 및 수질 영향 분석 보고서를 바탕으로 만든 러프 버전입니다."
)

# -----------------------------
# 공통 헤더
# -----------------------------
st.title("서울시 상수도 노후화 및 수질 영향 분석")
st.caption("인턴용 러프 Streamlit 앱")

# -----------------------------
# 페이지 1: 개요
# -----------------------------
if page == "개요":
    st.subheader("연구 개요")

    st.markdown("""
    이 앱은 서울시 자치구별 가상 데이터를 바탕으로  
    **상수도 노후화와 수질 변화의 관계**를 간단히 확인하기 위한 프로토타입입니다.

    핵심 구조는 다음과 같습니다.

    **노후화 → 부식 증가 → 수질 악화 → 시민 민원**
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("분석 지역 수", f"{len(df)}개")
    col2.metric("평균 사용연수", f"{df['사용연수'].mean():.1f}년")
    col3.metric("평균 민원", f"{df['민원'].mean():.1f}건")

    st.markdown("### 주요 해석")
    st.write(
        "사용연수가 높고 부식도가 큰 지역일수록 탁도와 철 농도가 높고, "
        "잔류염소는 낮아지는 경향을 보입니다. "
        "이는 노후 수도관이 수질 악화와 연결될 수 있음을 시사합니다."
    )

# -----------------------------
# 페이지 2: 데이터
# -----------------------------
elif page == "데이터":
    st.subheader("원시 데이터")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 기초 통계")
    st.dataframe(df.describe(), use_container_width=True)

# -----------------------------
# 페이지 3: 상관관계
# -----------------------------
elif page == "상관관계":
    st.subheader("노후도-수질 상관관계")

    corr = df.drop(columns=["지역구"]).corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, vmin=-1, vmax=1)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    ax.set_title("상관관계 히트맵")

    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)

    fig.colorbar(im, ax=ax)
    st.pyplot(fig)

    st.markdown("### 해석")
    st.write(
        "- 사용연수와 부식도는 강한 양의 상관관계를 보입니다.\n"
        "- 부식도는 탁도 및 철 농도 증가와 연결됩니다.\n"
        "- 잔류염소는 상대적으로 감소하는 방향을 보입니다."
    )

# -----------------------------
# 페이지 4: 추가 분석
# -----------------------------
elif page == "추가 분석":
    st.subheader("사용연수와 탁도 관계")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["사용연수"], df["탁도"])

    for _, row in df.iterrows():
        ax.annotate(row["지역구"], (row["사용연수"], row["탁도"]), fontsize=8)

    ax.set_xlabel("사용연수")
    ax.set_ylabel("탁도")
    ax.set_title("사용연수 vs 탁도")
    st.pyplot(fig)

    st.markdown("### 해석")
    st.write(
        "사용연수가 높을수록 탁도가 증가하는 경향이 관찰됩니다. "
        "러프한 데이터이므로 엄밀한 인과 해석보다는, "
        "노후화와 수질 악화가 함께 나타나는 패턴을 확인하는 수준으로 보는 것이 적절합니다."
    )

# -----------------------------
# 페이지 5: 정책 시사점
# -----------------------------
elif page == "정책 시사점":
    st.subheader("정책 시사점")

    st.markdown("""
    ### 1. 상태 기반 관리 필요
    단순히 오래된 관을 교체하는 방식보다,  
    **부식도·탁도·민원 수준**을 함께 고려한 우선순위 설정이 필요합니다.

    ### 2. 시민 수용성 고려
    수도관 교체는 필요하지만, 공사 과정에서 단수·교통 통제·소음이 발생할 수 있습니다.  
    따라서 **공사 필요성과 시민 수용성을 동시에 고려한 계획 수립**이 중요합니다.

    ### 3. 실행 예시
    - 단계적 시공
    - 사전 공지 강화
    - 민원 대응 체계 운영
    - 상업지역/주거지역 맞춤형 공사 시간 조정
    """)

    st.success("핵심 메시지: 노후화는 시설 문제가 아니라 수질과 시민 생활 문제로 이어집니다.")
