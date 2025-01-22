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
            
            # Verificar se o campo 'trintytype' existe
            tipo_transacao = getattr(transacao, 'trintytype', 'Tipo desconhecido')  # Padrão caso 'trintytype' não exista
            
            # Tentando obter o nome do payee (quem recebeu ou fez a transferência)
            payee = getattr(transacao, 'memo', 'Não disponível')  # Usando memo como fallback

            # Imprimir as informações
            print(f'Data: {data} | Valor: {valor:.2f} | | Para/De: {payee}| Tipo: {tipo_transacao} | ')

# Caminho para o arquivo .ofx
arquivo_ofx = r'c:\Users\user\Downloads\extrato.ofx'

# Chamar a função para processar o arquivo
processar_ofx(arquivo_ofx)



