from zeep import Client

def testar_servico_local():
    print("--- Testando Serviço SOAP Local (Calculadora) ---")
    wsdl_local = 'http://localhost:8000/?wsdl'
    
    try:
        cliente_local = Client(wsdl=wsdl_local)
        
        a, b = 10, 5
        print(f"Somar {a} + {b} = {cliente_local.service.somar(a, b)}")
        print(f"Subtrair {a} - {b} = {cliente_local.service.subtrair(a, b)}")
        print(f"Multiplicar {a} * {b} = {cliente_local.service.multiplicar(a, b)}")
        print(f"Dividir {a} / {b} = {cliente_local.service.dividir(a, b)}")
    except Exception as e:
        print(f"Erro ao conectar no serviço local: {e}")
        print("Certifique-se de que o servidor_calculadora.py está rodando.")

def testar_servico_externo():
    print("\n--- Testando Serviço SOAP Externo (NumberConversion) ---")
    wsdl_externo = 'https://www.dataaccess.com/webservicesserver/NumberConversion.wso?WSDL'
    
    try:
        cliente_externo = Client(wsdl=wsdl_externo)
        
        numero = 2026
        resultado = cliente_externo.service.NumberToWords(ubiNum=numero)
        print(f"O número {numero} por extenso em inglês é: {resultado.strip()}")
    except Exception as e:
        print(f"Erro ao conectar no serviço externo: {e}")

if __name__ == '__main__':
    testar_servico_local()
    testar_servico_externo()