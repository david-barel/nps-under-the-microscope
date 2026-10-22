"""Reproducible fictional respondent-level data; never real customers."""
import numpy as np, pandas as pd, json
from pathlib import Path
rng=np.random.default_rng(20261016)
root=Path(__file__).resolve().parents[1]
topics=['fees','reliability','navigation','speed','features','trust','clarity']
phrases={
'fees':('Fees feel unpredictable and expensive','Fees are clear and reasonable'),
'reliability':('The app sometimes freezes or fails','The app works reliably'),
'navigation':('It is hard to find what I need','I can find what I need easily'),
'speed':('Tasks take longer than expected','Everything feels quick'),
'features':('Important features are missing','The features cover what I need'),
'trust':('I am not fully confident my money is safe','I trust the app with my money'),
'clarity':('The information is confusing','The information is easy to understand')}
rows=[]
for i in range(1600):
    tenure=int(rng.choice([0,1,2,3,4,5,6],p=[.1,.13,.19,.19,.17,.13,.09]))
    segment=str(rng.choice(['Everyday','Saver','Investor'],p=[.48,.33,.19]))
    base=np.array([.17,.32,.39,.31,.27,.22,.25])
    base += (segment=='Investor')*np.array([-.03,0,0,0,.10,.04,.02])
    # Topic mention is not determined by score. It reflects salience/experience.
    flags=rng.random(7)<base
    if not flags.any():flags[rng.integers(7)]=True
    # Each topic can be praised or criticized; no score-conditioned question or text.
    positive=np.where(flags,rng.random(7)<np.array([.27,.56,.59,.68,.70,.76,.61]),False)
    weights=np.array([1.45,1.15,.65,.40,.70,.95,.60])
    contributions=np.where(flags,np.where(positive,weights*.50,-weights),0)
    latent=7.5+contributions.sum()+.09*tenure+rng.normal(0,1.85)
    score=int(np.clip(np.rint(latent),0,10))
    present=[k for j,k in enumerate(topics) if flags[j]]
    # Pick up to two salient themes for an answer to 'main reason'.
    selected=sorted([j for j in range(7) if flags[j]],key=lambda j:abs(contributions[j])+rng.random()*.45,reverse=True)[:2]
    response='; '.join(phrases[topics[j]][int(positive[j])] for j in selected)+'.'
    row={'respondent_id':f'B{str(i+1).zfill(4)}','segment':segment,'tenure_years':tenure,'recommendation_score':score,'open_end':response}
    for j,k in enumerate(topics):row['topic_'+k]=int(j in selected)
    rows.append(row)
df=pd.DataFrame(rows)
df.to_csv(root/'data'/'fictional_bank_nps.csv',index=False)
# Summary estimates only from coded topic mentions; R script independently refits same model.
import statsmodels.formula.api as smf
formula='recommendation_score ~ '+' + '.join('topic_'+t for t in topics)+' + C(segment) + tenure_years'
model=smf.ols(formula,df).fit(cov_type='HC3')
ci=model.conf_int()
summary=[]
for t in topics:
    key='topic_'+t
    summary.append({'id':t,'name':t.replace('_',' ').title(),'coefficient':round(float(model.params[key]),3),'low':round(float(ci.loc[key,0]),3),'high':round(float(ci.loc[key,1]),3),'prevalence':round(float(df[key].mean()*100),1),'mentions':int(df[key].sum())})
p=int((df.recommendation_score>=9).sum());d=int((df.recommendation_score<=6).sum());n=len(df)
(root/'assets'/'model_results.json').write_text(json.dumps({'sample_size':n,'nps':round(100*(p-d)/n,1),'r_squared':round(float(model.rsquared),3),'drivers':summary},indent=2))
print('Generated',n,'synthetic responses; NPS',round(100*(p-d)/n,1))
