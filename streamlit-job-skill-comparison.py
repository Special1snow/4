import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load the job skills data
@st.cache_data
def load_data():
    data = {
        'Skill': [
            '분석적 사고', '창의적 사고', '유연성과 민첩성',
            '동기부여', '자기개발',
            '기술력', '섬세함',
            '공감과 경청', '리더십과 영향력',
            '품질 관리', '시스템 사고', '인재 관리',
            '고객 서비스', '자원 관리 및 운영',
            'AI 및 빅데이터', '읽기,쓰기',
            '사용자 경험', '외국어', '교육 및 멘토링',
            '프로그래밍', '마케팅 및 미디어', '사이버 보안',
            '환경 관리', '지구력 및 정밀도',
            'Globality', '직관력', '커뮤니케이션',
            '스토리텔링', 'Biz통찰력', 'MS Office(엑셀,PPT)'
        ],
        '전략/기획': [8.2, 8.5, 8.4, 8.1, 7.8, 7.0, 8.6, 6.9, 9.0, 8.7, 7.7, 8.8, 7.0, 8.0, 7.6, 9.0, 5.8, 6.8, 8.6, 6.9, 8.3, 7.7, 5.5, 8.2, 7.6, 7.0, 8.5, 8.4, 9.2, 8.1],
        '성과관리': [6.5, 5.1, 6.7, 7.6, 5.3, 5.5, 8.1, 5.4, 7.1, 8.2, 8.4, 7.2, 6.4, 7.9, 5.3, 9.1, 4.1, 5.4, 7.4, 4.0, 4.3, 4.5, 4.8, 5.2, 5.3, 5.5, 6.3, 6.2, 7.6, 5.7],
        '사업개발': [7.8, 8.6, 8.9, 9.2, 8.5, 8.0, 7.3, 6.4, 9.3, 7.4, 7.0, 8.4, 5.6, 8.5, 8.6, 8.5, 6.6, 7.1, 7.2, 7.2, 8.7, 7.0, 6.2, 6.8, 8.0, 7.1, 6.8, 8.5, 9.7, 7.6],
        '마케팅/영업': [5.4, 9.0, 7.6, 5.7, 5.5, 9.2, 5.6, 8.9, 7.9, 5.6, 5.9, 6.2, 9.1, 6.4, 6.5, 5.8, 9.3, 7.6, 5.4, 8.1, 9.8, 7.9, 5.0, 5.5, 7.7, 5.1, 8.0, 9.4, 7.8, 6.1],
        '생산/기술': [8.5, 4.8, 6.6, 5.9, 9.0, 9.5, 9.1, 4.6, 5.5, 9.9, 9.4, 5.1, 5.3, 9.2, 9.8, 5.1, 5.4, 5.3, 6.1, 9.9, 4.4, 9.5, 7.9, 9.8, 5.5, 9.9, 5.8, 5.0, 5.0, 5.0],
        '구매/SCM': [6.3, 4.5, 5.4, 6.1, 5.0, 9.3, 8.0, 4.7, 6.3, 9.1, 9.2, 6.3, 4.6, 9.4, 10.0, 4.8, 4.9, 5.0, 5.0, 9.5, 4.6, 9.7, 7.2, 9.2, 5.2, 9.4, 5.5, 4.8, 5.4, 4.9],
        '재무/회계': [9.0, 4.2, 7.1, 7.5, 7.3, 7.4, 9.2, 5.4, 7.5, 8.0, 7.5, 6.0, 5.0, 6.5, 8.4, 5.6, 5.5, 5.4, 5.3, 6.8, 5.4, 8.2, 6.8, 6.6, 5.5, 7.2, 6.5, 5.2, 5.8, 6.0],
        'IP/법무': [7.2, 3.5, 5.0, 5.5, 4.0, 5.5, 7.3, 4.5, 6.0, 5.6, 5.2, 5.0, 4.5, 5.4, 6.1, 8.7, 4.3, 4.9, 4.8, 5.3, 4.1, 6.5, 5.0, 5.4, 5.3, 5.1, 5.2, 4.0, 5.4, 9.3],
        'R&D': [10.0, 9.3, 8.8, 7.2, 9.2, 9.8, 8.7, 5.5, 7.1, 9.6, 9.7, 6.4, 5.3, 9.3, 9.9, 9.5, 9.6, 4.2, 8.4, 9.7, 5.5, 9.8, 9.4, 9.2, 6.1, 9.5, 6.9, 5.4, 6.2, 8.9],
        'Staff': [7.0, 5.6, 6.2, 7.0, 5.5, 6.0, 7.1, 6.8, 6.9, 6.6, 6.5, 6.9, 6.5, 6.5, 5.5, 6.7, 5.6, 6.7, 5.4, 5.6, 6.2, 5.5, 6.3, 6.2, 6.5, 5.8, 6.4, 6.7, 6.7, 6.3],
        'O/I, 최적화': [7.4, 5.5, 6.3, 8.0, 5.4, 6.6, 7.0, 6.5, 6.2, 6.7, 7.1, 7.2, 6.4, 7.3, 6.8, 6.5, 6.7, 7.0, 7.1, 7.0, 7.0, 6.7, 6.4, 7.0, 7.1, 6.9, 6.4, 7.1, 7.3, 6.8],
        'Trading': [5.5, 7.6, 7.8, 6.0, 7.2, 7.0, 7.4, 7.8, 6.8, 7.0, 6.3, 6.4, 7.7, 7.6, 6.7, 6.3, 7.2, 8.1, 7.5, 6.6, 7.8, 6.2, 7.0, 6.7, 8.0, 6.5, 8.1, 8.3, 8.0, 6.6],
        'HR': [7.5, 7.0, 8.0, 9.5, 8.0, 5.0, 8.5, 9.0, 7.5, 7.0, 6.0, 10.0, 7.0, 7.5, 3.0, 8.0, 5.0, 6.5, 9.5, 2.5, 3.0, 4.5, 2.0, 4.0, 7.0, 5.0, 9.0, 9.0, 9.5, 8.0]
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar for user info and navigation
st.sidebar.title("사용자 정보")
name = st.sidebar.text_input("이름")
employee_id = st.sidebar.text_input("사번")
department = st.sidebar.text_input("부서명")

page = st.sidebar.selectbox("페이지 선택", ["역량 입력 및 비교", "직무별 요구 역량 점수"])

if page == "역량 입력 및 비교":
    st.title('직무별 역량 비교 분석')

    # User input for skills
    st.header('자신의 역량 점수 입력')
    user_skills = {}
    
    # 수정된 부분: 슬라이더 레이아웃 변경 및 타입 체크 추가
    skills = df['Skill'].tolist()
    for i in range(0, len(skills), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(skills):
                skill = skills[i + j]
                user_skills[str(skill)] = cols[j].slider(
                    f'{str(skill)}',
                    min_value=3.0,
                    max_value=10.0,
                    value=7.0,
                    step=0.5,
                    key=f'skill_{i+j}'
                )

    # Calculate similarity scores
    def calculate_similarity(user_scores, job_scores):
        return np.mean(1 - np.abs(np.array(list(user_scores)) - np.array(job_scores)) / 10)

    similarities = {}
    for job in df.columns[1:]:
        similarities[job] = calculate_similarity(user_skills.values(), df[job])

    # Display results
    st.header('직무 적합도 분석 결과')
    result_df = pd.DataFrame(list(similarities.items()), columns=['직무', '적합도'])
    result_df['적합도'] = result_df['적합도'].round(2)  # 소수점 둘째 자리까지 반올림
    result_df = result_df.sort_values('적합도', ascending=False)

    st.write(result_df)

    # Visualize results
    st.header('직무 적합도 시각화')
    # 가장 높은 적합도를 가진 직무 찾기
    max_similarity_job = result_df['직무'].iloc[0]

    # 색상 리스트 생성
    colors = ['red' if job == max_similarity_job else 'blue' for job in result_df['직무']]

    fig = go.Figure(data=[go.Bar(
    x=result_df['직무'],
    y=result_df['적합도'],
    marker_color=colors
    )])

    fig.update_layout(
    title=f'{name}님의 직무별 적합도' if name else '직무별 적합도',
    xaxis_title='직무',
    yaxis_title='적합도'
    )

    st.plotly_chart(fig)

    # Job selection for comparison
    st.header('특정 직무와 비교')
    selected_job = st.selectbox('비교할 직무 선택', df.columns[1:])

    # Radar chart for selected job
    st.subheader(f'{selected_job} 직무와의 역량 비교')
    fig = go.Figure()

    # Add user's skills
    fig.add_trace(go.Scatterpolar(
        r=list(user_skills.values()),
        theta=df['Skill'],
        fill='toself',
        name=f'{name}의 역량' if name else 'Your Skills',
        line_color='red'
    ))

    # Add selected job
    fig.add_trace(go.Scatterpolar(
        r=df[selected_job],
        theta=df['Skill'],
        fill='toself',
        name=selected_job
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True
    )

    st.plotly_chart(fig)

    st.write("이 분석 결과는 참고용이며, 실제 직무 적합성은 다양한 요소를 종합적으로 고려해야 합니다.")

elif page == "직무별 요구 역량 점수":
    st.title('직무별 요구 역량 점수')
    
    # Display full dataframe
    st.write(df)
    
    # Allow downloading as CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="CSV로 다운로드",
        data=csv,
        file_name="job_skills_data.csv",
        mime="text/csv",
    )
    
    # Job selection for detailed view
    selected_job = st.selectbox('상세 보기를 원하는 직무 선택', df.columns[1:])
    
    # Display selected job's skills
    st.subheader(f'{selected_job} 직무 요구 역량')
    job_skills = df[['Skill', selected_job]].sort_values(selected_job, ascending=False)
    st.write(job_skills)
    
    # Visualize selected job's skills
    fig = go.Figure(data=[go.Bar(x=job_skills['Skill'], y=job_skills[selected_job])])
    fig.update_layout(title=f'{selected_job} 직무 요구 역량', xaxis_title='역량', yaxis_title='점수')
    st.plotly_chart(fig)

    # Gap 분석 함수 추가
    def calculate_gap(user_skills, job_skills):
    gaps = {}
    for skill, user_score in user_skills.items():
        job_score = job_skills[skill]
        gap = job_score - user_score
        gaps[skill] = gap
    return gaps

    # 메인 페이지 선택 옵션에 'Gap 분석' 추가
    page = st.sidebar.selectbox("페이지 선택", ["역량 입력 및 비교", "직무별 요구 역량 점수", "Gap 분석"])

if page == "역량 입력 및 비교":
    # 기존의 '역량 입력 및 비교' 페이지 코드
    # ...

elif page == "직무별 요구 역량 점수":
    # 기존의 '직무별 요구 역량 점수' 페이지 코드
    # ...

elif page == "Gap 분석":
    st.title('역량 Gap 분석')

    # 사용자 역량 불러오기 (이전 페이지에서 입력한 값을 세션 상태로 저장했다고 가정)
    if 'user_skills' not in st.session_state:
        st.error("먼저 '역량 입력 및 비교' 페이지에서 자신의 역량을 입력해주세요.")
        st.stop()

    user_skills = st.session_state.user_skills

    # 직무 선택
    selected_job = st.selectbox('비교할 직무 선택', df.columns[1:])

    # 선택된 직무의 스킬 점수
    job_skills = dict(zip(df['Skill'], df[selected_job]))

    # Gap 계산
    gaps = calculate_gap(user_skills, job_skills)

    # Gap을 내림차순으로 정렬
    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1], reverse=True)

    # 결과 표시
    st.subheader("개선이 필요한 역량 (Gap이 큰 순서):")
    gap_df = pd.DataFrame(sorted_gaps, columns=['역량', 'Gap'])
    gap_df['현재 점수'] = gap_df['역량'].map(user_skills)
    gap_df['목표 점수'] = gap_df['역량'].map(job_skills)
    gap_df = gap_df[gap_df['Gap'] > 0]  # 양수 Gap만 표시
    gap_df = gap_df.reset_index(drop=True)
    gap_df.index = gap_df.index + 1  # 인덱스를 1부터 시작하도록 설정
    st.table(gap_df)

    # 상위 5개 개선 필요 역량에 대한 막대 그래프
    top_5_gaps = gap_df.head()
    fig = go.Figure(data=[
        go.Bar(name='현재 점수', x=top_5_gaps['역량'], y=top_5_gaps['현재 점수']),
        go.Bar(name='목표 점수', x=top_5_gaps['역량'], y=top_5_gaps['목표 점수'])
    ])
    fig.update_layout(barmode='group', title='상위 5개 개선 필요 역량', xaxis_title='역량', yaxis_title='점수')
    st.plotly_chart(fig)

    st.write("이 분석은 선택한 직무에서 요구하는 역량과 현재 본인의 역량 사이의 차이를 보여줍니다. Gap이 큰 역량일수록 개선의 여지가 크다는 것을 의미합니다.")

    # '역량 입력 및 비교' 페이지에서 사용자 입력을 세션 상태로 저장하는 코드 추가
    if page == "역량 입력 및 비교":

    # 사용자 입력을 세션 상태로 저장
    st.session_state.user_skills = user_skills
