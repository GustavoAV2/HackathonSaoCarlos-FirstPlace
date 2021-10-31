from settings import URL_APP

links = {
    1: lambda _id: f'Envie a proposta para o financeiro através do link: {URL_APP}/next_level/{_id}',
    2: lambda _id: f'Aprovar: {URL_APP}request/approve/{_id}\nNegar: {URL_APP}request/decline/{_id}',
}

