

# -*- coding: utf-8 -*-

# prompt: https://raw.githubusercontent.com/hpot/stat/main/2501kind.xlsx 이걸로 df생성

import pandas as pd
excel_url = 'https://raw.githubusercontent.com/hpot/stat/main/2501kind.xlsx'
df = pd.read_excel(excel_url)

# prompt: /content/drive/MyDrive/colab/유치원/2501kind.xlsx read show coulumns 0, 3, 18 remove row 0,1 1번컬럼 내용에 '교육청' 삭제 2번컬럼 내용에 '사립'포함하는 열삭제 renumbering column0의 이름을 지역으로 변경 column3의 이름을 설립유형으로 변경 column18의 이름을 총정원수로 변경print

#import pandas as pd
#file_path = '/content/drive/MyDrive/colab/유치원/2501kind.xlsx

# Select columns 0, 3, and 18
df = df.iloc[:, [0, 3, 18]]

# Remove rows 0 and 1
df = df.drop([0, 1])

# Remove '교육청' from column 0
df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.replace('교육청', '', regex=False)

# Remove rows where column 1 contains '사립'
df = df[~df.iloc[:, 1].astype(str).str.contains('사립', regex=False)]

# Renumber the index
df = df.reset_index(drop=True)

# Rename columns
df = df.rename(columns={df.columns[0]: '지역', df.columns[1]: '설립유형', df.columns[2]: '총정원'})

# prompt: 총정원수값 전부 int로 변환 df_kind 지역 groupby agg 공립유치원 count 총정원수 sum

# '총정원수' column to int
df['총정원'] = df['총정원'].astype(int)

# Group by '지역' and aggregate
df_kind  = df.groupby('지역').agg(
    공립유치원수=('설립유형', 'count'),  # Count '설립유형' column (which are all '공립' at this point)
    총정원=('총정원', 'sum')      # Sum '총정원수' column
).reset_index()

# prompt: df_kind DataFrame 사용: column0 값 전부 str로 변경 print

# Access the first column by its name
column_name = df_kind.columns[0]
# Convert the column to string type
df_kind[column_name] = df_kind[column_name].astype(str)

# prompt: https://raw.githubusercontent.com/hpot/stat/main/2501kind.xlsx 이걸로 df생성

import pandas as pd
excel_url = 'https://raw.githubusercontent.com/hpot/stat/main/pop345.xlsx'
df_pop = pd.read_excel(excel_url)

# prompt: /content/drive/MyDrive/colab/유치원/pop345.xlsx read print 2번열 이름을 '지역'으로 변경 4번열 이름을 '3~5세인구수'로 변경 2번 4번 열 제외하고 다른열 삭제 renumbering  후 0 1 2 행 삭제

#import pandas as pd
#file_path_pop = '/content/drive/MyDrive/colab/유치원/pop345.xlsx'
#df_pop = pd.read_excel(file_path_pop)

# Print initial column names for verification
#print("Initial column names:", df_pop.columns.tolist())

# Change the name of the 2nd column (index 1) to '지역'
df_pop = df_pop.rename(columns={df_pop.columns[1]: '지역'})

# Change the name of the 4th column (index 3) to '3~5세인구수'
df_pop = df_pop.rename(columns={df_pop.columns[3]: '3~5세인구수'})

# Keep only the columns named '지역' and '3~5세인구수'
df_pop = df_pop[['지역', '3~5세인구수']]

# Remove the first 3 rows (index 0, 1, and 2)
df_pop = df_pop.drop([0, 1, 2])

# prompt: df_kind 지역값 rstrip df_pop 지역값 rstrip

df_kind['지역'] = df_kind['지역'].str.rstrip()
df_pop['지역'] = df_pop['지역'].str.rstrip()

# prompt: df_kind df_pop merge remove column 0 1

import pandas as pd
# Merge the two dataframes on the '지역' column
merged_df = pd.merge(df_kind, df_pop, on='지역', how='inner')

# prompt: merged_df DataFrame 사용: 컬럼추가 '공립유치원 미취원율' 값은 1,0- (총정원수/3~5세인구수) 공립유치원 미취원율로 내림차순 정렬 3~5세인구수값 전부 int로 변경 print

# Replace commas in the '3~5세인구수' column and convert to integer
merged_df['3~5세인구수'] = merged_df['3~5세인구수'].str.replace(',', '').astype(int)

# Calculate the '공립유치원 미취원율'
merged_df['공립유치원 미취원율'] = 1.0 - (merged_df['총정원'] / merged_df['3~5세인구수'])

# Sort the DataFrame by '공립유치원 미취원율' in descending order
merged_df = merged_df.sort_values(by='공립유치원 미취원율', ascending=False)

