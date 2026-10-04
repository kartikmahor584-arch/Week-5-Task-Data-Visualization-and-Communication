import plotly.express as px, pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import warnings; warnings.filterwarnings("ignore")

df = px.data.gapminder()
COL = {"Africa":"#D55E00","Americas":"#009E73","Asia":"#CC79A7","Europe":"#0072B2","Oceania":"#E69F00"}
INK, GRID = "#222222", "#E6E6E6"
plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False,
    "axes.edgecolor":"#888","axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
    "axes.titleweight":"bold","axes.titlesize":14,"axes.titlelocation":"left","figure.dpi":100,"savefig.dpi":200,
    "axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,"axes.axisbelow":True})
SRC = "Source: Gapminder (via plotly.express.data.gapminder), 142 countries, 1952-2007"
def foot(fig, extra=""):
    fig.text(0.01, 0.01, SRC + extra, fontsize=8, color="#666")
def save(fig, name): fig.savefig(f"figures/{name}.png", bbox_inches="tight", facecolor="white"); plt.close(fig)
def wavg(g, c="lifeExp"): return np.average(g[c], weights=g["pop"])

# ---------- Fig 1: world + continents over time
c = df.groupby(["continent","year"]).apply(wavg).unstack(0)
world = df.groupby("year").apply(wavg)
fig, ax = plt.subplots(figsize=(11,6.2))
for k in c.columns:
    ax.plot(c.index, c[k], color=COL[k], lw=2.6, marker="o", ms=4)
    ax.text(2008.5, c[k].iloc[-1], f"{k}  {c[k].iloc[-1]:.1f}", color=COL[k], va="center", fontweight="bold", fontsize=11)
ax.plot(world.index, world, color="#444", lw=2, ls="--")
ax.text(2008.5, world.iloc[-1]-2.2, f"World  {world.iloc[-1]:.1f}", color="#444", va="center", fontweight="bold", fontsize=11)
ax.text(1951, c["Asia"].iloc[0], f"{c['Asia'].iloc[0]:.1f}", color=COL["Asia"], fontsize=10, ha="right", va="center", fontweight="bold")
ax.text(1951, c["Africa"].iloc[0], f"{c['Africa'].iloc[0]:.1f}", color=COL["Africa"], fontsize=10, ha="right", va="center", fontweight="bold")
ax.set_xlim(1945, 2022); ax.set_xticks(range(1950,2010,10)); ax.set_ylim(34, 84)
ax.set_xlabel("Year"); ax.set_ylabel("Life expectancy at birth (years, population-weighted)")
ax.set_title("The world gained 20 years of life in half a century, but not evenly")
ax.annotate("Asia gained 26.5 years,\nthe largest continental gain", xy=(1990, c.loc[1992,"Asia"]), xytext=(1953, 77),
            arrowprops=dict(arrowstyle="->", color=COL["Asia"]), color=COL["Asia"], fontsize=10)
ax.annotate("Africa's curve flattens\nfrom the 1990s", xy=(2002, c.loc[2002,"Africa"]), xytext=(1975, 41),
            arrowprops=dict(arrowstyle="->", color=COL["Africa"]), color=COL["Africa"], fontsize=10)
foot(fig); save(fig, "fig1_continent_trends")

# ---------- Fig 2: stacked area, share of world population by life-expectancy band
bins = [0,40,50,60,70,100]; labels = ["Under 40","40-50","50-60","60-70","70+"]
df["band"] = pd.cut(df.lifeExp, bins=bins, labels=labels, right=False)
sh = df.groupby(["year","band"])["pop"].sum().unstack().pipe(lambda t: t.div(t.sum(1), axis=0)*100)
pal = ["#7F1D1D","#D55E00","#E9A94B","#7FB8D8","#0B5394"]
fig, ax = plt.subplots(figsize=(11,6.2))
ax.stackplot(sh.index, [sh[l] for l in labels], labels=labels, colors=pal, alpha=.95)
ax.set_xlim(1952,2007); ax.set_ylim(0,100); ax.grid(False)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v:.0f}%"))
ax.set_xlabel("Year"); ax.set_ylabel("Share of world population (of the 142 countries)")
ax.set_title("In 1952, most people lived where life expectancy was under 60; by 2007 few did")
low52 = sh.loc[1952, ["Under 40","40-50","50-60"]].sum(); low07 = sh.loc[2007, ["Under 40","40-50","50-60"]].sum()
ax.text(1953, 3, f"Under 60 in 1952: {low52:.0f}% of people", color="white", fontweight="bold", fontsize=11)
ax.text(1983, 3, f"Under 60 in 2007: {low07:.0f}%", color="white", fontweight="bold", fontsize=11)
ax.legend(title="Life expectancy", loc="center left", bbox_to_anchor=(1.01,.5), frameon=False)
foot(fig); save(fig, "fig2_population_bands")

