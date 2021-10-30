from brutils import cpf, cnpj


def validate_cpf(cpf_number: str) -> bool:
    return cpf.validate(cpf_number)


def validate_cnpj(cnpj_number: str) -> bool:
    return cnpj.validate(cnpj_number)
