from typing import List, Dict
from app.PlanilhaRepositorio import PlanilhaRepositorio

class DashboardRepositorio:

    def __init__(self):
        self.planilha_repo = PlanilhaRepositorio()

# retorna valor de tudo que já foi gasto
    def get_total_saida(self,lista_movimentacoes: List[Dict]) -> float:

        total_gasto = sum(g['valor'] for g in lista_movimentacoes if g['tipo'] == 'saida' and g['pago'] == 'sim')

        return total_gasto

# retorna valor de tudo que já foi recebido
    def get_total_entrada(self,lista_movimentacoes: List[Dict]) -> float:

        total_entrada = sum(g['valor'] for g in lista_movimentacoes if g['tipo'] == 'entrada' and g['pago'] == 'sim')

        return total_entrada

# retorna valor do saldo atual
    def get_saldo_atual(self,lista_movimentacoes: List[Dict]) -> float:

        saldo = self.get_total_entrada(lista_movimentacoes) - self.get_total_saida(lista_movimentacoes)

        return saldo

# retorna valor de saidas ainda não pagas com recorte mensal (A pagar)
    def get_a_pagar(self, mes : str, lista_movimentacoes: List[Dict]) -> float:

        total_a_pagar = sum(g['valor'] for g in lista_movimentacoes 
                            if g['tipo'] == 'saida' 
                            and  g['pago'] == 'nao' 
                            and  g['considerar_no_painel'] == 'sim' 
                            and g['data'][5:7] == mes 
                            )

        return total_a_pagar

# retorna lista de saidas ainda não pagas com recorte mensal (A pagar)
    def get_a_pagar_lista(self, mes : str, lista_movimentacoes: List[Dict]) -> List[Dict]:
        
        a_pagar_lista = [
                            g for g in lista_movimentacoes
                            if g['tipo'] == 'saida'
                            and g['pago'] == 'nao'
                            and  g['considerar_no_painel'] == 'sim' 
                            and g['data'][5:7] == mes
                        ]
        
        return a_pagar_lista
    
    # Lista das coisas que não estão pagas mais proximas do vencimento independentes de serem entrada ou saida
    def get_lembrentes(self, lista_movimentacoes: List[Dict]) -> List[Dict]: 
        from datetime import datetime

        # 1. Pega a data de hoje exata do sistema
        hoje = datetime.now().date()
        
        # 2. Ordena calculando a distância absoluta de dias até o dia de hoje
        lembretes = [l for l in lista_movimentacoes if l['pago'] == "nao"]

        lembretes_filtrados = sorted(
            lembretes, 
            key=lambda g: abs((datetime.strptime(g['data'], "%Y-%m-%d").date() - hoje).days)
        )

        
        return lembretes_filtrados