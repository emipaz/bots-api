from collections import deque
from utils import consulta_con_funcion, consulta, rol_content_func
from utils import consulta_dolar


def main():
    
    memoria = deque(maxlen=20) # memoria de 20 mensajes incliuyendo las respuestas
    
    while True:
        mensaje = input(">> ")
        # opcion de terminar el chat
        if mensaje == "exit()":
            break
        # guardamos el mensaje del usuario
        memoria.append({
                        "role": "user",
                        "content": mensaje  
                        })
        # realizamos la consulta si hay una función como plug_in 
        response = consulta_con_funcion(list(memoria))
        rol, content, datos_funcion = rol_content_func(response)
        # si hay una función como plug_in, la ejecutamos
        if datos_funcion:
            func, argumentos = datos_funcion
            if func == "consulta_dolar":
                datos_dolar = consulta_dolar()
                #agregamos la respuesta de la función como plug_in a la memoria
                memoria.append({
                                "role": "function",
                                "name": func,
                                "content": datos_dolar}
                                )
                #consultamos nuevamente pero la funcion simple de chat
                response_dolar = consulta(list(memoria))
                rol, content, _ = rol_content_func(response_dolar)
        # gueradamos la respuesta de chat-gpt en la memoria
        memoria.append({
                        "role": rol,
                        "content": content  
                        })
        #mostramos la respuesta al usuario
        print("Chat :", content)
        
main()