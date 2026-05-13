from zeep import Client

def iniciar_cliente(url_wsdl):
    try:
        return Client(wsdl=url_wsdl)
    except Exception as e:
        print(f"Erro ao conectar no WSDL: {e}")
        return None

def menu():
    server = 'http://localhost:8000/?wsdl' # serviço interno (calculadora)
    # server = 'https://www.dataaccess.com/webservicesserver/NumberConversion.wso?WSDL' # serviço interno (conversão de números em palavras)
    wsdl_url = server
    
    print(f"Lendo e decodificando o contrato WSDL de: {wsdl_url} ...")
    cliente = iniciar_cliente(wsdl_url)
    if not cliente:
        return

    metodos_disponiveis = [m for m in dir(cliente.service) if not m.startswith('_')]

    while True:
        print("\n" + "=" * 50)
        print("  CLIENTE - LEITOR DE WSDL  ")
        print("=" * 50)
        
        print("0 - Sair")

        for indice, nome in enumerate(metodos_disponiveis):
            print(f"{indice + 1} - {nome}")
        
        print("=" * 50)
        
        opcao = input("\nEscolha a operação pelo número: ").strip()

        if opcao == '0':
            break
            
        try:
            indice_escolhido = int(opcao) - 1
            if 0 <= indice_escolhido < len(metodos_disponiveis):
                comando = metodos_disponiveis[indice_escolhido]
                print(f"\n--- Executando: {comando} ---")
                
                operacao_wsdl = cliente.service._binding._operations[comando]
                
                tipo_entrada = operacao_wsdl.input.body.type
                
                argumentos = {}
                
                if hasattr(tipo_entrada, 'elements') and tipo_entrada.elements:
                    for nome_parametro, elemento_wsdl in tipo_entrada.elements:

                        tipo_esperado = elemento_wsdl.type.name if elemento_wsdl.type else 'desconhecido'
                        
                        valor_bruto = input(f"Digite o valor para '{nome_parametro}' (tipo esperado: {tipo_esperado}): ")
                        
                        if 'int' in tipo_esperado.lower() or 'decimal' in tipo_esperado.lower():
                            try:
                                argumentos[nome_parametro] = int(valor_bruto)
                            except ValueError:
                                argumentos[nome_parametro] = valor_bruto
                        else:
                            argumentos[nome_parametro] = valor_bruto
                else:
                    print("(Este método não exige parâmetros de entrada)")

                print("\n")

                # PROCESSAMENTO
                print("Enviando Envelope SOAP para o servidor...")
                
                funcao_remota = getattr(cliente.service, comando)
                
                resultado = funcao_remota(**argumentos)
                
                print(f">>> RESULTADO OBTIDO: {resultado}")
                
            else:
                print("Opção inválida.")
                
        except ValueError:
            print("Erro: Digite um número válido do menu.")
        except Exception as e:
             print(f"Falha na comunicação ou erro no servidor: {e}")

if __name__ == '__main__':
    menu()