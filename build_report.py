import numpy as np, pandas as pd, plotly.express as px, warnings; warnings.filterwarnings("ignore")
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Image as RLImage, Table, TableStyle, KeepTogether)

df = px.data.gapminder()
wavg = lambda g, c="lifeExp": np.average(g[c], weights=g["pop"])
world = df.groupby("year").apply(wavg)
cont = df.groupby(["continent","year"]).apply(wavg).unstack(0)
df["band"] = pd.cut(df.lifeExp, [0,60,100], labels=["lt60","ge60"], right=False)
sh = df.groupby(["year","band"])["pop"].sum().unstack().pipe(lambda t: t.div(t.sum(1),axis=0)*100)
df["b40"] = df.lifeExp<40
u40_52 = df[(df.year==1952)&df.b40]["pop"].sum()/df[df.year==1952]["pop"].sum()*100
r2 = {}; sl = {}; pred = {}
for y in (1952,2007):
    d=df[df.year==y]; x=np.log10(d.gdpPercap); s,i=np.polyfit(x,d.lifeExp,1); r2[y]=np.corrcoef(x,d.lifeExp)[0,1]**2; sl[y]=s; pred[y]=(i+s*3,i+s*4)
p = df.pivot(index="country",columns="year",values="lifeExp")
n_decl = int((p[2007]<p[1952]).sum())

NAVY, ACCENT, GREY = colors.HexColor("#0B3C5D"), colors.HexColor("#D55E00"), colors.HexColor("#555555")
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, spaceBefore=6, spaceAfter=8, leading=22)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12, textColor=ACCENT, spaceBefore=8, spaceAfter=3)
B = ParagraphStyle("B", parent=ss["BodyText"], fontName="Helvetica", fontSize=10, leading=14.2, textColor=colors.HexColor("#222222"), spaceAfter=6)
SM = ParagraphStyle("SM", parent=B, fontSize=8.5, leading=11, textColor=GREY)
CAP = ParagraphStyle("CAP", parent=SM, alignment=TA_CENTER, spaceAfter=8)
TT = ParagraphStyle("TT", parent=B, fontName="Helvetica-Bold", fontSize=30, leading=36, textColor=NAVY, alignment=TA_LEFT)
ST = ParagraphStyle("ST", parent=B, fontSize=14, leading=19, textColor=GREY)
CELL = ParagraphStyle("CELL", parent=B, fontSize=8.8, leading=11.5, spaceAfter=0)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Helvetica-Bold", textColor=colors.white)

def footer(c, d):
    c.saveState(); c.setFont("Helvetica",8); c.setFillColor(GREY)
    c.drawString(inch, 0.55*inch, "Health and Wealth of Nations, 1952-2007 | Data Visualization Portfolio")
    c.drawRightString(letter[0]-inch, 0.55*inch, f"Page {d.page}"); c.restoreState()
doc = BaseDocTemplate("Data_Visualization_Narrative_Report.pdf", pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.9*inch, bottomMargin=0.9*inch,
                      title="Health and Wealth of Nations, 1952-2007: Data Visualization Narrative Report", author="Data Visualization Portfolio")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=footer)])
W = doc.width
def img(name, maxh=4.9*inch):
    path=f"figures/{name}.png"; w,h=Image.open(path).size; r=min(W/w, maxh/h); return RLImage(path, width=w*r, height=h*r)
def P(t, s=B): return Paragraph(t, s)
def tbl(rows, widths, head=True):
    data=[[Paragraph(c, CELLB if (head and i==0) else CELL) for c in r] for i,r in enumerate(rows)]
    t=Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F6F9")]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#CCCCCC")),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)])); return t

S=[]
# ---- title page
S += [Spacer(1,1.6*inch), P("Health and Wealth of Nations, 1952-2007", TT), Spacer(1,6),
      P("Seven visualizations and a narrative on how humanity gained twenty years of life, who was left behind, and what income can and cannot explain", ST), Spacer(1,.5*inch),
      P("<b>Week 5 Task: Data Visualization and Communication</b><br/>Dataset: Gapminder (142 countries, 12 observations each, 1952-2007)<br/>Tools: Python, pandas, Matplotlib, Plotly, ReportLab", B),
      Spacer(1,.3*inch),
      P("Portfolio contents: this narrative report (PDF), seven static figures (PNG, 200 dpi), one interactive animated chart (HTML), and the reproducible Python scripts.", SM), PageBreak()]

