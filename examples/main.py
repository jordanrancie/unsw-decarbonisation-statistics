import altair as alt
import datapane as dp
from vega_datasets import data

df = data.iris()
columns = list(df.columns)
print(columns)


fig = (
    alt.Chart(df)
    .mark_point()
    .encode(x=alt.X("sepalLength", scale=alt.Scale(zero=False)), 
            y=alt.X("sepalWidth", scale=alt.Scale(zero=False)),
            color="species")
)

view = dp.Select(dp.Plot(fig, label="Plot"), dp.DataTable(df, label="Data"))
view

dp.save_report(view, "quickstart_report.html", open=True)