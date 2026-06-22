from datetime import datetime
from flask import Flask,jsonify,render_template,request,Response
from bracket_logic import load_zones,make_bracket_from_zones,overlay_promiedos_bracket
from promiedos_client import PromiedosClient,PROMIEDOS_API_URL,PROMIEDOS_PAGE_URL
from renderer import render_svg
app=Flask(__name__); STATE={'zones':load_zones(),'promiedos':None,'last_update':None,'last_error':None,'include_thirds':False,'source':'zonas_validadas.json','api_summary':{}}
def current_bracket():
    b=overlay_promiedos_bracket(make_bracket_from_zones(STATE.get('zones') or load_zones(),STATE['include_thirds']),STATE['promiedos']); b['source']=STATE.get('source','Promiedos'); return b
def current_svg(): return render_svg(current_bracket(),'Promiedos tablas'+(' · con terceros' if STATE['include_thirds'] else ' · sin terceros'))
@app.route('/')
def index(): return render_template('index.html')
@app.route('/api/update_promiedos',methods=['POST'])
def update_promiedos():
    try:
        c=PromiedosClient(); zones,bracket=c.fetch_all(); STATE.update({'zones':zones,'promiedos':bracket,'last_update':datetime.now().isoformat(timespec='seconds'),'last_error':None,'source':'Promiedos tablas','api_summary':c.last_summary}); return jsonify({'ok':True,'message':'Actualizado desde Promiedos. Grupos leídos: '+', '.join(zones.keys())})
    except Exception as exc:
        STATE['last_error']=str(exc)
        if 'c' in locals(): STATE['api_summary']=c.last_summary
        return jsonify({'ok':False,'error':str(exc),'api_summary':STATE['api_summary']}),500
@app.route('/api/settings',methods=['POST'])
def settings():
    STATE['include_thirds']=bool((request.get_json(force=True,silent=True) or {}).get('include_thirds')); return jsonify({'ok':True,'include_thirds':STATE['include_thirds']})
@app.route('/api/render')
def render(): return jsonify({'svg':current_svg(),'include_thirds':STATE['include_thirds']})
@app.route('/bracket.svg')
def bracket_svg(): return Response(current_svg(),mimetype='image/svg+xml')
@app.route('/api/debug')
def debug(): return jsonify({'api_url':PROMIEDOS_API_URL,'page_url':PROMIEDOS_PAGE_URL,'last_update':STATE['last_update'],'last_error':STATE['last_error'],'include_thirds':STATE['include_thirds'],'source':STATE['source'],'zones':STATE['zones'],'api_summary':STATE['api_summary'],'promiedos':STATE['promiedos']})
if __name__=='__main__': app.run(host='0.0.0.0',port=5000,debug=False)
