from requests import request


def validate_address(cep: str) -> dict:
    response = request("Get", url=f"https://viacep.com.br/ws/{cep}/json/")
    response_json = response.json()
    response_json = {
            "logradouro": response_json.get('logradouro'),
            "complemento": response_json.get('complemento'),
            "bairro": response_json.get('bairro'),
            "localidade": response_json.get('localidade'),
            "uf": response_json.get('uf'),
            "cep": response_json.get('cep')
        }
    return response_json
