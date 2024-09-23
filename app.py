from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    #pd.read_csv() le o csv
    data = pd.read_csv('archive/CrimesOnWomenData.csv', skipinitialspace=True)
    #seleciona colunas especificas
    return data[['id', 'State', 'Year', 'Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']]

data = load_data()

@app.route('/crimes', methods=['GET'])
def get_crimes():
    """Consulta todos os crimes."""
    return jsonify(data.to_dict(orient='records'))

@app.route('/crimes', methods=['POST'])
def add_crime():
    """Inserir novo crime"""
    data_nova = request.json
    global data
    # Crie um DataFrame apenas para as colunas desejadas
    novo_dado = pd.DataFrame([data_nova])[['id', 'State', 'Year', 'Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']]
    data = pd.concat([data, novo_dado], ignore_index=True)
    data.to_csv('archive/CrimesOnWomenData.csv', index=False)  # salva
    return jsonify(data_nova), 201

@app.route('/crimes/<int:id>', methods=['PUT'])
def update_crime(id):
    """Atualizar dados existentes."""
    atualizar_data = request.json
    global data
    if id in data['id'].values:
        # Atualiza apenas as colunas existentes
        for key in atualizar_data.keys():
            if key in data.columns:
                data.loc[data['id'] == id, key] = atualizar_data[key]
        data.to_csv('archive/CrimesOnWomenData.csv', index=False)  # salva
        return jsonify(atualizar_data)
    else:
        return jsonify({'error': 'Registro não encontrado'}), 404

@app.route('/crimes/<int:id>', methods=['DELETE'])
def delete_crime(id):
    """tirar dados apartir de um id"""
    global data
    if id in data['id'].values:
        data = data[data['id'] != id]
        data.to_csv('archive/CrimesOnWomenData.csv', index=False)  # salva
        return jsonify({'message': 'Registro deletado'}), 204
    else:
        return jsonify({'error': 'Registro não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
