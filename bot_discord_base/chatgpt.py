import openai

import os
__import__("sys").path.append('../..')
from collections import deque

from dotenv import load_dotenv

load_dotenv()

openai_key     = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_key

cliente = openai.OpenAI()

chats = dict()

def leer(us):
    chats[us] = chats.get(us, deque(maxlen=10))
    return chats
    
def gpt(us, entrada):
    
    chats = leer(us)
    chats[us].append(entrada)
    
    # TODO remove old messages reveer si es necesario 
    while (tokens := sum ( [len(x.split()) for x in chats[us]])) > 2048:
        chats[us].popleft()
    # 
    
    prompt = [{"role": "user", "content": x} for x in chats[us]]

    completion = cliente.chat.completions.create(
                    model       = "gpt-3.5-turbo", 
                    messages    = prompt,
                    temperature = 1,
                    max_tokens  = 2048)
    chats[us].append(completion.choices[0].message.content)
    return completion.choices[0].message.content

def chat (entrada):
    completion = cliente.completions.create(
        model ="gpt-3.5-turbo-instruct",
        prompt = entrada,
        max_tokens = 2048)
    return completion.choices[0].text

def imagen(mensaje):

    response = cliente.images.generate(
            model="dall-e-3",
            prompt = mensaje,
            n = 1, # cantidad de imagenes puede ir de 1 a 10
            size = "1024x1024"
        )
    url = response.model_dump()["data"][0]["url"]
    return  url