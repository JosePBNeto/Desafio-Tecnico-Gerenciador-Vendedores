import sqlite3
from flask import Flask, request, jsonify
from Vendedor import GerenciarVendedor, Vendedor
from app.Excel_functions import criar_atualizar_em_lotes, calcular_comissoes, calcular_volume_e_media_vendas

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

gerenciadorVendedor = GerenciarVendedor()
FILE_PATH_VENDAS = '../resources/Vendas.xlsx'
FILE_PATH_VENDEDORES = "../resources/Vendedores.xlsx"

@app.route('/vendedores', methods=['POST'])
def create_vendedor():
    data = request.json
    try:
        vendedor = Vendedor(data['nome'], data['cpf'], data['data_nascimento'], data['email'], data['estado'])
        gerenciadorVendedor.create_vendedor(vendedor)
        resposta = {
            "message": "Vendedor criado com sucesso",
            "data": {
                "nome": vendedor.nome,
                "cpf": vendedor.cpf,
                "data_nascimento": vendedor.data_nascimento,
                "email": vendedor.email,
                "estado": vendedor.estado
            }
        }
        return jsonify(resposta), 201
    except sqlite3.IntegrityError as e:
        return jsonify({
            "status": "erro",
            "message": f"Erro ao criar vendedor: {e}"
        }), 500

@app.route('/vendedores/<cpf>', methods=['GET'])
def get_vendedor(cpf):
    vendedor = gerenciadorVendedor.read_vendedor(cpf)
    if vendedor:
        return jsonify({
            "cpf": vendedor[0],
            "nome": vendedor[1],
            "data_nascimento": vendedor[2],
            "email": vendedor[3],
            "estado": vendedor[4]
        }), 200
    return jsonify({"message": "Vendedor não encontrado"}), 404

@app.route('/vendedores/<cpf>', methods=['PUT'])
def update_vendedor(cpf):
    vendedor_existente = gerenciadorVendedor.read_vendedor(cpf)
    if vendedor_existente:
        data = request.json
        try:
            vendedor = Vendedor(data['nome'], data['cpf'], data['data_nascimento'], data['email'], data['estado'])
            gerenciadorVendedor.update_vendedor(vendedor)
            return jsonify({
                "status": "success",
                "message": f"Vendedor com CPF {cpf} atualizado com sucesso"
            }), 200
        except sqlite3.IntegrityError as e:
            return jsonify({
                "status": "erro",
                "message": f"Erro ao atualizar vendedor: {e}"
            }), 500
    else:
        return jsonify({
            "status": "erro",
            "message": f"Vendedor com CPF {cpf} não encontrado"
        }), 404

@app.route('/vendedores/<cpf>', methods=['DELETE'])
def delete_vendedor(cpf):
    vendedor = gerenciadorVendedor.read_vendedor(cpf)
    if vendedor:
        gerenciadorVendedor.delete_vendedor(cpf)
        return jsonify({
            "status": "success",
            "message": f"Vendedor com CPF {cpf} excluído com sucesso"
        }), 200
    else:
        return jsonify({
            "status": "erro",
            "message": f"Vendedor com CPF {cpf} não encontrado"
        }), 404

@app.route('/vendedores', methods=['GET'])
def get_all_vendedores():
    vendedores = gerenciadorVendedor.read_all_vendedores()
    return jsonify(
        [{"cpf": v[0], "nome": v[1], "data_nascimento": v[2], "email": v[3], "estado": v[4]} for v in vendedores]
    ), 200

@app.route('/vendedores/planilha', methods=['POST'])
def update_planilha_vendedor():
    try:
        lista_de_vendedores = criar_atualizar_em_lotes(FILE_PATH_VENDEDORES)
        vendedores_json = [
            {
                'Nome': vendedor.nome,
                'CPF': vendedor.cpf,
                'Data de Nascimento': vendedor.data_nascimento,
                'Email': vendedor.email,
                'Estado': vendedor.estado
            } for vendedor in lista_de_vendedores
        ]
        return jsonify({"message": "Vendedores atualizados ou adicionados", "vendedores": vendedores_json}), 201
    except FileNotFoundError as e:
        return jsonify({
            "status": "erro",
            "message": f"Arquivo não encontrado: {e.filename}"
        }), 404
    except sqlite3.IntegrityError as e:
        return jsonify({
            "status": "erro",
            "message": f"Erro ao atualizar ou criar vendedor: {e}"
        }), 500

@app.route('/vendedores/calcularComissao', methods=['POST'])
def calcular_planilha_vendedor():
    try:
        calcular_comissoes(FILE_PATH_VENDAS)
        return jsonify({'success': 'Comissões calculadas com sucesso. Foi adicionado ou atualizado uma nova sheet na planilha Excel'}), 201
    except FileNotFoundError as e:
        return jsonify({
            "status": "erro",
            "message": f"Arquivo não encontrado: {e.filename}"
        }), 404

@app.route('/vendedores/calcularVolumeVendasPorCanal', methods=['POST'])
def calcular_volume_media_por_vendedor():
    try:
        calcular_volume_e_media_vendas(FILE_PATH_VENDAS)
        return jsonify({'success': 'Volume de vendas e média por profissional por canal calculados com sucesso'}), 201
    except FileNotFoundError as e:
        return jsonify({
            "status": "erro",
            "message": f"Arquivo não encontrado: {e.filename}"
        }), 404

if __name__ == '__main__':
    app.run(debug=True)
