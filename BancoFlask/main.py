# Importando a biblioteca Flask
from flask import *

# Importando a classe ContaCorrente do módulo models.ContaCorrente
from models.ContaCorrente import ContaCorrente

# Criando a aplicação Flask
webApp = Flask(__name__)

# Definindo a chave secreta para a sessão da aplicação
webApp.secret_key = 'UFAPE'

# Criando duas instâncias da classe ContaCorrente
conta1 = ContaCorrente("Matheus", 1234, 1000, 5000, "teus", "adm")
conta2 = ContaCorrente("Mayara", 12345, 5000, 10000, "12345", "user")

# Criando uma lista de contas
listaContas = [conta1, conta2]

# Função que retorna a conta do usuário logado
def contaUsuario():
    for conta in listaContas:
        if conta.titular == session['usuario_logado']:
            return conta

# Função que retorna a conta com o número especificado
def pegarContaPeloNumero(numero):
    for conta in listaContas:
        if conta.numero == numero:
            return conta
    return None

# Função que verifica se o usuário está logado
def usuarioLogado() -> bool:
    if session["usuario_logado"] == None or 'usuario_logado' not in session:
        return False
    return True

# Função que verifica se um usuário com o login especificado existe
def usuarioExiste(login) -> bool:
    for usuario in listaContas:
        if usuario.titular == login:
            return True
    return False

# Função que retorna a conta associada ao login especificado
def pegarUsuario(login) -> ContaCorrente:
    for usuario in listaContas:
        if usuario.titular == login:
            return usuario
    return None

# Rota que renderiza a página principal se o usuário estiver logado, caso contrário redireciona para a página de login
@webApp.route("/main")
def main():
    if usuarioLogado():
        return render_template("index.html", cargo=session['nivel'], usuario=session['usuario_logado'], conta=contaUsuario())
    else:
        return redirect("/login")

# Rota que renderiza a página de login
@webApp.route("/")
def pre_render():
    return render_template("login.html")

# Rota que renderiza a página de status se o usuário estiver logado como usuário comum
@webApp.route("/status")
def status():
    if usuarioLogado() and session['nivel'] == 'user':
        return render_template("status.html", conta=contaUsuario())
    else:
        flash("Usuário sem permissão!")
        return redirect("/main")

# Rota que renderiza a página de listagem de contas se o usuário estiver logado como administrador
@webApp.route('/contas')
def listagemDeContas():
    if usuarioLogado() and session['nivel'] == 'adm':
        return render_template("listaContas.html", contas=listaContas)
    else:
        flash("Usuário sem permissão!")
        return redirect("/main")

# Rota que renderiza a página de criação de conta se o usuário estiver logado como administrador
@webApp.route("/criarConta")
def criarConta():
    if usuarioLogado() and session['nivel'] == 'adm':
        return render_template("criarConta.html")
    else:
        flash("Usuário sem permissão!")
        return redirect("/main")

# Rota que cadastra uma nova conta com os dados fornecidos
@webApp.route("/cadastrarConta", methods=["POST", ])
def cadastrarConta():
    titular = request.form["titular"]
    numero = int(request.form["numero"])
    saldo = float(request.form["saldo"])
    chequeEspecial = float(request.form["chequeEspecial"])
    senha = request.form["senha"]
    cargo = request.form["cargo"]

    conta = ContaCorrente(titular, numero, saldo, chequeEspecial, senha, cargo)
    listaContas.append(conta)

    return redirect("/contas")

# Rota que exclui uma conta com o índice fornecido na URL
@webApp.route('/excluir/<int:index>')
def excluirConta(index):
    listaContas.pop(index)
    return redirect('/contas')

# Rota que renderiza a página de edição de conta com os dados da conta no índice especificado na URL
@webApp.route('/editar/<int:index>')
def telaEditarConta(index):
    return render_template('editarConta.html', titulo="Alterar Conta", conta=listaContas[index], index=index)

# Rota que atualiza os dados de uma conta com base nos dados fornecidos no formulário de edição
@webApp.route('/update', methods=['POST', ])
def updateFilme():
    index = int(request.form["index"])
    conta = listaContas[index]

    conta.titular = request.form["titular"]
    conta.numero = int(request.form["numero"])
    conta.saldo = float(request.form["saldo"])
    conta.chequeEspecial = float(request.form["chequeEspecial"])
    conta.senha = request.form["senha"]
    conta.cargo = request.form["cargo"]
    
    return redirect('/contas')

# Rota que renderiza a página de saque se o usuário estiver logado como usuário comum
@webApp.route("/saque")
def saque():
    if usuarioLogado() and session['nivel'] == 'user':
        return render_template("saque.html")
    else:
        flash("Usuário sem permissão!")
        return redirect("/main")
    
