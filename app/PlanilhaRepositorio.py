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
        
        # credencias em variavel de ambiente no render 
        infos_credenciais = os.environ.get("GOOGLE_CREDENTIALS")

        # converte json em dicionario python
        credencias_dict = json.loads(infos_credenciais)
        
        #  método que lê as credenciais em dicionario python
        credenciais = Credentials.from_service_account_info(credencias_dict, scopes=escopos)
        
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


    # atualizar status de pagamento do registro lembrar de passar o numero da linha do registro
    """
    def atualizar_status_pago(self, linha_index: int, novo_status: str) -> bool:
        try:
            # No gspread, a linha 1 é o cabeçalho. A primeira linha de dados é a 2.
            # Coluna 6 é a coluna 'pago'
            self.aba_dois.update_cell(linha_index, 6, novo_status)
            return True
        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            return False

    # 4. DELETE Deletar registro lembrabr de passar a linha do registro
    def deletar(self, linha_index: int) -> bool:
        try:
            self.aba_dois.delete_rows(linha_index)
            return True
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return False
    """



    