# prompt: merged_df DataFrame 사용: 지역명 공립유치원수 총정원수 3~5세인구수 공립유치원 미취원율 을 제외한 모든 열 삭제print

# Drop all columns except for the specified ones
columns_to_keep = ['지역', '공립유치원수', '총정원', '3~5세인구수', '공립유치원 미취원율']
merged_df = merged_df[columns_to_keep]

# prompt: merged_df 깊은 복사 into final_df

final_df = merged_df.copy(deep=True)

# prompt: final_df DataFrame 사용: 지역과 공립유치원 미취원율 제외한 모든 행 삭제 into rr_df 공립유치원 미취원율 오름차순정렬 print

# Select the columns '지역' and '공립유치원 미취원율' and assign to rr_df
rr_df = final_df[['지역', '공립유치원 미취원율']]

# Sort rr_df by '공립유치원 미취원율' in ascending order
rr_df = rr_df.sort_values(by='공립유치원 미취원율')

# prompt: rr_df DataFrame 사용: 공립유치원 미취원율 값 ×100 후.2f round print

# Multiply the column by 100 and round to 2 decimal places
rr_df['공립유치원 미취원율'] = (rr_df['공립유치원 미취원율'] * 100).round(2)

# prompt: rr_df col1값 추출 후 리스트화 into region col2값 추출후 리스트화 into rate print

region = rr_df.iloc[:, 0].tolist()
rate = rr_df.iloc[:, 1].tolist()

# prompt: rate값 전부 100.0-rate 후 .2f round into c

c = [round(100.0 - r, 2) for r in rate]

# prompt: final_df 에서 유치원 미취원율열 삭제 후 into final2_df

final2_df = final_df.drop(columns=['공립유치원 미취원율'])

# prompt: rr_df를 series로 변경

rr_series = rr_df.set_index('지역')['공립유치원 미취원율']
rr_series

# %%
#$ import dash 등 필요한 라이브러리 임포트

import dash
from dash import dcc
from dash import html
from dash import dash_table, Input, Output, callback, no_update

import pandas as pd
import plotly.express as px

# 데이터프레임 및 Series가 이미 준비되었다고 가정합니다.
# (이전에 엑셀 파일을 읽고 처리하여 rr_series를 생성하여 rr_series를 생성)
# 예: rr_series = rr_df.set_index('지역')['공립유치원 미취원율']

# 데이터를 애니메이션 프레임으로 변환 (색상 정보 로직 제거)
data_frames = []
num_steps_per_bar = 5 # 한 바가 채워지는 단계 수
num_bars = len(rr_series)
# 프레임 수는 동일
num_frames = num_bars * (num_steps_per_bar + 1)

frame_counter = 0
# 마지막 바부터 거꾸로 채워지도록 순회
for bar_index in range(num_bars - 1, -1, -1):
    for step in range(num_steps_per_bar + 1):
        current_frame_data = {}
        current_frame_texts = {} # <-- 텍스트 값을 위한 딕셔너리 추가

        for i in range(num_bars):
            item_name = rr_series.index[i]
            item_value = rr_series.iloc[i]

            if i > bar_index:
                # 현재 채워지고 있는 바보다 아래 있는 바 (이미 완료된 바)
                current_frame_data[item_name] = item_value
                current_frame_texts[item_name] = f"{item_value:.2f}%" # <-- 완료된 바의 텍스트
            elif i == bar_index:
                # 현재 채워지고 있는 바
                current_value = item_value * step / num_steps_per_bar
                current_frame_data[item_name] = current_value
                # 진행 중인 바의 텍스트 (값이 변경됨)
                if step == num_steps_per_bar:
                     current_frame_texts[item_name] = f"{current_value:.2f}%" # <-- 완료 시 텍스트
                else:
                     current_frame_texts[item_name] = f"{current_value:.2f}%" # <-- 진행 중 텍스트
            else:
                # 현재 채워지고 있는 바보다 위에 있는 바 (아직 시작 안 함)
                current_frame_data[item_name] = 0
                current_frame_texts[item_name] = "" # <-- 시작 전 바의 텍스트는 비워둠


        df_current_step = pd.DataFrame({
            '항목': list(current_frame_data.keys()),
            '값': list(current_frame_data.values()),
            '프레임': frame_counter,
        })
        data_frames.append(df_current_step)
        frame_counter += 1

animated_df = pd.concat(data_frames)


# 가로 막대 그래프 생성
fig = px.bar(animated_df,
             x='값',
             y='항목',
             orientation='h',
             animation_frame='프레임',
             range_x=[0, 100],
             range_y=[-0.5, num_bars - 0.5],
             color='값',  # '값' 컬럼에 따라 색상 매핑 (수정)
             color_continuous_scale=
              [px.colors.qualitative.Plotly[1],
               px.colors.qualitative.Plotly[0]],

             hover_data={'값': True,
                         '항목': True,
                         '프레임': False,
              },





)

