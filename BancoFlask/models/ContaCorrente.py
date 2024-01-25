# Definindo a classe conta corrente
class ContaCorrente:
    # Função que inicializa os atributos da 
    def __init__(self, titular ,numero, saldo, chequeEspecial, senha, cargo) -> None:
        # Inicialização dos atributos da conta corrente
        self.titular = titular
        self.numero = numero
        self.saldo = saldo
        self.chequeEspecialAtual = chequeEspecial
        self.chequeEspecial = chequeEspecial
        self.senha = senha
        self.cargo = cargo

    # Função que realiza o saque de uma conta
    def realizarSaque(self, valor):
        # Verifica se o valor do saque é válido em relação ao saldo e ao cheque especial
        if self.saldo + self.chequeEspecialAtual < valor:
            return False  # Retorna False se não houver saldo suficiente
        else:
            # Realiza o saque, primeiro do saldo e, se necessário, do cheque especial
            if self.saldo >= valor:
                self.saldo -= valor
            else:
                self.chequeEspecialAtual -= valor - self.saldo
        return True  # Retorna True indicando que o saque foi bem-sucedido

    # Função que realiza o depósito para uma conta
    def realizarDeposito(self, valor):
        # Verifica se o valor do depósito é válido
        if valor <= 0:
            return False  # Retorna False se o valor do depósito for inválido
        else:
            self.saldo += valor  # Realiza o depósito adicionando ao saldo
        return True  # Retorna True indicando que o depósito foi bem-sucedido
    
    # Função que realiza a transferência de uma valor para uma conta
    def realizarTransferencia(self, contaDestino, valor, senha):
        # Verifica condições para realizar a transferência
        if valor <= 0:
            return "VALOR_INVALIDO"
        if self.saldo + self.chequeEspecialAtual < valor:
            return "SALDO_INSUFICIENTE"
        if self == contaDestino:
            return "MESMA_CONTA"
        if not self.validarSenha(senha):
            return "SENHA_INCORRETA"
        
        # Realiza a transferência subtraindo o valor da conta de origem e adicionando na conta de destino
        self.saldo -= valor
        contaDestino.saldo += valor
        return "TRANSFERENCIA_REALIZADA"
    
    # Função que calcula a quantidade de cheque especial que foi utilizada
    def pegarQuantidadeChequeEspecialUtilizado(self):
        # Retorna a quantidade de cheque especial utilizado
        return self.chequeEspecial - self.chequeEspecialAtual
    
    # Função que valida a senha da conta
    def validarSenha(self, senhaPadrao) -> bool:
        # Verifica se a senha fornecida é igual à senha da conta
        return self.senha == senhaPadrao