import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

# 예시 데이터
trend_data = pd.DataFrame(
    {
        "트렌드": ["인스타그램 릴스", "틱톡 마케팅", "AI 마케팅", "메타버스 광고"],
        "검색량": np.random.randint(1000, 5000, 4),
    }
)

fig = px.bar(trend_data, x="트렌드", y="검색량", title="실시간 트렌드")

app.layout = html.Div(
    [
        html.H1("Mr. Mark AI 대시보드"),
        dcc.Graph(figure=fig),
        html.Div("품질지표, AI 예측, 실시간 데이터 등 다양한 시각화 추가 가능"),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
