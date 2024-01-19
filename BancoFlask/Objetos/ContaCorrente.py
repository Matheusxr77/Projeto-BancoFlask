class ContaCorrente:
    def __init__(self, titular ,numero, saldo, chequeEspecial, senha, cargo) -> None:
        self.titular = titular
        self.numero = numero
        self.saldo = saldo
        self.chequeEspecialAtual = chequeEspecial
        self.chequeEspecial = chequeEspecial
        self.senha = senha
        self.cargo = cargo
        
    def realizarSaque(self, valor):
        if self.saldo + self.chequeEspecialAtual < valor:
            return False
        else:
            if self.saldo >= valor:
                self.saldo -= valor
            else:
                self.chequeEspecialAtual -= valor - self.saldo
        return True
    
    def realizarDeposito(self, valor):
        if valor <= 0:
            return False
        else:
            self.saldo += valor
        return True
    
    def realizarTransferencia(self, contaDestino, valor, senha):
        if valor <= 0:
            return "VALOR_INVALIDO"
        if self.saldo + self.chequeEspecialAtual < valor:
            return "SALDO_INSUFICIENTE"
        if self == contaDestino:
            return "MESMA_CONTA"
        if not self.validarSenha(senha):
            return "SENHA_INCORRETA"
        self.saldo -= valor
        contaDestino.saldo += valor
        return "TRANSFERENCIA_REALIZADA"
    
    def pegarQuantidadeChequeEspecialUtilizado(self):
        return self.chequeEspecial - self.chequeEspecialAtual

    def validarSenha(self, senhaPadrao) -> bool:
        return self.senha == senhaPadrao