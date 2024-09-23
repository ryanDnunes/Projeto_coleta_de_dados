from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    data = pd.read_csv('archive/CrimesOnWomenData.csv', skipinitialspace=True)
    return data[['id', 'State', 'Year', 'Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']]

data = load_data()

@app.route('/crimes', methods=['GET'])
def get_crimes():
    """Consulta todos os dados."""
    return jsonify(data.to_dict(orient='records'))

@app.route('/crimes', methods=['POST'])
def add_crime():
    """Inserir novos dados."""
    new_data = request.json
    global data
    # Crie um DataFrame apenas com as colunas desejadas
    new_entry = pd.DataFrame([new_data])[['id', 'State', 'Year', 'Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']]
    data = pd.concat([data, new_entry], ignore_index=True)
    data.to_csv('archive/CrimesOnWomenData.csv', index=False)  # Atualiza o arquivo CSV
    return jsonify(new_data), 201

@app.route('/crimes/<int:id>', methods=['PUT'])
def update_crime(id):
    """Atualizar dados existentes."""
    updated_data = request.json
    global data
    if id in data['id'].values:
        # Atualiza apenas as colunas existentes
        for key in updated_data.keys():
            if key in data.columns:
                data.loc[data['id'] == id, key] = updated_data[key]
        data.to_csv('archive/CrimesOnWomenData.csv', index=False)  # Atualiza o arquivo CSV
        return jsonify(updated_data)
    else:
        return jsonify({'error': 'Registro não encontrado'}), 404

@app.route('/crimes/<int:id>', methods=['DELETE'])
def delete_crime(id):
    """Deletar dados existentes."""
    global data
    if id in data['id'].values:
        data = data[data['id'] != id]
        data.to_csv('archive/CrimesOnWomenData.csv', index=False)  # Atualiza o arquivo CSV
        return jsonify({'message': 'Registro deletado'}), 204
    else:
        return jsonify({'error': 'Registro não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
