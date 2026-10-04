import plotly.express as px, pandas as pd, numpy as np
df = px.data.gapminder()
print("missing:", df.isna().sum().sum(), "dups:", df.duplicated(['country','year']).sum(), "countries:", df.country.nunique())
# population-weighted life exp
def wavg(g): return np.average(g.lifeExp, weights=g['pop'])
w = df.groupby('year').apply(wavg); print("world pw:\n", w.round(1).iloc[[0,-1]])
c = df.groupby(['continent','year']).apply(wavg).unstack(); print((c[[1952,2007]]).round(1)); print((c[2007]-c[1952]).round(1))
# unweighted gap
for y in (1952,2007):
    d=df[df.year==y]; print(y,"mean",d.lifeExp.mean().round(1),"std",d.lifeExp.std().round(1),"min",d.loc[d.lifeExp.idxmin(),['country','lifeExp']].tolist(),"max",d.loc[d.lifeExp.idxmax(),['country','lifeExp']].tolist(), "range", (d.lifeExp.max()-d.lifeExp.min()).round(1))
# gains
p = df.pivot(index='country',columns='year',values='lifeExp'); gain=(p[2007]-p[1952]).sort_values(); print(gain.tail(8).round(1)); print(gain.head(8).round(1))
# declines
dec = p.diff(axis=1).min(axis=1).sort_values().head(10); print(dec.round(1))
print((p[2007]<p[1952]).sum(), "countries lower in 2007")
# Preston
for y in (1952,1977,2007):
    d=df[df.year==y]; x=np.log10(d.gdpPercap); s,i=np.polyfit(x,d.lifeExp,1); r=np.corrcoef(x,d.lifeExp)[0,1]
    print(y,"slope per 10x",round(s,1),"R2",round(r**2,2),"pred@$1000",round(i+s*3,1),"pred@$10000",round(i+s*4,1))
# Africa 2007 low
a=df[(df.year==2007)]; print(a.sort_values('lifeExp').head(6)[['country','lifeExp','gdpPercap']])
print(a[a.gdpPercap<2000].shape, a[(a.gdpPercap>10000)].lifeExp.min())
# GDP growth
g=df.groupby('year').apply(lambda g: np.average(g.gdpPercap,weights=g['pop'])); print(g.round(0).iloc[[0,-1]])
# overperformers: residual in 2007
d=df[df.year==2007].copy(); x=np.log10(d.gdpPercap); s,i=np.polyfit(x,d.lifeExp,1); d['res']=d.lifeExp-(i+s*x)
print(d.sort_values('res').head(5)[['country','lifeExp','gdpPercap','res']].round(1)); print(d.sort_values('res').tail(5)[['country','lifeExp','gdpPercap','res']].round(1))
# share of world pop in countries <60 life exp
for y in (1952,2007):
    d=df[df.year==y]; print(y, "pop share <60:", round(d[d.lifeExp<60]['pop'].sum()/d['pop'].sum()*100,1))
print(p.loc[['Rwanda','Zimbabwe','Cambodia','China','South Africa','Botswana','Swaziland']].round(1).T)
