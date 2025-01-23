import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS
from ofxparse import OfxParser
import os

app = Flask(__name__)

# Habilita CORS para permitir acesso de qualquer origem
CORS(app)

# Configuração da conexão com o SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=FINANCAS;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Pasta para salvar os arquivos temporariamente
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota para buscar dados do banco
@app.route('/get_dados', methods=['GET'])
def get_dados():
    try:
        cursor.execute(
            """
   SELECT FORMAT(quando, 'dd/MM/yyyy') AS Quando,
       -- Pegando a parte da string a partir do primeiro hífen
       RIGHT(onde, LEN(onde) - CHARINDEX('-', onde) - 1) AS Onde,  
       CONVERT(decimal(18,2), quanto) AS Quanto  
FROM MOVIMENTACAO
WHERE Onde LIKE '%-%'  -- Garante que o valor tem ao menos um hífen
ORDER BY quando;



    """
        )
        dados = cursor.fetchall()

        lista_dados = []
        for dado in dados:
            lista_dados.append({
                'data': dado[0],
                'onde': dado[1],
                'valor': float(dado[2]),
            })

        print(f"Lista de dados retornada: {lista_dados}")  # Log dos dados
        return jsonify(lista_dados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        


# Rota para fazer upload e processar arquivo OFX
@app.route('/upload_ofx', methods=['POST'])
def upload_ofx():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    # Validação do tipo de arquivo OFX
    if not file.filename.lower().endswith('.ofx'):
        return jsonify({"error": "Arquivo deve ser no formato OFX"}), 400

    # Salvar o arquivo na pasta temporária
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        # Processar o arquivo OFX
        with open(filepath, 'rb') as f:
            ofx = OfxParser.parse(f)

        for conta in ofx.accounts:
            for transacao in conta.statement.transactions:
                data = transacao.date.strftime('%Y-%m-%d')  # Formato de data para SQL Server
                valor = transacao.amount
                onde = getattr(transacao, 'memo', 'Não disponível')  # Fallback para memo
                tipo = getattr(transacao, 'trinitytype', 'Desconhecido')  # Verificar tipo

                # Inserir os dados na tabela MOVIMENTACAO
                cursor.execute(
                    """
                    INSERT INTO MOVIMENTACAO (quando, onde, quanto)
                    VALUES (?, ?, ?)
                    """,
                    (data, onde, valor)
                )

        # Após inserir na MOVIMENTACAO, agora insere os dados nas tabelas T_ENTRADA e T_SAIDA
        cursor.execute(
            """
            INSERT INTO T_ENTRADA (mes, total)
            SELECT 
            DATETRUNC(MONTH, quando) AS Mes,
	        SUM(quanto) AS total
            FROM MOVIMENTACAO
            WHERE quanto >= 0
            GROUP BY DATETRUNC(MONTH, quando);
            """
        )

        cursor.execute(
            """
            -- Inserir saídas (quanto <= 0) na tabela T_SAIDA
            INSERT INTO T_SAIDA (mes, total)
            SELECT 
                DATETRUNC(MONTH, quando) AS Mes,
                SUM(quanto) AS total
            FROM MOVIMENTACAO
            WHERE quanto <= 0
            GROUP BY DATETRUNC(MONTH, quando);
            """
        )

        conn.commit()  # Confirma as alterações no banco
        os.remove(filepath)  # Remove o arquivo após o processamento

        return jsonify({"message": "Arquivo processado com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao processar o arquivo OFX: {str(e)}"}), 500


if __name__ == '__main__':
    # Inicia o servidor Flask na porta 5000
    app.run(debug=True)