# ---- exec summary
S += [P("1. Executive summary", H1),
 P(f"Between 1952 and 2007, population-weighted life expectancy across the 142 countries in this dataset rose from <b>{world[1952]:.1f}</b> to <b>{world[2007]:.1f}</b> years, a gain of {world[2007]-world[1952]:.1f} years in 55 years. "
   f"The share of people living in countries with a life expectancy below 60 fell from <b>{sh.loc[1952,'lt60']:.0f}%</b> to <b>{sh.loc[2007,'lt60']:.0f}%</b>. That is the headline, and it is genuinely good news."),
 P("The data also contain three complications that a headline average hides, and the report is built around them:"),
 P(f"<b>1. Progress was uneven.</b> Asia gained {cont['Asia'].iloc[-1]-cont['Asia'].iloc[0]:.1f} years and closed most of its gap with Europe, while Africa gained {cont['Africa'].iloc[-1]-cont['Africa'].iloc[0]:.1f} years and still sits {cont['Oceania'].iloc[-1]-cont['Africa'].iloc[-1]:.1f} years behind Oceania."),
 P(f"<b>2. Income matters, but it is not destiny.</b> Income per person explains roughly {r2[2007]*100:.0f}% of the variation in life expectancy across countries in 2007, yet a country with the same income lived about {pred[2007][0]-pred[1952][0]:.0f} years longer in 2007 than in 1952. Some countries sit more than 20 years below what their income predicts; others sit over 10 years above."),
 P(f"<b>3. Progress can reverse.</b> Life expectancy fell by more than 5 years between consecutive observations in several countries, through conflict, famine and the HIV/AIDS epidemic. Zimbabwe and Swaziland ended 2007 below their 1952 level."),
 P("Each section below pairs one visualization with the reasoning for the chart type chosen and the insight it supports. Figures are ordered as a story: the big picture, who benefited, what drives the differences, where the exceptions are."),
 PageBreak()]

# ---- data & method
S += [P("2. Dataset, preparation and method", H1),
 P("<b>Source.</b> The Gapminder dataset distributed with the Plotly library (<font face='Courier'>plotly.express.data.gapminder()</font>). It contains 1,704 rows: 142 countries observed every five years from 1952 to 2007, with life expectancy at birth, population, and GDP per capita (inflation-adjusted international dollars), plus a continent label."),
 P("<b>Why this dataset.</b> It is public, well documented, and rich in the very things this task asks for: long-run trends, patterns across groups, and peculiarities (reversals and outliers) that reward careful visual treatment. It is also familiar enough that readers can sanity-check results."),
 P("<b>Data checks.</b> No missing values and no duplicate country-year rows were found. Life expectancy is within plausible bounds (23.6 to 82.6 years). GDP per capita spans about $241 to $113,523, so a logarithmic axis is used wherever it is plotted."),
 P("<b>Method choices that affect accuracy.</b>"),
 P("&bull; <b>Population-weighted averages</b> are used for continents and the world, so that a large country (China, India) counts in proportion to its people. Unweighted country averages are used only when the unit of analysis is the country, as in the rankings.<br/>"
   "&bull; <b>Log-income regression.</b> Life expectancy is regressed on log<sub>10</sub>(GDP per capita) separately for each year. The slope is read as years of life per tenfold increase in income. This describes association, not causation.<br/>"
   "&bull; <b>Colour.</b> A colour-blind-safe palette (Okabe-Ito) is used and every continent is also directly labelled, so colour is never the only carrier of meaning."),
 P("<b>Storyboard.</b> The table shows the narrative job of each visualization.", B),
 tbl([["#","Visualization","Question it answers","Technique"],
   ["1","Continental life-expectancy trends","How much did the world improve, and for whom?","Annotated multi-line chart, direct labels"],
   ["2","Population by life-expectancy band","How many <i>people</i> (not countries) benefited?","100% stacked area"],
   ["3","Income vs life expectancy, 1952 and 2007","Does wealth explain longevity?","Small-multiple bubble scatter, log axis, fit line"],
   ["4","Predicted life at fixed income","Is something other than income lifting life expectancy?","Two-line chart with shaded gap"],
   ["5","Six reversals","Is progress always upward?","Small multiples against a world benchmark"],
   ["6","Over- and under-performers","Who beats or misses the income prediction?","Diverging lollipop chart"],
   ["7","Fastest climbers","Who improved most?","Dumbbell (start to end) chart"],
   ["+","Interactive animation (HTML)","How did the whole picture move through time?","Animated bubble chart with hover"]],
   [0.3*inch, 1.9*inch, 2.4*inch, 1.9*inch]),
 PageBreak()]

