from app.PlanilhaRepositorio import PlanilhaRepositorio
from app.DashboardRepositorio import DashboardRepositorio

# Instancia o nosso repositório
repo = PlanilhaRepositorio()
dashboard = DashboardRepositorio()


print("\n--- 1. Testando a Leitura (READ) ---")
m = repo.get_movimentacoes()
categorias = repo.get_categorias()
# print(m)

"""
for idx, gasto in enumerate(m, start=1):
    # Mudamos 'item' para 'descricao' para bater com a sua planilha
    print(f"Linha {idx}: {gasto['descricao']} - R$ {gasto['valor']} (Pago: {gasto['pago']})")
"""


# for idx, cat in enumerate(categorias,start=1):
#     print(f"Linha: {idx}: {cat['id']} - {cat['descricao']} - {cat['tipo_padrao']}")


print("\n--- 2. Teste calculo total gasto ---")
print("\n--- 2.1 Valor Saidas ---")
print(f"Total saidas: {dashboard.get_total_saida(m)}")

print("\n--- 2.2 Valor Entradas ---")
print(f"Total saidas: {dashboard.get_total_entrada(m)}")

print("\n--- 2.3 Valor Saldo atual ---")
print(f"Total saidas: {dashboard.get_saldo_atual(m)}")


print("\n--- 3 Valor devendo no mês ---")
a_pagar = dashboard.get_a_pagar_lista('07',m)

for idx, s in enumerate(a_pagar, start=1):
    print(f"Linha {idx}: {s['descricao']} - R$ {s['valor']} (Vencimento: {s['data']})")

print(f"Total a pagar no mes 07: {dashboard.get_a_pagar('07',m)}")


print("\n--- 4 Lista lembretes ---")
lembrete = dashboard.get_lembrentes(m)

for index, l in enumerate(lembrete[:5],start=1):
    print(f"Linha: {index}:  (Tipo de lembrete: {l['tipo']}) -- {l['descricao']} -- R$ {l['valor']} -- (Vencimento: {l['data']})")
