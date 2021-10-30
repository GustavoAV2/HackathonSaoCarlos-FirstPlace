from json import JSONDecodeError

from requests import request


def validate_address(cep: str) -> dict or None:
    response = request("Get", url=f"https://viacep.com.br/ws/{cep}/json/")
    try:
        response_json = response.json()
    except JSONDecodeError:
        return None
    response_json = {
            "logradouro": response_json.get('logradouro'),
            "complemento": response_json.get('complemento'),
            "bairro": response_json.get('bairro'),
            "localidade": response_json.get('localidade'),
            "uf": response_json.get('uf'),
            "cep": response_json.get('cep')
        }
    return response_json