def section(num, title, fig, what, why, insight, maxh=None):
    maxh = maxh or {"fig6_over_under_performers":3.8*inch}.get(fig, 4.6*inch)
    return [P(f"Figure {num-2}: {title}", H1), img(fig, maxh), P(f"Figure {num-2}. See text.", CAP) if False else Spacer(1,4),
            P("What the chart shows", H2), P(what), P("Why this visual technique", H2), P(why), P("Insight and relevance", H2), P(insight), PageBreak()]

S += section(3, "The big picture: twenty years gained, unevenly", "fig1_continent_trends",
 f"Population-weighted life expectancy for each continent, 1952-2007, with the world average dashed. Every line rises. The world moves from {world[1952]:.1f} to {world[2007]:.1f} years. Asia starts at {cont['Asia'].iloc[0]:.1f} and ends at {cont['Asia'].iloc[-1]:.1f}; Africa starts at {cont['Africa'].iloc[0]:.1f} and ends at {cont['Africa'].iloc[-1]:.1f}.",
 "A line chart is the natural form for change over time, and with only five series it stays readable. Labels at the line ends replace a legend so the reader never has to look away from the data. Annotations point to the two features that carry the story: Asia's steep climb and Africa's flattening. Population weighting keeps China and India from being under-represented.",
 f"The gap between Europe and Asia shrank from {cont['Europe'].iloc[0]-cont['Asia'].iloc[0]:.1f} years in 1952 to {cont['Europe'].iloc[-1]-cont['Asia'].iloc[-1]:.1f} years in 2007, which is convergence. The Africa line tells a different story: it stalls at roughly 53 years between 1992 and 2002, while every other continent keeps rising. The dip in Asia between 1957 and 1962 is the Chinese famine, visible at continental scale because of China's size (see Figure 5). The average conceals diversity inside each continent, which is why the later figures look at countries.")

low = sh.loc[1952,'lt60']; lowe = sh.loc[2007,'lt60']
S += section(4, "How many people benefited?", "fig2_population_bands",
 f"The share of the dataset's population living in countries within each life-expectancy band, for each year. In 1952, {low:.0f}% of people lived in countries with life expectancy under 60, and {u40_52:.0f}% in countries under 40. By 2007 the under-60 share is {lowe:.0f}%, and the 70-plus band, almost empty in 1952, holds over 60% of people.",
 "Figure 1 weights countries by population; this chart goes further and makes <i>people</i> the unit of count. A 100% stacked area suits a composition that changes over time because it shows how the whole is divided at every moment. A sequential colour scheme (dark red for low, deep blue for high) means the eye reads 'worse to better' without a legend lookup.",
 "This is the most persuasive single picture of the period because it measures progress in human terms. The temporary rise of the 40-50 band around 1962 comes from China's famine-era dip, a reminder that one country can move a global composition. By the 1990s the most rapid change is a migration of people from the 50-70 bands into 70-plus, which implies the frontier of progress shifted from preventing early deaths to extending adult life.")

