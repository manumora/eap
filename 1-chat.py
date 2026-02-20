#!/usr/bin/env python3
"""
Agente de Chat con LangChain y Gemini Flash
Permite hacer preguntas y obtener respuestas de Gemini sobre cualquier tema
"""

import os
import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage


class Chat:
    def __init__(self, api_key=None):
        """
        Inicializa el agente de chat con la API de Gemini Flash
        """
        if api_key is None:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("No se encontró la clave de API. Establece GOOGLE_API_KEY")
        
        # Configurar el modelo Gemini Flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Prompt del sistema para un asistente general
        self.system_prompt = """Eres un asistente de IA útil y amigable. 
Responde las preguntas del usuario de manera clara, precisa y útil.
Si no estás seguro de algo, es mejor decirlo que inventar información.
Responde en español a menos que el usuario pida específicamente otro idioma.
"""

    def obtener_respuesta(self, pregunta):
        """
        Obtiene una respuesta de Gemini para la pregunta del usuario
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=pregunta)
            ]
            
            response = self.llm.invoke(messages)
            return response.content.strip()
            
        except Exception as e:
            return f"Error al obtener respuesta: {str(e)}"

    def ejecutar(self):
        """
        Bucle principal del chat
        """
        print("Chat iniciado")
        print("Escribe 'exit' para salir")
        print("=" * 50)
        
        while True:
            try:
                pregunta = input("\nTu pregunta: ").strip()
                
                if pregunta.lower() in ['exit', 'salir', 'quit']:
                    print("Hasta luego!")
                    break
                
                if not pregunta:
                    print("Por favor, escribe una pregunta válida.")
                    continue
                
                print("Pensando...")
                respuesta = self.obtener_respuesta(pregunta)
                
                print("\nRespuesta:")
                print("-" * 30)
                print(respuesta)
                print("-" * 30)
                
            except KeyboardInterrupt:
                print("\n\nHasta luego!")
                break
            except Exception as e:
                print(f"Error inesperado: {str(e)}")


def main():
    """
    Función principal
    """
    try:
        api_key = None
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
        
        agente = Chat(api_key)
        agente.ejecutar()
        
    except ValueError as e:
        print(f"Error de configuración: {e}")
        print("\nPara usar este chat:")
        print("1. Obtén una API key de Google AI Studio: https://makersuite.google.com/app/apikey")
        print("2. Establece la variable de entorno: export GOOGLE_API_KEY='tu_api_key'")
        print("3. O pásala como argumento: python 1-chat.py tu_api_key")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
