#!/usr/bin/env python3
"""
Agente Bash con LangChain y Gemini Flash
Convierte prompts de usuario en comandos bash y los ejecuta de forma segura
"""

import os
import subprocess
import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage


class AgenteBash:
    def __init__(self, api_key=None):
        """
        Inicializa el agente bash con la API de Gemini Flash
        """
        if api_key is None:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("No se encontró la clave de API. Establece GOOGLE_API_KEY")
        
        # Configurar el modelo Gemini Flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.1,
            convert_system_message_to_human=True
        )
        
        # Prompt del sistema para generar comandos bash
        self.system_prompt = """Eres un experto en bash y comandos de terminal. 
Tu tarea es convertir las peticiones del usuario en comandos bash apropiados y seguros.

REGLAS IMPORTANTES:
1. Responde ÚNICAMENTE con el comando bash, sin explicaciones adicionales
2. No incluyas caracteres como ```bash``` o ``` en tu respuesta
3. Los comandos deben ser seguros y no destructivos
4. Si la petición no se puede convertir a un comando bash, responde "ERROR: No se puede convertir a comando bash"
5. Usa comandos estándar de bash/Unix
6. Para operaciones que requieren permisos especiales, usa sudo cuando sea apropiado

Ejemplos:
- Usuario: "listar archivos" → ls -la
- Usuario: "buscar archivos python" → find . -name "*.py"
- Usuario: "ver uso de disco" → df -h
- Usuario: "procesos en ejecución" → ps aux
"""

    def generar_comando_bash(self, prompt_usuario):
        """
        Genera un comando bash basado en el prompt del usuario
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt_usuario)
            ]
            
            response = self.llm.invoke(messages)
            comando = response.content.strip()
            
            # Limpiar la respuesta de posibles caracteres de markdown
            comando = comando.replace('```bash', '').replace('```', '').strip()
            
            return comando
            
        except Exception as e:
            return f"ERROR: Error al generar comando - {str(e)}"

    def ejecutar_comando(self, comando):
        """
        Ejecuta un comando bash de forma segura
        """
        try:
            result = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.stdout + result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            return "ERROR: El comando excedió el tiempo límite de 30 segundos", 1
        except Exception as e:
            return f"ERROR: Error al ejecutar comando - {str(e)}", 1

    def es_comando_peligroso(self, comando):
        """
        Verifica si un comando es potencialmente peligroso
        """
        comandos_peligrosos = [
            'rm -rf /', 'rm -rf /*', 'rm -rf ~', 'rm -rf $HOME',
            'dd if=/dev/zero', 'mkfs', 'fdisk', 'parted',
            'shutdown', 'reboot', 'halt', 'poweroff',
            'chmod 777 /', 'chown -R root:root /',
            '> /dev/sda', 'dd if=/dev/urandom'
        ]
        
        comando_lower = comando.lower().strip()
        return any(peligroso in comando_lower for peligroso in comandos_peligrosos)

    def ejecutar(self):
        """
        Bucle principal del agente bash
        """
        print("Agente Bash iniciado")
        print("Escribe 'exit' para salir")
        print("=" * 50)
        
        while True:
            try:
                prompt_usuario = input("\nTu petición: ").strip()
                
                if prompt_usuario.lower() in ['exit', 'salir', 'quit']:
                    print("Hasta luego!")
                    break
                
                if not prompt_usuario:
                    print("Por favor, escribe una petición válida.")
                    continue
                
                print("Generando comando bash...")
                comando = self.generar_comando_bash(prompt_usuario)
                
                if comando.startswith("ERROR:"):
                    print(f"Error: {comando}")
                    continue
                
                if self.es_comando_peligroso(comando):
                    print(f"COMANDO PELIGROSO DETECTADO: {comando}")
                    print("Este comando no será ejecutado por seguridad.")
                    continue
                
                print(f"Comando generado: {comando}")
                
                while True:
                    respuesta = input("¿Ejecutar este comando? (s/n): ").strip().lower()
                    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                        print("Ejecutando comando...")
                        salida, codigo = self.ejecutar_comando(comando)
                        
                        print("\nResultado:")
                        print("-" * 30)
                        if salida:
                            print(salida)
                        else:
                            print("(Sin salida)")
                        
                        print(f"\nCódigo de salida: {codigo}")
                        break
                        
                    elif respuesta in ['n', 'no']:
                        print("Comando cancelado.")
                        break
                    else:
                        print("Responde 's' para sí o 'n' para no.")
                
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
        
        agente = AgenteBash(api_key)
        agente.ejecutar()
        
    except ValueError as e:
        print(f"Error de configuración: {e}")
        print("\nPara usar este agente:")
        print("1. Obtén una API key de Google AI Studio: https://makersuite.google.com/app/apikey")
        print("2. Establece la variable de entorno: export GOOGLE_API_KEY='tu_api_key'")
        print("3. O pásala como argumento: python agente_bash.py tu_api_key")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
