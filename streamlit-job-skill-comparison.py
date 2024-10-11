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

    # Load the course competency matrix
    @st.cache_data
    def load_course_data():
        data = {
            'Course Name': [
                '데이터 기반 의사결정: 비즈니스 분석의 핵심',
                '디자인 씽킹: 혁신적 문제 해결 방법론',
                '애자일 방법론: 변화에 빠르게 적응하기',
                '자기 결정 이론: 내재적 동기 극대화하기',
                '평생 학습자의 마인드셋: 성장형 사고방식 기르기',
                '4차 산업혁명 핵심 기술 이해하기',
                '감성 지능: 자신과 타인의 감정 이해하기',
                '적극적 경청: 깊이 있는 대화의 기술',
                '변혁적 리더십: 팀을 혁신으로 이끄는 방법',
                '식스 시그마: 데이터 기반 품질 개선',
                '복잡계 이론: 조직을 하나의 생태계로 보기',
                '인재 유치와 유지: 최고의 인재 확보 전략',
                '옴니채널 고객 경험 디자인',
                '지속 가능한 공급망 관리',
                '머신러닝 기초: 비즈니스 인사이트 도출',
                '설득력 있는 비즈니스 라이팅',
                'UX 리서치: 사용자 중심 디자인의 시작',
                '비즈니스 영어: 협상과 프레젠테이션 스킬',
                '게이미피케이션: 재미있는 학습 경험 만들기',
                '파이썬으로 시작하는 데이터 사이언스',
                '인플루언서 마케팅: 소셜 미디어 영향력 활용',
                '제로 트러스트 보안: 새로운 패러다임',
                'ESG 경영: 지속가능성을 통한 기업 가치 제고',
                '마인드풀니스: 집중력과 정확성 향상',
                '글로벌 비즈니스 에티켓: 문화적 민감성 기르기',
                '데이터 시각화: 인사이트 직관적 파악',
                '스토리텔링을 통한 효과적인 메시지 전달',
                '시나리오 플래닝: 불확실성 속 전략 수립',
                '고급 엑셀: 매크로와 VBA 활용'
            ],
            '분석적 사고': [10, 4, 3, 2, 2, 4, 1, 1, 3, 8, 6, 2, 3, 4, 8, 4, 3, 2, 2, 8, 2, 4, 3, 1, 1, 6, 2, 6, 6],
            '창의적 사고': [1, 10, 4, 2, 4, 3, 2, 1, 6, 1, 4, 2, 6, 2, 2, 6, 6, 3, 8, 3, 6, 2, 3, 3, 2, 4, 8, 6, 3],
            '유연성과 민첩성': [1, 4, 10, 2, 4, 2, 3, 2, 6, 1, 4, 2, 4, 3, 1, 1, 2, 3, 4, 1, 4, 2, 3, 3, 4, 1, 2, 6, 1],
            '동기부여': [0.5, 2, 3, 10, 6, 1, 4, 2, 6, 1, 1, 4, 1, 1, 1, 2, 1, 2, 6, 2, 3, 1, 2, 4, 2, 1, 3, 2, 1],
            '자기개발': [1, 2, 2, 6, 10, 2, 4, 3, 3, 1, 1, 2, 1, 1, 2, 3, 2, 3, 4, 3, 2, 2, 2, 6, 3, 2, 3, 2, 2],
            '기술력': [2, 1, 2, 0, 1, 10, 0, 0, 1, 3, 2, 1, 6, 3, 8, 0, 3, 1, 3, 8, 3, 8, 2, 0, 1, 6, 1, 2, 6],
            '섬세함': [0.5, 2, 1, 2, 2, 0.5, 10, 6, 4, 4, 2, 4, 6, 1, 1, 4, 6, 3, 2, 1, 3, 1, 2, 6, 6, 4, 4, 2, 2],
            '공감과 경청': [0, 3, 2, 2, 2, 0, 10, 10, 6, 1, 2, 6, 4, 1, 0, 3, 6, 6, 3, 0, 4, 1, 3, 4, 8, 1, 6, 2, 0],
            '리더십과 영향력': [2, 3, 4, 4, 3, 2, 6, 6, 10, 3, 4, 6, 2, 3, 1, 4, 2, 6, 3, 1, 4, 2, 6, 3, 4, 2, 6, 6, 1],
            '품질 관리': [1, 1, 3, 0.5, 1, 1, 0.5, 1, 2, 10, 2, 1, 3, 4, 2, 1, 2, 1, 1, 2, 1, 3, 3, 3, 1, 3, 1, 2, 4],
            '시스템 사고': [4, 4, 4, 1, 2, 4, 1, 1, 4, 6, 10, 3, 4, 6, 3, 1, 3, 1, 2, 3, 2, 4, 6, 1, 2, 4, 2, 8, 2],
            '인재 관리': [0, 1, 3, 3, 2, 0.5, 4, 4, 6, 2, 3, 10, 1, 1, 0, 1, 1, 2, 2, 0, 1, 1, 2, 2, 3, 1, 2, 2, 1],
            '고객 서비스': [1, 4, 2, 1, 1, 1, 4, 6, 2, 3, 2, 2, 10, 2, 1, 3, 8, 4, 3, 0, 6, 1, 3, 2, 4, 3, 4, 2, 1],
            '자원 관리 및 운영': [2, 1, 3, 1, 1, 2, 1, 1, 3, 6, 4, 3, 3, 10, 2, 1, 1, 1, 1, 1, 2, 3, 6, 1, 2, 3, 1, 4, 4],
            'AI 및 빅데이터': [6, 0.5, 1, 0, 1, 6, 0, 0, 0.5, 3, 2, 1, 4, 2, 10, 1, 2, 0, 2, 8, 3, 4, 1, 0, 0, 8, 1, 3, 4],
            '읽기,쓰기': [2, 1, 1, 2, 3, 2, 2, 3, 3, 2, 2, 3, 2, 2, 3, 10, 3, 6, 3, 3, 4, 2, 3, 2, 3, 4, 8, 3, 3],
            '사용자 경험': [0, 6, 3, 1, 1, 3, 2, 2, 1, 2, 1, 1, 10, 1, 2, 2, 10, 2, 8, 2, 6, 2, 2, 1, 2, 6, 3, 2, 2],
            '외국어': [0, 0, 0, 0, 1, 0, 1, 2, 1, 0, 0, 1, 1, 0, 0, 3, 0, 10, 1, 1, 1, 0, 1, 1, 6, 0, 2, 1, 0],
            '교육 및 멘토링': [0, 1, 1, 2, 3, 1, 2, 3, 3, 1, 1, 2, 1, 1, 1, 2, 1, 2, 10, 2, 1, 1, 1, 2, 2, 1, 3, 1, 1],
            '프로그래밍': [2, 0.5, 2, 0, 1, 4, 0, 0, 0, 2, 1, 0, 2, 1, 6, 0, 2, 0, 3, 10, 1, 4, 0, 0, 0, 4, 0, 1, 8],
            '마케팅 및 미디어': [1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 3, 6, 1, 2, 4, 4, 3, 4, 1, 10, 1, 3, 1, 3, 3, 6, 3, 1],
            '사이버 보안': [0, 0, 0.5, 0, 0.5, 3, 0, 0, 0, 1, 1, 0, 1, 1, 2, 0, 0, 0, 0, 2, 1, 10, 1, 0, 0, 1, 0, 1, 1],
            '환경 관리': [0, 1, 0.5, 0.5, 1, 2, 0.5, 0.5, 1, 2, 3, 1, 1, 8, 1, 1, 1, 0.5, 1, 1, 1, 1, 10, 1, 2, 1, 1, 3, 1],
            '지구력 및 정밀도': [1, 1, 3, 3, 3, 0.5, 1, 2, 2, 6, 1, 1, 2, 2, 2, 2, 3, 2, 3, 3, 2, 3, 2, 10, 2, 2, 2, 2, 4],
            'Globality': [0.5, 1, 1, 0.5, 2, 2, 2, 2, 2, 1, 2, 2, 2, 3, 1, 2, 2, 6, 2, 1, 4, 2, 4, 1, 10, 1, 3, 4, 1],
            '직관력': [3, 4, 2, 3, 3, 3, 6, 4, 4, 2, 6, 4, 4, 3, 4, 3, 6, 3, 4, 3, 4, 3, 4, 6, 4, 10, 4, 6, 4],
            '커뮤니케이션': [1, 3, 3, 2, 2, 1, 6, 8, 6, 2, 2, 4, 4, 2, 1, 8, 4, 8, 4, 1, 6, 2, 4, 3, 8, 3, 8, 3, 1],
            '스토리텔링': [1, 4, 1, 1, 1, 1, 4, 4, 4, 1, 2, 3, 4, 1, 2, 8, 4, 6, 6, 1, 8, 1, 3, 2, 4, 6, 10, 4, 1],
            'Biz통찰력': [6, 3, 3, 1, 2, 6, 2, 2, 4, 3, 6, 4, 4, 4, 4, 3, 3, 4, 2, 3, 4, 3, 6, 1, 4, 4, 3, 10, 2],
            'MS Office': [1, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 1, 2, 2, 4, 1, 2, 1, 3, 1, 1, 1, 1, 1, 6, 3, 1, 10]
        }
        return pd.DataFrame(data)
    
    # 교육 과정 추천
    st.header('교육 과정 추천')
    course_df = load_course_data()
    
    # 사용자가 선택한 희망 직무
    desired_job = st.selectbox('희망 직무 선택', df.columns[1:])
    
    # 역량 차이 계산
    skill_gaps = df[desired_job] - pd.Series(user_skills)
    skill_gaps = skill_gaps[skill_gaps > 0]  # 양수 값만 선택 (개선이 필요한 역량)
    
    # 상위 5개 개선 필요 역량
    top_5_gaps = skill_gaps.nlargest(5)
    
    st.subheader('개선이 필요한 상위 5개 역량:')
    st.write(top_5_gaps)
    
    # 교육 과정 점수 계산
    course_scores = pd.DataFrame()
    for skill in top_5_gaps.index:
        course_scores[skill] = course_df[skill] * top_5_gaps[skill]
    
    course_scores['Total Score'] = course_scores.sum(axis=1)
    recommended_courses = course_scores.nlargest(5, 'Total Score')
    
    st.subheader('추천 교육 과정 (상위 5개):')
    for i, (index, row) in enumerate(recommended_courses.iterrows(), 1):
        st.write(f"{i}. {course_df.loc[index, 'Course Name']} (점수: {row['Total Score']:.2f})")
    
    st.write("이 교육 과정들은 현재 역량과 희망 직무 사이의 격차를 줄이는 데 도움이 될 것입니다.")

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