fig.update_yaxes(categoryorder='array', categoryarray=rr_series.index, automargin=True)

fixed_animation_speed = 50

# 텍스트 템플릿과 위치는 그대로 유지
# marker_color는 px.bar의 color 인자로 대체되므로 여기서는 필요 없습니다.
fig.update_traces(
    marker_cornerradius=3,
    texttemplate='%{x}%', # <-- text_auto를 사용하지 않으므로 texttemplate는 필요 없을 수 있습니다.
    textposition='inside',
    textfont=dict(color='white',),

)

# Play button arguments for the animation
# 이 설정을 자동 트리거에도 사용합니다.
play_button_args = [None, {
    "frame": {"duration": fixed_animation_speed, "redraw": False},
    "fromcurrent": True,
    "transition": {"duration": fixed_animation_speed, "easing": "linear"}
}]


# Update layout with animation controls and axis ranges
fig.update_layout(
    xaxis=dict(fixedrange=True,
               title=rr_series.name,

               ), # <-- x축 제목 설정
    yaxis=dict(fixedrange=True,
               title=rr_series.index.name
               ), # <-- y축 제목 설정

    updatemenus=[
        {
            "buttons": [
                {
                    "args": play_button_args,
                    "label": "Play",
                    "method": "animate"
                },
                 {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ],
    height=max(660, num_bars * 30),
    showlegend=False, # 색상 범례 (이산형) 숨김 유지
    coloraxis_showscale=False, # <-- 색상 바 (연속형) 숨김 유지
    hoverlabel=dict(
        bgcolor='white',
        font_size=13,
        font_color='black',
    ),
    # uniformtext 관련 설정은 필요에 따라 제거하거나 조정합니다.
    # font 설정은 축 라벨 등 다른 텍스트에 영향을 줍니다.
    # font=dict(size=12) # <-- 전체 폰트 크기 설정은 여기에 두거나 제거합니다.

)


# Dash 앱 초기화
app = dash.Dash(__name__)
server = app.server
app.title = '지역별 공립유치원 미취원율'


# 앱 레이아웃 정의
app.layout = html.Div([
    html.H1("지역별 공립유치원 미취원율"), # <-- H1 값 변경
    dcc.Graph(
        id='animated-bar-chart',
        figure=fig,
    ),
    # 애니메이션 자동 시작을 위한 Interval 컴포넌트
    dcc.Interval(
        id='animation-interval',
        interval=2000,  # 페이지 로드 후 1초 뒤에 첫 번째 트리거
        n_intervals=0,  # 초기 값
        max_intervals=1 # 한 번만 실행되도록 설정
    ),
    html.Div(style={'height': '30px'}),
    dash_table.DataTable(data=rr_df.to_dict('records'),
                         page_size=17,
                         id='dt1',
                         sort_action='native',
    ),
    html.Div(style={'height': '30px'}),
    dash_table.DataTable(data=final2_df.to_dict('records'),
                         page_size=17,
                         id='dt2',
                         sort_action='native'
    ),

    # clientside_callback의 Output을 위한 더미 컴포넌트
    html.Div(id='dummy-output', style={'display': 'none'})


])

# 클라이언트 사이드 콜백을 사용하여 로드 후 애니메이션 시작
# 이 콜백 로직은 자동 시작을 위해 필요합니다.
# Plotly.animate 호출 시 애니메이션 설정을 함께 전달합니다.
app.clientside_callback(
        """
            function(n_intervals) {
                // n_intervals 값이 0보다 크면 (Interval이 한 번이라도 트리거되면) 실행
                if (n_intervals > 0) {
                    const graphDiv = document.querySelector('.js-plotly-plot');
                    // Play 버튼의 애니메이션 설정 객체를 정의합니다.
                    const animationConfig = {
                        frame: { duration: """ + str(fixed_animation_speed) + """, redraw: false },
                        fromcurrent: true,
                        transition: { duration: """ + str(fixed_animation_speed) + """, easing: "linear" }
                    };
                    // Plotly.animate 함수에 설정 객체를 인자로 전달합니다.
                    Plotly.animate(graphDiv, null, animationConfig);
                }
                return window.dash_clientside.no_update; // 더미 출력은 업데이트하지 않음
            }
        """,
    Output('dummy-output', 'children'),
    Input('animation-interval', 'n_intervals'),
    prevent_initial_call=True
)

# 앱 실행
if __name__ == '__main__':
    app.run(debug=False)
