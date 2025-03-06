from datetime import datetime
from typing import List

class ContaBancaria:
    """Classe que representa uma conta bancária com operações básicas."""
    
    def __init__(self, titular: str):
        self._titular = titular.strip().title()
        self._saldo = 0.0
        self._historico: List[str] = []
        self._taxa_saque = 2.0
        self._limite_saque_diario = 1000.0

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def titular(self) -> str:
        return self._titular

    def _registrar_operacao(self, mensagem: str) -> None:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._historico.append(f"[{data_hora}] {mensagem}")

    def depositar(self, valor: float) -> bool:
        try:
            if valor <= 0:
                raise ValueError("O valor do depósito deve ser positivo.")
            self._saldo += valor
            self._registrar_operacao(f"Depósito: R$ {valor:.2f}")
            return True
        except ValueError as e:
            print(f"Erro: {e}")
            return False

    def sacar(self, valor: float) -> bool:
        try:
            if valor <= 0:
                raise ValueError("O valor do saque deve ser positivo.")
            custo_total = valor + self._taxa_saque
            if custo_total > self._saldo:
                raise ValueError("Saldo insuficiente para realizar o saque.")
            if valor > self._limite_saque_diario:
                raise ValueError(f"Limite de saque diário é R$ {self._limite_saque_diario:.2f}")
            
            self._saldo -= custo_total
            self._registrar_operacao(f"Saque: R$ {valor:.2f} (Taxa: R$ {self._taxa_saque:.2f})")
            return True
        except ValueError as e:
            print(f"Erro: {e}")
            return False

    def extrato(self) -> None:
        print(f"\n=== Extrato da Conta de {self._titular} ===")
        if not self._historico:
            print("Nenhuma operação realizada ainda.")
        else:
            for operacao in self._historico:
                print(operacao)
        print(f"Saldo atual: R$ {self._saldo:.2f}")
        print("=" * 40)

class Cliente:
    """Classe que representa um cliente do banco."""
    
    def __init__(self, nome: str):
        self._nome = nome.strip().title()
        self._contas: List[ContaBancaria] = []

    @property
    def nome(self) -> str:
        return self._nome

    def adicionar_conta(self, conta: ContaBancaria) -> None:
        if conta.titular != self._nome:
            raise ValueError("O titular da conta deve ser o mesmo que o cliente.")
        self._contas.append(conta)

    def listar_contas(self) -> List[ContaBancaria]:
        return self._contas

class Banco:
    """Classe que gerencia clientes e suas contas."""
    
    def __init__(self, nome: str):
        self._nome = nome
        self._clientes: List[Cliente] = []

    def adicionar_cliente(self, cliente: Cliente) -> None:
        self._clientes.append(cliente)

    def buscar_cliente(self, nome: str) -> Cliente | None:
        for cliente in self._clientes:
            if cliente.nome == nome.strip().title():
                return cliente
        return None

def obter_valor(mensagem: str) -> float:
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Por favor, digite um valor numérico válido.")

def menu_operacoes() -> str:
    print("\n=== Sistema Bancário ===")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Ver Extrato")
    print("4. Sair")
    return input("Escolha uma operação (1-4): ").strip()

def main():
    banco = Banco("xAI Bank")
    print("Seja bem-vindo!")
    
    while True:
        try:
            nome = input("Digite o nome do titular da conta: ").strip()
            if not nome:
                raise ValueError("O nome não pode ser vazio.")
            break
        except ValueError as e:
            print(f"Erro: {e}")

    cliente = Cliente(nome)
    conta = ContaBancaria(cliente.nome)
    cliente.adicionar_conta(conta)
    banco.adicionar_cliente(cliente)
    print(f"Conta criada com sucesso para {cliente.nome} no {banco._nome}!")

    operacoes = {
        '1': lambda: conta.depositar(obter_valor("Valor a depositar: R$ ")),
        '2': lambda: conta.sacar(obter_valor("Valor a sacar: R$ ")),
        '3': conta.extrato,
        '4': lambda: "sair"
    }

    while True:
        opcao = menu_operacoes()
        
        if opcao in operacoes:
            if opcao == '4':
                print(f"Obrigado por usar nossos serviços, {cliente.nome}!")
                break
            resultado = operacoes[opcao]()
            if resultado is True:
                print("Operação realizada com sucesso!")
        else:
            print("Opção inválida! Por favor, escolha entre 1 e 4.")

if __name__ == "__main__":
    main()