from flask import Flask, request, jsonify, make_response
from Vendedor import GerenciarVendedor, Vendedor
from Excel_functions import criar_atualizar_em_lotes, calcular_comissoes, calcular_volume_e_media_vendas

app = Flask(__name__)

gerenciadorVendedor = GerenciarVendedor()
FILE_PATH_VENDAS = 'Vendas.xlsx'
FILE_PATH_VENDEDORES = "planilha_vendedores.xlsx"

@app.route('/vendedores', methods=['POST'])
def create_vendedor():
    data = request.json
    vendedor = Vendedor(data['nome'], data['cpf'], data['data_nascimento'], data['email'], data['estado'])
    gerenciadorVendedor.create_vendedor(vendedor)

    resposta = {
        "message": "Vendedor criado com sucesso",
        "data": {
            "nome": vendedor.nome,
            "cpf": vendedor.cpf,
            "data_nascimento": str(vendedor.data_nascimento),
            "email": vendedor.email,
            "estado": vendedor.estado
        }
    }

    return jsonify(resposta), 201

@app.route('/vendedores/<cpf>', methods=['GET'])
def get_vendedor(cpf):
    vendedor = gerenciadorVendedor.read_vendedor(cpf)
    if vendedor:
        return jsonify({"cpf": vendedor[0], "nome": vendedor[1], "data_nascimento": vendedor[2], "email": vendedor[3], "estado": vendedor[4]}), 200
    return jsonify({"message": "Vendedor não encontrado"}), 404

@app.route('/vendedores/<cpf>', methods=['PUT'])
def update_vendedor(cpf):
    vendedor_existente = gerenciadorVendedor.read_vendedor(cpf)

    if vendedor_existente:
        data = request.json
        vendedor = Vendedor(data['nome'], data['cpf'], data['data_nascimento'], data['email'], data['estado'])
        print(vendedor.nome, vendedor.cpf)
        gerenciadorVendedor.update_vendedor(vendedor)
        return jsonify({
            "status": "successo",
            "message": f"Vendedor com CPF {cpf} atualizado com sucesso"
        }), 200
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
            "status": "error",
            "message": f"Vendedor com CPF {cpf} não encontrado"
        }), 404

@app.route('/vendedores', methods=['GET'])
def get_all_vendedores():
    vendedores = gerenciadorVendedor.read_all_vendedores()
    return jsonify([{"cpf": v[0], "nome": v[1], "data_nascimento": v[2], "email": v[3], "estado": v[4]} for v in vendedores]), 200

@app.route('/vendedores/planilha', methods=['POST'])
def update_planilha_vendedor():
    lista_de_vendedores = criar_atualizar_em_lotes(FILE_PATH_VENDEDORES)

    vendedores_json = []
    for vendedor in lista_de_vendedores:
        vendedor_dict = {
            'Nome': vendedor.nome,
            'CPF': vendedor.cpf,
            'Data de Nascimento': vendedor.data_nascimento,
            'Email': vendedor.email,
            'Estado': vendedor.estado
        }
        vendedores_json.append(vendedor_dict)

    return jsonify({"message": "Vendedores atualizados ou adicionados", "vendedores": vendedores_json}), 201

@app.route('/vendedores/calcularComissao', methods=['POST'])
def calcular_planilha_vendedor():
    calcular_comissoes(FILE_PATH_VENDAS)

    return jsonify({'success': 'Comissões calculadas sucesso'}), 201

@app.route('/vendedores/calcularVolumeVendasPorCanal', methods=['POST'])
def calcular_volume_media_por_vendedor():
    calcular_volume_e_media_vendas(FILE_PATH_VENDAS)

    return jsonify({'success': 'Volume de vendas e média por profissional por canal calculadao com sucesso'}), 201

if __name__ == '__main__':
    app.run(debug=True)
