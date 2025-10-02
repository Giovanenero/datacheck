import re
from querie import consulta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",  # dev
    "http://fswmldev01.wise.corp:4223",  # prod
    # pode usar "*" para liberar tudo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pessoa")
def pessoa(cpf:str, nome:str, nascimento:str):
    try:

        cpf = re.sub(r'[^0-9]', '', cpf)

        if len(cpf) != 11:
            return {
                'data': {},
                'message': 'CPF inválido'
            }
        
        cpf = f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}' 

        data = consulta(cpf)

        return {
            'projudi': data,
            'message': 'OK'
        }

    except Exception as e:
        return {
            'projudi': None,
            'message': str(e)
        }