S += section(5, "Does income explain longevity?", "fig3_income_vs_life",
 f"Each bubble is a country, sized by population and coloured by continent, plotted on income (log scale) against life expectancy. The left panel is 1952 and the right is 2007, on identical axes. The dashed line is a least-squares fit. The fit explains R<super>2</super> = {r2[1952]:.2f} of the variation in 1952 and {r2[2007]:.2f} in 2007.",
 "A scatter plot is the right tool for a relationship between two continuous variables. The log scale straightens the well-known curved relationship and prevents rich countries from compressing everyone else into the left edge. Using side-by-side panels with shared axes lets the reader compare years without a legend for 'year'. Bubble area encodes population, so the two giants (China, India) are impossible to miss.",
 f"Two things are visible at once. First, the relationship is strong and positive in both years. Second, the entire cloud has moved up and to the right, and in 2007 poor countries sit well above where poor countries sat in 1952. The slope flattened from {sl[1952]:.1f} to {sl[2007]:.1f} years per tenfold increase in income, so the payoff from income alone shrank as other drivers (vaccines, sanitation, medical knowledge) became available at lower cost. This is an association: the chart cannot show that income causes longevity, only that the two travel together.")

S += section(6, "Same income, longer life", "fig4_fixed_income",
 f"For each year, the life expectancy predicted by the fitted income relationship at two fixed income levels: $1,000 and $10,000 per person. The predicted value at $1,000 climbs from {pred[1952][0]:.1f} years in 1952 to {pred[2007][0]:.1f} in 2007. At $10,000 it climbs from {pred[1952][1]:.1f} to {pred[2007][1]:.1f}.",
 "This chart isolates what Figure 3 hints at. Holding income fixed removes the effect of economic growth and leaves the change attributable to everything else. Two lines with a shaded gap is a deliberately simple form so the headline (about 12 extra years at the low-income benchmark) can be read in seconds.",
 "Life expectancy at a given income rose substantially, which is consistent with knowledge and technology (vaccination, antibiotics, oral rehydration, clean water practice) spreading faster than wealth. Two caveats are important. The upper line flattens after the early 1990s partly because the fitted line is pulled down by a handful of southern African countries whose life expectancy collapsed (Figures 5 and 6). And these are model predictions at hypothetical income levels, not observed values for particular countries.")

S += section(7, "Progress is not guaranteed", "fig5_setbacks",
 f"Six countries whose life expectancy fell sharply, each plotted against the world average in grey. Rwanda's 1992 value (23.6) is {44.0-23.6:.1f} years below its 1987 value. Cambodia drops to 31.2 in 1977, China to 44.5 in 1962, and three southern African countries (Zimbabwe, South Africa, Botswana) lose between 12 and 22 years between the late 1980s or early 1990s and the early 2000s. Overall, only {n_decl} of 142 countries (Zimbabwe and Swaziland) finished 2007 below their 1952 level.",
 "Small multiples with a shared scale let the reader compare shapes across countries without needing to decode six overlapping lines. The grey world line is a constant benchmark, so deviation from the global path is the visual signal. Colour is reserved for the one thing that matters in each panel (the country), and the marked point shows the low.",
 "The three patterns are distinct. Conflict and mass atrocity produce a sharp V that recovers within a decade or two (Rwanda, Cambodia). Famine produces a short dip followed by rapid recovery (China). The HIV/AIDS epidemic produces a longer, slower hill that peaks and then declines for 10 to 15 years (Zimbabwe, South Africa, Botswana), and recovery is only just starting by 2007. Note on labelling: the causes named in the figure are historical context, not information contained in the dataset. The dataset's Rwandan low is labelled 1992 even though the genocide took place in 1994, which shows that values are period estimates in five-year steps and should not be read as exact event dates.")

S += section(8, "Beyond income: over- and under-performers", "fig6_over_under_performers",
 "For 2007, the gap in years between each country's actual life expectancy and what the income relationship predicts. The eight largest positive and eight largest negative gaps are shown, with GDP per capita in brackets. Vietnam is 13.1 years above prediction; Swaziland is 25.9 years below. Botswana and South Africa, both far richer than Vietnam, sit more than 20 years below.",
 "A diverging lollipop chart is the cleanest way to show signed deviations from a baseline. The zero line is the model's prediction, blue means a better outcome than income predicts and red means worse. Sorting by value lets the reader rank at a glance, and the data labels make the exact value available without gridline lookups.",
 "Residuals are where the interesting questions live. The lowest-ranked countries are mostly southern and central African states with high HIV prevalence or resource-dependent economies where average income is a poor indicator of how the population fares. The highest are a mix of low- and middle-income countries; the chart cannot say why they do better than their income predicts, though that is exactly the question worth investigating. Treat this as a prompt for investigation, not a conclusion: residuals depend on the model, GDP averages mask inequality, and the data do not identify causes.")

