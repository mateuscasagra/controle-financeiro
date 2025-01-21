import pyodbc
from flask import Flask, jsonify
from flask_cors import CORS

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

# Rota para buscar dados do banco
@app.route('/get_dados', methods=['GET'])
def get_dados():
    try:
        # Consulta SQL para pegar os dados
        cursor.execute("SELECT FORMAT(quando, 'dd/MM/yyyy') AS Quando, onde AS Onde, CONVERT(decimal(4,2), quanto) AS Qaunto, tipo AS Tipo FROM MOVIMENTACAO ORDER BY quando;")
        
        # Pega todos os resultados
        dados = cursor.fetchall()

        # Cria uma lista para armazenar os dados formatados
        lista_dados = []
        for dado in dados:
            lista_dados.append({
                'data': dado[0],  # Data da movimentação
                'onde': dado[1],  # Onde ocorreu a movimentação
                'valor': dado[2],
                 'tipo': dado[3]   # Valor da movimentação
            })

        # Retorna os dados como um JSON
        return jsonify(lista_dados)

    except Exception as e:
        # Caso ocorra algum erro, retorna uma mensagem de erro
        return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    # Inicia o servidor Flask na porta 5000
    app.run(debug=True)




