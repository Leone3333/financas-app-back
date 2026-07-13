from datetime import datetime
from flask import Flask, jsonify,request
from flask_cors import CORS
from app.PlanilhaRepositorio import PlanilhaRepositorio
from app.DashboardRepositorio import DashboardRepositorio 

app = Flask(__name__)
port = 3001
host = '0.0.0.0'
CORS(app)
# Instancia o nosso repositório
repo = PlanilhaRepositorio()
dashboard = DashboardRepositorio()


@app.route('/api/dashboard/', methods=['GET'])
@app.route('/api/dashboard/<mes>', methods=['GET'])
def data_dashboard(mes=None):

    if mes is None:
        mes = datetime.now().strftime('%m')

    m = repo.get_movimentacoes()
    saldo = dashboard.get_saldo_atual(m)
    a_pagar = dashboard.get_a_pagar(mes,m)
    lembretes = dashboard.get_lembrentes(m)

    return jsonify({
        'mes': mes,
        'saldo': saldo,
        'a_pagar': a_pagar,
        'lembretes': lembretes[:5],
    }),200

@app.route('/api/dashboard/lembretes/', methods=['GET'])
@app.route('/api/dashboard/lembretes/<mes>', methods=['GET'])
def data_a_pagar_lista(mes=None):

    if mes is None:
        mes = datetime.now().strftime('%m')

    m = repo.get_movimentacoes()
    a_pagar = dashboard.get_a_pagar(mes,m)
    a_pagar_lista = dashboard.get_a_pagar_lista(mes,m)

    return jsonify({
        'mes': mes,
        'a_pagar': a_pagar,
        'a_pagar_lista': a_pagar_lista,
    }),200

@app.route('/api/dashboard/lembretes/<int:id>/<int:col>/<novo_status>', methods=['PUT'])
def update_considerar_painel(id,col,novo_status):

    update_line = repo.atualizar_status(id,col,novo_status)

    return jsonify({
        'status_request': update_line    
    }),200

if __name__ == '__main__':
    app.run(host,debug=True,port=port)

