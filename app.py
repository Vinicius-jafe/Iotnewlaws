from flask import Flask, request
from datetime import datetime
import sqlite3
import re
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('decibeis.db', timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/dados', methods=['POST'])
def dados():
    print("\n=== Nova Requisição ===")
    print("Headers:", dict(request.headers))
    print("Form data:", request.form)
    print("Raw data:", request.get_data())
    print("Args (query string):", request.args)

    decibel_raw = request.form.get('decibel')
    if not decibel_raw:
        print("❌ Decibel não enviado!")
        return "Decibel não enviado", 400

    # Extrair o número final usando regex
    match = re.search(r'([\d.]+)$', decibel_raw)
    if match:
        decibel_value = float(match.group(1))
        print(f"✅ Decibel extraído e convertido: {decibel_value}")
    else:
        print(f"❌ Não foi possível extrair número de: {decibel_raw}")
        return "Valor decibel inválido", 400

    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕒 Data da leitura: {data}")

    # Salvar no banco
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO decibeis (valor, data) VALUES (?, ?)', (decibel_value, data))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Erro no banco: {e}")
        return f"Erro no banco: {e}", 500
    finally:
        conn.close()

    print("========================\n")
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # ✅ Ajuste número 3
    app.run(host='0.0.0.0', port=port)
