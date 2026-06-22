import json,re
from pathlib import Path
from flags import canon_country_name
R32={73:('2A','2B','LA'),74:('1E','3A/B/C/D/F','BOS'),75:('1F','2C','MTY'),76:('1C','2F','HOU'),77:('1I','3C/D/F/G/H','NYNJ'),78:('2E','2I','DAL'),79:('1A','3C/E/F/H/I','CDMX'),80:('1L','3E/H/I/J/K','ATL'),81:('1D','3B/E/F/I/J','SFBA'),82:('1G','3A/E/H/I/J','SEA'),83:('2K','2L','TOR'),84:('1H','2J','LA'),85:('1B','3E/F/G/I/J','VAN'),86:('1J','2H','MIA'),87:('1K','3D/E/I/J/L','KC'),88:('2D','2G','DAL')}
R16={89:(74,77,'PHI'),90:(73,75,'HOU'),91:(76,78,'NYNJ'),92:(79,80,'CDMX'),93:(83,84,'DAL'),94:(81,82,'SEA'),95:(86,88,'ATL'),96:(85,87,'VAN')}
QF={97:(89,90,'BOS'),98:(93,94,'LA'),99:(91,92,'MIA'),100:(95,96,'KC')}; SF={101:(97,98,'DAL'),102:(99,100,'ATL')}; THIRD={103:(101,102,'MIA')}; FINAL={104:(101,102,'NYNJ')}
def load_zones(path='zonas_validadas.json'):
    p=Path(path); return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
def resolve(seed,zones):
    seed=str(seed).upper()
    if re.fullmatch(r'[12][A-L]',seed):
        rows=zones.get(seed[1],[]); pos=int(seed[0])-1
        return canon_country_name(rows[pos].get('team','')) if len(rows)>pos else ''
    if seed.startswith('3'): return ''
    return canon_country_name(seed)
def make_bracket_from_zones(zones,include_thirds=False):
    b={'r32':{},'r16':{},'qf':{},'sf':{},'third':{},'final':{},'source':'Promiedos'}
    for n,(a,c,v) in R32.items(): b['r32'][n]={'venue':v,'home':resolve(a,zones),'away':resolve(c,zones)}
    for n,(a,c,v) in R16.items(): b['r16'][n]={'venue':v,'home':f'Ganador M{a}','away':f'Ganador M{c}'}
    for n,(a,c,v) in QF.items(): b['qf'][n]={'venue':v,'home':f'Ganador M{a}','away':f'Ganador M{c}'}
    for n,(a,c,v) in SF.items(): b['sf'][n]={'venue':v,'home':f'Ganador M{a}','away':f'Ganador M{c}'}
    for n,(a,c,v) in THIRD.items(): b['third'][n]={'venue':v,'home':f'Perdedor M{a}','away':f'Perdedor M{c}'}
    for n,(a,c,v) in FINAL.items(): b['final'][n]={'venue':v,'home':f'Ganador M{a}','away':f'Ganador M{c}'}
    return b
def seed_like(v):
    v=str(v or '').upper(); return not v or v.startswith(('GANADOR','PERDEDOR')) or re.fullmatch(r'[123][A-L](?:/[A-L])*',v)
def overlay_promiedos_bracket(base,prom):
    changed=0
    if prom:
        for rk in ['r32','r16','qf','sf','third','final']:
            for n,d in prom.get(rk,{}).items():
                n=int(n); h=canon_country_name(d.get('home')); a=canon_country_name(d.get('away'))
                if n in base.get(rk,{}) and h and a and not seed_like(h) and not seed_like(a): base[rk][n]['home']=h; base[rk][n]['away']=a; changed+=1
    base['source']='Promiedos cuadro armado' if changed else 'Promiedos tablas + estructura'
    return base
