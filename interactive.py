import plotly.express as px
df = px.data.gapminder()
COL = {"Africa":"#D55E00","Americas":"#009E73","Asia":"#CC79A7","Europe":"#0072B2","Oceania":"#E69F00"}
fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
    size="pop", color="continent", hover_name="country", log_x=True, size_max=55,
    range_x=[200,70000], range_y=[22,87], color_discrete_map=COL,
    labels={"gdpPercap":"GDP per capita (international $, log scale)","lifeExp":"Life expectancy at birth (years)","pop":"Population","continent":"Continent"},
    title="Health and wealth of nations, 1952-2007 (press play, hover for country detail)")
fig.update_layout(template="plotly_white", font=dict(family="Arial", size=13), title_font_size=18, height=650,
    legend=dict(orientation="h", y=-0.2), margin=dict(b=140))
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
fig.update_traces(marker=dict(line=dict(width=0.6, color="white"), opacity=0.8))
fig.write_html("interactive_health_wealth.html", include_plotlyjs=True, full_html=True)
print("ok")
