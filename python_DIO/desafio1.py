menu = """
====== Menu ====== 
    [D] Depositar
    [S] Sacar
    [E] Extrato
    [Q] Sair
    
 ================= 
    =>"""

saldo = 0
limite = 500
numero_saques = 0
extrato = ""
LIMITE_SAQUE = 3


while True:

    opcao = input(menu).upper()
    

    if opcao == 'D':
        print("Depósito")
        novo_deposito = float(input('Digite o valor do deposito: '))
        saldo += novo_deposito
        if novo_deposito > 0:
            extrato += f"Novo deposito: R${novo_deposito:.2f}\n"
            print(f'Seu saldo atual é R$ {saldo:.2f} reais')
        else:
            print("Valor inválido!")
            




    elif opcao == 'S':
        print('Saque')
        
        
        if numero_saques > LIMITE_SAQUE:
            print('Você atingiu o numero máximo de saque diários!') 
        else: 
            novo_saque = int(input('Digite o valor que deseja sacar: '))
        
            if novo_saque > saldo:
                print("Saldo insuficiente")
            
            elif novo_saque > limite:
                print('O valor digitado excede o limite de R$500,00 por saque!')
            
            elif novo_saque < 0:
                print('Valor inválido. O valor deve ser maior que zero.')

            else:
                numero_saques += 1  
                saldo -= novo_saque
                extrato += f"Novo saque: R${novo_saque:.2f}\n"
                
                print(f"Saque de R${novo_saque:.2f} realizado com sucesso. Saldo atual: R${saldo:.2f}")

                
            


            
    elif opcao == 'E':
        titulo = 'Extrato'
        print(titulo.center(20, '='))
        
        if extrato == "":
            print('Não foram realizadas movimentações.')
        else:
            print(extrato)
            print(f'Seu saldo atual é R{saldo:.2f}')

       

        
    
        
        

        
            


                  
                     
            

    

    elif opcao == 'Q':
        print("Obrigado por usar nosso sistema bancário. Até mais!")
        
        break
    
    else:
        print('Opção inválida, tente novamente!')