# Rota que processa o saque com base nos dados fornecidos no formulário
@webApp.route("/sacar", methods=["POST", ])
def sacar():
    numero = int(request.form["numero"])
    valorSaque = float(request.form["valorSaque"])

    conta = pegarContaPeloNumero(numero)

    if conta is None:
        flash(f"Conta com número {numero} não encontrada!")
        return redirect("/saque")

    if session['usuario_logado'] != conta.titular:
        flash("Você não tem permissão para realizar saques nesta conta.")
        return redirect("/saque")

    resultadoSaque = conta.realizarSaque(valorSaque)

    if resultadoSaque == False:
        flash("Saldo insuficiente para realizar o saque!")
    elif resultadoSaque == True:
        flash("Saque realizado com sucesso!")
        return render_template("resultadoSaque.html", conta=conta, resultadoSaque=resultadoSaque)
    else:
        flash("Valor de saque inválido!")
    
    return redirect("/saque")

# Rota que renderiza a página de depósito se o usuário estiver logado como usuário comum
@webApp.route("/deposito")
def deposito():
    if usuarioLogado() and session['nivel'] == 'user':
        return render_template("deposito.html")
    else:
        flash("Usuário sem permissão!")
        return redirect("/main")

# Rota que processa o depósito com base nos dados fornecidos no formulário
@webApp.route("/depositar", methods=["POST", ])
def depositar():
    numero = int(request.form["numero"])
    valorDeposito = float(request.form["valorDeposito"])

    conta = pegarContaPeloNumero(numero)

    if conta is None:
        flash(f"Conta com número {numero} não encontrada!")
        return redirect("/deposito")
    
    resultadoDeposito = conta.realizarDeposito(valorDeposito)

    if resultadoDeposito == False:
        flash("Não é possível depositar valores negativos e/ou nulos!")
    elif resultadoDeposito == True:
        flash("Deposito realizado com sucesso!")
        return render_template("resultadoDeposito.html", conta=conta, resultadoDeposito=resultadoDeposito)
    else:
        flash("Valor de deposito inválido!")
    
    return redirect("/deposito")

# Rota que renderiza a página de transferência se o usuário estiver logado como usuário comum
@webApp.route("/transferencia")
def transferencia():
    if usuarioLogado() and session['nivel'] == 'user':
        return render_template("transferencia.html", contas=listaContas)
    else:
        flash("Usuário sem permissão!")
        return redirect("/main")

# Rota que processa a transferência com base nos dados fornecidos no formulário
@webApp.route("/transferir", methods=["POST", ])
def transferir():
    numeroOrigem = int(request.form["numeroOrigem"])
    numeroDestino = int(request.form["numeroDestino"])
    valorTransferencia = float(request.form["valorTransferencia"])
    senha = request.form["senha"]

    contaOrigem = pegarContaPeloNumero(numeroOrigem)
    contaDestino = pegarContaPeloNumero(numeroDestino)

    if contaOrigem is None:
        flash("Conta de origem não encontrada!")
        return redirect("/transferencia")
    
    if contaDestino is None:
        flash("Conta de destino não encontrada!")
        return redirect("/transferencia")

    if session['usuario_logado'] != contaOrigem.titular:
        flash("Você não tem permissão para realizar transferências nesta conta.")
        return redirect("/transferencia")

    resultadoTransferencia = contaOrigem.realizarTransferencia(contaDestino, valorTransferencia, senha)

    if resultadoTransferencia == "TRANSFERENCIA_REALIZADA":
        flash("Transferência realizada com sucesso!")
        return render_template("resultadoTransferencia.html", contaOrigem=contaOrigem, contaDestino=contaDestino, valorTransferencia=valorTransferencia)
    elif resultadoTransferencia == "SALDO_INSUFICIENTE":
        flash("Saldo insuficiente para realizar a transferência!")
    elif resultadoTransferencia == "SENHA_INCORRETA":
        flash("Senha incorreta para realizar a transferência!")
    elif resultadoTransferencia == "MESMA_CONTA":
        flash("Você não pode transferir para a mesma conta!")
    elif resultadoTransferencia == "VALOR_INVALIDO":
        flash("Valor de transferência inválido!")

    return redirect("/transferencia")

# Rota que exibe a página de acesso se o usuário não estiver logado, caso contrário redireciona para a página principal
@webApp.route('/login')
def exibirPaginaAcesso():
    if usuarioLogado() == False:
        proximaPagina = request.args.get('proximaPagina')
        return render_template('login.html', proximaPagina=proximaPagina)
    else:
        return redirect("/main")

# Rota que autentica o usuário com base nos dados fornecidos no formulário de login
@webApp.route('/autenticar', methods=['POST', ])
def autenticarUsuario():
    login = request.form["login"]
    senha = request.form["senha"]
    proximaPagina = request.form["proximaPagina"]

    if not usuarioExiste(login):
        flash(f"Login {login} não existe!")
        return redirect(url_for('exibirPaginaAcesso', proximaPagina=proximaPagina))

    usuario = pegarUsuario(login)

    if not usuario.validarSenha(senha):
        flash(f"Senha incorreta!")
        return redirect(url_for('exibirPaginaAcesso', proximaPagina=proximaPagina))

    flash(f"Bem-vindo, {usuario.titular}!")
    session['usuario_logado'] = usuario.titular
    session['nivel'] = usuario.cargo

    return redirect(proximaPagina)

# Rota que realiza o logout do usuário
@webApp.route('/logout')
def logout():
    session['usuario_logado'] = None
    return redirect('/login')

# Iniciando a aplicação Flask em modo de depuração
webApp.run(debug=True)