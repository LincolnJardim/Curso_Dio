from abc import ABC, abstractmethod, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap
class Cliente:
    def __init__(self, _endereco):
        self.endereco = _endereco
        self._contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    
    def __init__(self, nome, data_nascimento, cpf, endereco):

        super().__init__(endereco)

        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

class Conta:
    
  def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

  @classmethod
  def nova_conta(cls, cliente, numero):
      return cls(numero, cliente)
  
  @property
  def saldo(self):
    return self._saldo
    
  @property
  def numero(self):
      return self._numero
  
  @property
  def agencia(self):
      return self._agencia
  
  @property
  def cliente(self):
      return self._cliente
  
  def historico(self):
      return self._historico

    
  def sacar(self, valor):
      saldo = self.saldo
      
      if valor > saldo:
          print("\n XXX Operação falhou! Você não tem saldo suficiente.")

      elif saldo < valor:
          print('\n === Saque realizado com sucesso! ===')
          return True
      
      else:
          print('\n XXX Operação falhou! O valor informado é inválido. XXX')
      return False


   
  def depositar(self, valor):
      
      if valor > 0:
        self._saldo += valor
        
        print('\n=== Depósito realizado com sucesso! ===')
        
      else:
        print("\nXXX Operação falhou! O valor informado é inválido. XXX")
        return False
      
      return True
          
    
class ContaCorrente(Conta):
   
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
       super().__init__(numero, cliente)
       self.limite = limite
       self.limite_saque = limite_saques

    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self._historico.transacoes if transacao["tipo"]  == Saque.__name__]
        )
        
        if numero_saques > self.limite_saque:
            print("XXX Operação falhou! Você atingiu o número limite de saques diário.")

        elif valor > self.limite:
            print("XXX Operação falhou! O saque excede o limite da sua conta.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C: \t\t{self.numero}
            Titular:\t{self.cliente.nome}
          """
      

class Historico:
    def __init__(self):
       self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
           self._transacoes.append(
               {
                   "tipo": transacao.__class__.__name__,
                   "valor": transacao.valor,
                   "data": datetime.now().strftime
                   ("%d-%m-%Y %H:%m:%s"),
               }
           )

class Transação(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transação):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registar(self, conta):
      sucesso_transacao = conta.depositar(self.valor)

      if sucesso_transacao:
          conta.historico.adicionar_transacao(self)

class Saque(Transação):
    
    def __init__(self, valor):
        
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():

    menu_texto = """\n
========== MENU ==========
[D]  Depositar
[S]  Sacar
[E]  Extrato
[NU] Novo Usuário
[NC] Nova Conta
[LC] Listar Contas
[Q]  Sair
==========================
=> """ 
    return input(menu_texto).strip().upper()





def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(clientes):
    if not clientes.contas:
        print('\n XXX Cliente não possui conta! XXX')
        return
    
    return clientes.contas[0]


def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('|n XXX Cliente não eoncontrado! XXX')
        return
    
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nXXX Cliente não encontrado! XXX')
        return
    
    valor = input('Informe o valor do saque: ')
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nXXX Cliente não encontrado! XXX')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("|n=============== EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}'


    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('============================================')


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente =  filtrar_cliente(cpf, clientes)

    if cliente:
        print('\nXXX Já existe um cliente com esse CPF! XXX')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa)')
    endereco = input('Informe o edereço completo (logradouro, número - bairro - cidade/sigla estado): )')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('\n === Cliente criado com sucesso! ===')


def criar_conta(numero_conta, clientes, contas):


    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nXXX Cliente não encontrado! Fluxo de criação de conta encerrado. XXX')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    clientes.contas.append(conta)

    print('\n === Conta criada com sucesso! ===')


def listar_contas(contas):
    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta)))



def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'D':
            depositar(clientes)

        elif opcao == 'S':
            sacar(clientes)
        
        elif opcao == 'E':
            exibir_extrato(clientes)

        elif opcao == "NU":
            criar_cliente(clientes)
        
        elif opcao == 'NC':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 'LC':
            listar_contas(contas)
        
        elif opcao == 'Q':
            break

        else:
            print('Opção inválida, digite novamente a opção desejada!')


main()