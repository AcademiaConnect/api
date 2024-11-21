import openai
import os
import json
from datetime import date
from dotenv import load_dotenv

def get_event_by_gpt(input) -> dict:
    # definindo a chave da api, alterar aqui
    
    #aqui usei o dotenv, alterar depois
    load_dotenv()
    
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # prompt para o api
    prompt = f"""
                Extraia as seguintes informações do texto abaixo e organize-as em campos pré-definidos. Caso o campo "título" ou "descrição" não estejam claros no texto, gere-os com base nas informações disponíveis no próprio texto.

                Campos a serem extraídos:

                Título (se não houver, crie um título adequado com base no texto)
                Data inicial
                Data final
                Localização
                Descrição (se não houver, crie uma descrição baseada no conteúdo do texto)

                Texto:
                {input}

                Organize a resposta apenas nos seguintes campos:
                {{
                    "title": "título extraído"
                    "dateInitial": "data inicial extraída"
                    "dateFinal": "data final extraída"
                    "location": "endereço extraída"
                    "description": "descrição extraída"
                }}    

                Se alguma informação não estiver presente ou for incompleta, deixe o campo como null. Pode ser bem criativo na descrição, limitando os caracteres até 230.

                Caso seja solicitado alguma data, hoje é {str(date.today())}
            """

    # requisição para a api
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente na criação de eventos bastante criativo."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # resposta da api
    evento = completion.choices[0].message.content

    # transformando em json
    event_data = json.loads(evento)

    # para depurar
    #print(f"Tipo do json: {type(event_data)}\nResposta do GPT: {evento}")

    # retorno da função
    return event_data

