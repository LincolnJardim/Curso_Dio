import textwrap

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

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato +=(f"Depósito:\tR${valor:.2f}\n")
        print('\n=== Depósito realizado com sucesso! ===')
    else:
        print("\nXXX Operação falhou! O valor informado é inválido. XXX")
        
    return saldo, extrato
    
def sacar(*, saque, saldo, limite, extrato,  limite_saques, numero_saques):

    if numero_saques >= limite_saques:
        print("XXX Operação falhou! Você atingiu o número limite de saques diário.")
    elif limite > saque:
        limite = saque > saldo
        print("XXX Operação falhou! O saque escede o limite da sua conta.")

    elif saque <= saldo:
        saldo -= saque
        extrato += f'Saque:\t\tR$ {saque:.2f}\n'
        numero_saques += 1  # Atualiza só quando o saque for efetuado
        print(f"O valor R${saque:.2f} foi sacado de sua conta.\nO saldo atual da sua conta é: R${saldo:.2f}")
    
    else:
        print("Operação falhou! Você não possui saldo suficiente.")
    
    return saldo, numero_saques  # Para atualizar os valores fora da função


def exibir_extrato(saldo, /, *, extrato):
        titulo = "Extrato"
        print(titulo.center(20, '='))

        
        if extrato == "":
            print('Não foram realizadas movimentações.')
        else:
            print(extrato)
            print(f'\nSeu saldo atual é \t\tR${saldo:.2f}')

    
def criar_usuario(usuarios):
    cpf = input("Informe seu CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    for usuario in usuarios:

        if usuario["cpf"] == cpf:
            print("Usuário já cadastrado!")
            return
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input('Informe sua data de nascimento (dd/mm/aaaa): ')
    endereco = input('Informe o endereço (logradouro, número - bairro - cidade/estado):')

    novo_usuario = {
        'nome': nome,
        'cpf': cpf,
        'data_nascimento': data_nascimento,
        'endereco': endereco,
    }

    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")
    

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_conta(agencia, numero_conta, usuarios):
        cpf = input('Informe o CPF do usuário:')
        usuario = filtrar_usuario(cpf, usuarios)

        if usuario:
            print('\n=== Conta criada com sucesso! ===')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
        
        print("\nXXX Usuário não encontrato, fluxo de criação de conta encerrado! XXX")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    numero_saques = 0
    extrato = ""
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'D':
            print("Depósito")
            
            valor = float(input('Digite o valor do deposito: '))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 'S':
            print('Saque') 

            saque = float(input('Digite o valor do saque: '))

            saldo, extrato = sacar(
                saldo=saldo,
                saque=saque,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
        
        elif opcao == 'E':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "NU":
            criar_usuario(usuarios)
        
        elif opcao == 'NC':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 'LC':
            listar_contas(contas)
        
        elif opcao == 'Q':
            break

        else:
            print('Opção inválida, digite nomanete a opção desejada!')



main()



