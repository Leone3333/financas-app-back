import os
import json
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict

# COMANDO PARA ENTRAR NO AMBIENTE VIRTUAL 
# source venv/bin/activate

class PlanilhaRepositorio:
    def __init__(self):
        # iniciar conexão com planilha
        escopos = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
        
        info_env = os.environ.get("GOOGLE_CREDENTIALS")

        if info_env:
            # Se estiver rodando no Render (Nuvem)
            credencias_dict = json.loads(info_env)
            credenciais = Credentials.from_service_account_info(credencias_dict, scopes=escopos)
        else:
            # Se estiver rodando no seu computador pessoal (Local)
            credenciais = Credentials.from_service_account_file("credenciais.json", scopes=escopos)
            
        self.cliente = gspread.authorize(credenciais)
        self.planilha = self.cliente.open("gastos_projects")
        self.aba_categorias = self.planilha.worksheet('categorias') 
        self.aba_movimentacoes = self.planilha.worksheet('movimentacoes') 
        self.aba_bancos = self.planilha.worksheet('bancos') 

    # criar registro de gasto 
    
    """
    def create(self, gasto_dados: List) -> bool:
        try:
            self.aba_dois.append_row(gasto_dados)
            return True
        except Exception as e:
            print(f"Erro na classe ao inserir: {e}")
            return False
    
    """
    
    # returna todos os registros independente de . ou ,
    def get_movimentacoes(self) -> List[Dict]:
        # from gspread import NumericFormatting
        return self.aba_movimentacoes.get_all_records()
    
    def get_categorias(self) -> List[Dict]:
        # from gspread import NumericFormatting
        return self.aba_categorias.get_all_records()


    # atualizar status de considerar painel da lista de coisas a pagar
    def atualizar_movimentacao(self, id: int, dados_atualizados: dict) -> bool:
        try:
            registro = 0

            movimentacoes = self.get_movimentacoes()

            for idx, s in enumerate(movimentacoes, start=2):
                if s['id'] == id:
                    registro = idx
                    print(registro)
                    break

            if registro == 0:
                print(f"ID {id} não foi encontrado na planilha.")
                return False

            registro_atual = movimentacoes[registro - 2]
            dados_finais = {**registro_atual, **dados_atualizados}

            linha_para_salvar = [
                dados_finais.get('id'),
                dados_finais.get('data'),
                dados_finais.get('descricao'),
                dados_finais.get('valor'),
                dados_finais.get('tipo'),
                dados_finais.get('categoria_id'),
                dados_finais.get('banco_id'),
                dados_finais.get('forma_pagamento'),
                dados_finais.get('pago'),
                dados_finais.get('considerar_no_painel'),
                dados_finais.get('parcela_atual'),
                dados_finais.get('parcela_total')
            ]
            
            intervalo = f"A{registro}:L{registro}"

            # No gspread, a linha 1 é o cabeçalho. A primeira linha de dados é a 2.
            # Coluna 6 é a coluna 'pago'
            self.aba_movimentacoes.update(range_name=intervalo,values=[linha_para_salvar])
            print(f"Linha {registro} atualizada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            return False

    """
    # 4. DELETE Deletar registro lembrabr de passar a linha do registro
    def deletar(self, linha_index: int) -> bool:
        try:
            self.aba_dois.delete_rows(linha_index)
            return True
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return False
    """



    