# ---------- Fig 3: Preston curve 1952 vs 2007
fig, axes = plt.subplots(1,2, figsize=(13,6), sharey=True)
for ax, y in zip(axes, (1952,2007)):
    d = df[df.year==y]
    ax.scatter(d.gdpPercap, d.lifeExp, s=np.sqrt(d["pop"])/90, c=d.continent.map(COL), alpha=.65, edgecolor="white", lw=.6)
    ax.set_xscale("log"); ax.set_xlim(200, 70000); ax.set_ylim(23, 87)
    x = np.log10(d.gdpPercap); s,i = np.polyfit(x, d.lifeExp, 1); r2 = np.corrcoef(x, d.lifeExp)[0,1]**2
    xs = np.linspace(x.min(), x.max(), 50); ax.plot(10**xs, i+s*xs, color="#333", lw=2, ls="--")
    ax.set_title(str(y)); ax.set_xlabel("GDP per capita (international $, log scale)")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_: f"${v:,.0f}"))
    ax.text(0.97, 0.05, f"R\u00b2 = {r2:.2f}\n+{s:.1f} years per 10x income", transform=ax.transAxes, ha="right", fontsize=10, bbox=dict(fc="white", ec="#ccc"))
    for n in (["China","India","United States","Japan"] if y==2007 else ["China","India","United States","Afghanistan"]):
        r = d[d.country==n].iloc[0]; ax.annotate(n, (r.gdpPercap, r.lifeExp), xytext=(6,-12), textcoords="offset points", fontsize=9)
axes[0].set_ylabel("Life expectancy at birth (years)")
fig.suptitle("Income still predicts longevity, but the whole curve has shifted upward", x=0.01, ha="left", fontsize=14, fontweight="bold", y=1.0)
handles = [plt.Line2D([],[],marker="o",ls="",color=v,label=k,ms=8) for k,v in COL.items()]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, bbox_to_anchor=(.5,-.04))
fig.text(0.01,-0.04,"Bubble size = population", fontsize=8, color="#666"); foot(fig); save(fig, "fig3_income_vs_life")

# ---------- Fig 4: income-matched comparison: expected life at $1,000 / $10,000
rows = []
for y in sorted(df.year.unique()):
    d = df[df.year==y]; x = np.log10(d.gdpPercap); s,i = np.polyfit(x, d.lifeExp, 1)
    rows.append((y, i+s*3, i+s*4))
t = pd.DataFrame(rows, columns=["year","at1k","at10k"])
fig, ax = plt.subplots(figsize=(11,6))
ax.plot(t.year, t.at10k, color="#0072B2", lw=2.8, marker="o"); ax.plot(t.year, t.at1k, color="#D55E00", lw=2.8, marker="o")
ax.fill_between(t.year, t.at1k, t.at10k, color="#999", alpha=.12)
ax.text(2007.6, t.at10k.iloc[-1], f"At $10,000: {t.at10k.iloc[-1]:.0f} yrs", color="#0072B2", fontweight="bold", va="center")
ax.text(2007.6, t.at1k.iloc[-1], f"At $1,000: {t.at1k.iloc[-1]:.0f} yrs", color="#D55E00", fontweight="bold", va="center")
ax.annotate(f"A $1,000-per-person country in 2007\nis predicted to live {t.at1k.iloc[-1]-t.at1k.iloc[0]:.0f} years longer\nthan one in 1952", xy=(2005, t.at1k.iloc[-1]-.3), xytext=(1962, 56),
            arrowprops=dict(arrowstyle="->", color="#333"), fontsize=10)
ax.set_xlim(1951, 2023); ax.set_ylim(38, 76); ax.set_xlabel("Year"); ax.set_ylabel("Predicted life expectancy (years)")
ax.set_title("Same income, longer life: predicted longevity at fixed income levels")
foot(fig, ". Predictions from a yearly fit of life expectancy on log10(GDP per capita)."); save(fig, "fig4_fixed_income")