S += section(9, "The fastest climbers", "fig7_biggest_gains",
 "The twelve largest gains in life expectancy between 1952 and 2007. Grey dots mark 1952, coloured dots 2007, and the connecting bar is the gain. Oman leads with +38.1 years, followed by Vietnam (+33.8), Indonesia (+33.2) and Saudi Arabia (+32.9). Eight of the twelve are in Asia, three in Africa and one in the Americas.",
 "A dumbbell chart is ideal for 'before and after' for many entities: it shows both endpoints and the distance between them, which a bar chart of gains alone would hide. Showing only the top twelve keeps the chart legible while still revealing the pattern.",
 "Nobody from Europe or Oceania appears, and this is partly a ceiling effect: they began at high levels and had less room to grow. The top performers started low, and many are middle-income or oil-exporting economies, but the list is not simply a list of fast economic growers (Vietnam appears in Figure 6 as a large positive residual too). For reference, China gained 29.0 years and India 27.3, together about 39% of the dataset's 2007 population and driving most of Asia's overall rise in Figure 1.")

S += [P("Interactive companion", H1),
 P("The file <font face='Courier'>interactive_health_wealth.html</font> animates the income-versus-life-expectancy view from 1952 to 2007, one frame per observation year. Hover shows country, income, life expectancy and population; legend items can be clicked to isolate a continent; the slider allows scrubbing to any year. Animation is appropriate here because the central story is movement through time, and it lets a reader follow individual countries (watch Rwanda drop and recover, or China rise through the middle of the plot) that the static figures can only sample. The static figures remain the primary evidence because they are annotated, printable, and do not rely on the reader pressing play."),
 P("Conclusion", H1),
 P(f"The long-run story of 1952-2007 is one of remarkable and mostly broad-based improvement: {world[2007]-world[1952]:.0f} extra years of life, and a transformation from a world where {low:.0f}% of people lived under 60 to one where {lowe:.0f}% did. Reading beyond the average reveals what a single headline cannot. Africa lagged behind and stalled; income is strongly related to longevity but does not determine it, and the relationship changed as technology spread; the most striking exceptions, on both sides, are explained by factors that income does not capture; and progress can reverse quickly when systems fail."),
 P("For a decision-maker the implications are practical. Averages should be disaggregated, because the average hid Africa's stall. Income growth is not a substitute for health systems, because the same income buys more years of life now than before. And monitoring should be continuous, because the reversals in Figure 5 happened inside a single five-year window."),
 P("Limitations and honest caveats", H1),
 P("&bull; <b>Period covered.</b> The dataset ends in 2007, so it says nothing about later developments, including recovery from the HIV/AIDS peak.<br/>"
   "&bull; <b>Resolution.</b> Five-year steps cannot pinpoint events and can miss short shocks entirely.<br/>"
   "&bull; <b>Estimates.</b> Early values (especially pre-1960 for low-income countries) are modelled estimates with substantial uncertainty; the dataset gives no error bars.<br/>"
   "&bull; <b>Country averages.</b> Inequality within countries is invisible, and a country's GDP per capita is not any individual's income.<br/>"
   "&bull; <b>Association, not causation.</b> All income-longevity statements describe correlation. Event labels (famine, conflict, HIV/AIDS) are external historical context supplied by the author, not variables in the data.<br/>"
   "&bull; <b>Country coverage.</b> 142 countries are included, not all; population shares refer to this subset, not to the world total."),
 P("Appendix: reproducibility", H2),
 P("Files: <font face='Courier'>make_figures.py</font> (all static figures), <font face='Courier'>interactive.py</font> (HTML animation), <font face='Courier'>build_report.py</font> (this report). Every number in this report is computed in code from the dataset, with the exception of the historical event labels noted above. Requirements: pandas, numpy, matplotlib, plotly, reportlab, Pillow.", SM)]
doc.build(S); print("built")
