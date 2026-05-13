from spyne import Application, rpc, ServiceBase, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple

class CalculadoraService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def somar(ctx, a, b):
        return a + b

    @rpc(Integer, Integer, _returns=Integer)
    def subtrair(ctx, a, b):
        return a - b

    @rpc(Integer, Integer, _returns=Integer)
    def multiplicar(ctx, a, b):
        return a * b

    @rpc(Integer, Integer, _returns=Integer)
    def dividir(ctx, a, b):
        if b == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return a // b

app = Application(
    [CalculadoraService],
    tns='br.ufrn.tads.calculadora',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    print("Servidor SOAP Calculadora rodando em http://localhost:8000/")
    print("WSDL disponível em: http://localhost:8000/?wsdl")
    run_simple('localhost', 8000, wsgi_app)