# ---------- Fig 5: setbacks small multiples
p = df.pivot(index="year", columns="country", values="lifeExp")
cases = [("Rwanda","1992 value: 23.6 (civil war and genocide era)", 1992, "Conflict"),("Cambodia","1977: Khmer Rouge era, 31.2",1977,"Conflict"),
         ("China","1962: famine years, 44.5",1962,"Famine"),("Zimbabwe","Fell from 62.4 (1987) to 40.0 (2002)",2002,"HIV/AIDS era"),
         ("South Africa","Fell from 61.9 (1992) to 49.3 (2007)",2007,"HIV/AIDS era"),("Botswana","Fell from 63.6 (1987) to 46.6 (2002)",2002,"HIV/AIDS era")]
fig, axes = plt.subplots(2,3, figsize=(13,7), sharex=True)
world_s = world
for ax,(n,note,yr,tag) in zip(axes.ravel(), cases):
    ax.plot(world_s.index, world_s, color="#BBB", lw=2, label="World average")
    ax.plot(p.index, p[n], color="#B91C1C" if tag!="Famine" else "#7F1D1D", lw=2.8, marker="o", ms=4)
    ax.scatter([yr],[p.loc[yr,n]], s=90, color="#B91C1C", zorder=5, edgecolor="white")
    ax.set_title(f"{n}  ({tag})", fontsize=11); ax.set_ylim(20,80)
    ax.text(0.03,0.04,note, transform=ax.transAxes, fontsize=8.5, color="#444")
for ax in axes[:,0]: ax.set_ylabel("Life expectancy (years)")
for ax in axes[1]: ax.set_xlabel("Year")
axes[0,0].legend(frameon=False, fontsize=8, loc="upper left")
fig.suptitle("Progress is not guaranteed: six reversals hidden inside the upward trend", x=0.01, ha="left", fontsize=14, fontweight="bold", y=1.0)
foot(fig, ". Event labels are historical context, not derived from the dataset."); save(fig, "fig5_setbacks")

# ---------- Fig 6: over/under performers vs income prediction (2007)
d = df[df.year==2007].copy(); x = np.log10(d.gdpPercap); s,i = np.polyfit(x, d.lifeExp, 1); d["res"] = d.lifeExp-(i+s*x)
sel = pd.concat([d.nsmallest(8,"res"), d.nlargest(8,"res")]).sort_values("res")
fig, ax = plt.subplots(figsize=(10,7))
colors = ["#B91C1C" if r<0 else "#0072B2" for r in sel.res]
ax.hlines(sel.country, 0, sel.res, color=colors, lw=3); ax.scatter(sel.res, sel.country, color=colors, s=70, zorder=3)
ax.axvline(0, color="#333", lw=1); ax.grid(axis="y", visible=False)
for r,(cn,v,g) in zip(range(len(sel)), zip(sel.country, sel.res, sel.gdpPercap)):
    ax.text(v+(1 if v>0 else -1), r, f"{v:+.1f}  (${g:,.0f})", va="center", ha="left" if v>0 else "right", fontsize=8.5, color="#333")
ax.set_xlim(-35, 22); ax.set_xlabel("Years above / below life expectancy predicted by income (2007)")
ax.set_title("Beyond income: who lives longer, and shorter, than their wealth predicts")
foot(fig, ". Brackets show GDP per capita."); save(fig, "fig6_over_under_performers")

# ---------- Fig 7: dumbbell biggest gains, 1952 -> 2007 (top 12 gains)
pv = df.pivot(index="country", columns="year", values="lifeExp"); gain = (pv[2007]-pv[1952]).sort_values()
top = gain.tail(12); cont = df.drop_duplicates("country").set_index("country").continent
fig, ax = plt.subplots(figsize=(10,6.5))
for n in top.index:
    ax.plot([pv.loc[n,1952], pv.loc[n,2007]], [n,n], color="#BBB", lw=3, zorder=1)
    ax.scatter(pv.loc[n,1952], n, color="#999", s=60, zorder=2); ax.scatter(pv.loc[n,2007], n, color=COL[cont[n]], s=80, zorder=3)
    ax.text(pv.loc[n,2007]+1, n, f"+{gain[n]:.1f}", va="center", fontsize=9.5, fontweight="bold", color=COL[cont[n]])
ax.set_xlim(25,88); ax.grid(axis="y", visible=False); ax.set_xlabel("Life expectancy (years)  |  grey = 1952, colour = 2007")
ax.set_title("The fastest climbers: the twelve largest life-expectancy gains, 1952-2007")
foot(fig); save(fig, "fig7_biggest_gains")
print("done")
