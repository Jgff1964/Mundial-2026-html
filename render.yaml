import re, requests
from bs4 import BeautifulSoup
from flags import canon_country_name
PROMIEDOS_PAGE_URL='https://www.promiedos.com.ar/league/fifa-world-cup/fjda'
PROMIEDOS_API_URL='https://api.promiedos.com.ar/league/tables_and_fixtures/fjda'
R32=[74,77,73,75,83,84,81,82,76,78,79,80,86,88,85,87]; R16=[89,90,93,94,91,92,95,96]; QF=[97,98,99,100]; SF=[101,102]
class PromiedosClient:
    def __init__(self,timeout=25):
        self.timeout=timeout; self.session=requests.Session(); self.last_summary={}
        self.session.headers.update({'User-Agent':'Mozilla/5.0 Chrome/148 Safari/537.36','Accept':'application/json,text/plain,*/*','Accept-Language':'es-AR,es;q=0.9','Origin':'https://www.promiedos.com.ar','Referer':'https://www.promiedos.com.ar/','X-Ver':'1.11.7.5'})
    def fetch_all(self):
        data=self.fetch_api(); return self.extract_zones_from_api(data), self.fetch_bracket_page()
    def fetch_api(self):
        r=self.session.get(PROMIEDOS_API_URL,timeout=self.timeout)
        self.last_summary={'api_url':PROMIEDOS_API_URL,'status_code':r.status_code,'content_type':r.headers.get('content-type'),'x_ver_sent':self.session.headers.get('X-Ver'),'text_preview':r.text[:1000]}
        r.raise_for_status(); data=r.json(); self.last_summary.update({'root_type':type(data).__name__,'root_keys':list(data.keys())[:50] if isinstance(data,dict) else None,'list_len':len(data) if isinstance(data,list) else None}); return data
    def extract_zones_from_api(self,data):
        cand=[]; self._walk(data,[],cand); rows=[]
        for path,title,lst in cand:
            clean=[{'team':t} for t in [self._row_team(x) for x in lst] if t]
            if len(clean)>=2: rows.append((path,title,clean))
        groups=list('ABCDEFGHIJKL'); zones={}
        for i,(_,_,r) in enumerate(rows[:12]): zones[groups[i]]=r
        self.last_summary['tables_found']=len(rows); self.last_summary['groups_found']=list(zones.keys())
        if len(zones)<8: raise RuntimeError(f"Promiedos API no devolvió suficientes tablas de grupos. Leídas: {list(zones.keys())}. Debug: {self.last_summary}")
        return zones
    def _walk(self,obj,path,out):
        if isinstance(obj,dict):
            title=str(obj.get('name') or obj.get('title') or obj.get('grupo') or obj.get('group') or '')
            for k,v in obj.items():
                if isinstance(v,list) and sum(1 for x in v if isinstance(x,dict) and self._row_team(x))>=2: out.append((path+[str(k)],title or str(k),v))
                self._walk(v,path+[str(k)],out)
        elif isinstance(obj,list):
            for i,v in enumerate(obj): self._walk(v,path+[str(i)],out)
    def _row_team(self,row):
        if not isinstance(row,dict): return ''
        for k in ['team','equipo','name','nombre','club','country','pais','selection','seleccion']:
            v=row.get(k)
            t=canon_country_name(v)
            if t and not t.startswith(('GANADOR','PERDEDOR')): return t
            if isinstance(v,dict):
                for kk in ['name','nombre','short_name','shortName','displayName']:
                    t=canon_country_name(v.get(kk))
                    if t: return t
        return ''
    def fetch_bracket_page(self):
        soup=BeautifulSoup(self.session.get(PROMIEDOS_PAGE_URL,timeout=self.timeout).text,'html.parser'); tokens=[x.strip() for x in soup.get_text('\n').splitlines() if x.strip() and 'Loading' not in x]
        try: tokens=tokens[tokens.index('CUADRO')+1:]
        except ValueError: pass
        sec=self._split(tokens); final,third=self._final(sec.get('Final',[])); return {'r32':self._pairs_to_matches(sec.get('16avos de final',[]),R32),'r16':self._pairs_to_matches(sec.get('Octavos de Final',[]),R16),'qf':self._pairs_to_matches(sec.get('Cuartos de Final',[]),QF),'sf':self._pairs_to_matches(sec.get('Semifinales',[]),SF),'final':final,'third':third}
    def _split(self,tokens):
        names=['16avos de final','Octavos de Final','Cuartos de Final','Semifinales','Final']; sec={}; cur=None
        for t in tokens:
            if t in names: cur=t; sec[cur]=[]; continue
            if cur and t not in {'FINAL','3er puesto'}: sec[cur].append(t)
        return sec
    def _clean(self,t):
        t=str(t).strip().replace('Ganador del partido ','Ganador M').replace('Perdedor del partido ','Perdedor M')
        return t if t.upper().startswith(('GANADOR','PERDEDOR')) else canon_country_name(t)
    def _pairs(self,tokens):
        c=[self._clean(t) for t in tokens if self._clean(t)]; return [(c[i],c[i+1]) for i in range(0,len(c)-1,2)]
    def _pairs_to_matches(self,tokens,nums): return {n:{'venue':'','home':p[0],'away':p[1]} for n,p in zip(nums,self._pairs(tokens))}
    def _final(self,tokens):
        p=self._pairs(tokens); return ({104:{'venue':'NYNJ','home':p[0][0],'away':p[0][1]}} if len(p)>0 else {}, {103:{'venue':'MIA','home':p[1][0],'away':p[1][1]}} if len(p)>1 else {})
