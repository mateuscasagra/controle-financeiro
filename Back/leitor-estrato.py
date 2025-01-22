from ofxparse import OfxParser

# Função para processar o arquivo .ofx e extrair as informações
def processar_ofx(arquivo_ofx):
    # Abrir o arquivo como binário (modo 'rb') para evitar problemas de codificação
    with open(arquivo_ofx, 'rb') as f:
        ofx = OfxParser.parse(f)

    # Iterar sobre as transações e imprimir as informações
    for conta in ofx.accounts:
        for transacao in conta.statement.transactions:
            data = transacao.date.strftime("%d/%m/%Y")  # Formatar a data
            valor = transacao.amount  # Valor da transação
            tipo_transacao = 'Crédito' if valor > 0 else 'Débito'  # Tipo da transação
            print(f'Data: {data} | Valor: {valor:.2f} | Tipo: {tipo_transacao}')

# Caminho para o arquivo .ofx
arquivo_ofx = r'c:\Users\user\Downloads\extrato.ofx'

# Chamar a função para processar o arquivo
processar_ofx(arquivo_ofx)
