import os

# Classe Cliente
class Cliente:
    def __init__(self, id_cliente, nome, cpf):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
   
    # Getter e Setter para id_cliente
    @property
    def id_cliente(self):
        return self._id_cliente
   
    @id_cliente.setter
    def id_cliente(self, value):
        if len(str(value)) == 4:  # ID do cliente deve ter 4 dígitos
            self._id_cliente = value
        else:
            raise ValueError("ID do cliente deve ter 4 dígitos.")
   
    # Getter e Setter para nome
    @property
    def nome(self):
        return self._nome
   
    @nome.setter
    def nome(self, value):
        if len(value) >= 3:
            self._nome = value
        else:
            raise ValueError("Nome deve ter pelo menos 3 caracteres.")
   
    # Getter e Setter para cpf
    @property
    def cpf(self):
        return self._cpf
   
    @cpf.setter
    def cpf(self, value):
        if len(str(value)) == 11:
            self._cpf = value
        else:
            raise ValueError("CPF deve ter 11 dígitos.")

    def __repr__(self):
        return f"Cliente(id_cliente={self.id_cliente}, nome={self.nome}, cpf={self.cpf})"

# Classe Conta
class Conta:
    def __init__(self, numero, saldo, cliente):
        self.numero = numero
        self.saldo = saldo
        self.cliente = cliente  # Relacionamento com Cliente
   
    # Getter e Setter para saldo
    @property
    def saldo(self):
        return self._saldo
   
    @saldo.setter
    def saldo(self, value):
        if value < 0:
            raise ValueError("Saldo não pode ser negativo.")
        self._saldo = value

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor de depósito deve ser positivo.")
        self.saldo += valor

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor de saque deve ser positivo.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor

    def __repr__(self):
        return f"Conta(numero={self.numero}, saldo={self.saldo}, cliente={self.cliente})"

# Classe Banco
class Banco:
    def __init__(self):
        self.clientes = []  # Lista de clientes
        self.contas = []    # Lista de contas
        self._load_data()

    def _load_data(self):
        """Carrega dados de clientes e contas a partir de um arquivo JSON"""
        if os.path.exists("dados_banco.txt"):
            with open("dados_banco.txt", "r") as file:
                data=file.readlines()
                for line in data:
                    if line[:8]=="cliente:":
                        datasplit=line[8:].split(";")
                        cliente=Cliente(int(datasplit[0]),datasplit[1],datasplit[2])
                        self.clientes.append(cliente)
                    elif line[:6]=="conta:":
                        datasplit=line[6:].split(";")
                        id_cliente = int(datasplit[2][19:23])
                        cliente = next((c for c in self.clientes if c.id_cliente == id_cliente), None)
                        conta=Conta(int(datasplit[0]),float(datasplit[1]),cliente)
                        self.contas.append(conta)

    def _save_data(self):
        #Salva dados de clientes e contas em um arquivo txt
        data=""
        for i in self.clientes:
            dados=";".join(str(x) for x in vars(i).values())
            data=data+"cliente:" + dados + ";\n"
        for i in self.contas:
            contavars=vars(i)
            dados=";".join(str(x) for x in contavars.values())
            data=data+"conta:" + dados + ";\n"
        with open("dados_banco.txt","w") as file:
            file.write(data)


    def adicionar_cliente(self, id_cliente, nome, cpf):
        try:
            cliente = Cliente(id_cliente, nome, cpf)
            self.clientes.append(cliente)
            self._save_data()
        except ValueError as e:
            print(f"Erro ao adicionar cliente: {e}")
   
    def adicionar_conta(self, numero, saldo, id_cliente):
        try:
            cliente = next((c for c in self.clientes if c.id_cliente == id_cliente), None)
            if cliente is None:
                raise ValueError("Cliente não encontrado.")
            conta = Conta(numero, saldo, cliente)
            self.contas.append(conta)
            self._save_data()
        except ValueError as e:
            print(f"Erro ao adicionar conta: {e}")

    def buscar_cliente(self, id_cliente):
        return next((cliente for cliente in self.clientes if cliente.id_cliente == id_cliente), None)

    def buscar_conta(self, numero):
        return next((conta for conta in self.contas if conta.numero == numero), None)

    def realizar_deposito(self, numero_conta, valor):
        try:
            conta = self.buscar_conta(numero_conta)
            if conta is None:
                raise ValueError("Conta não encontrada.")
            conta.depositar(valor)
            self._save_data()
        except ValueError as e:
            print(f"Erro ao realizar depósito: {e}")

    def realizar_saque(self, numero_conta, valor):
        try:
            conta = self.buscar_conta(numero_conta)
            if conta is None:
                raise ValueError("Conta não encontrada.")
            conta.sacar(valor)
            self._save_data()
        except ValueError as e:
            print(f"Erro ao realizar saque: {e}")






# Exemplo de uso
banco = Banco()

# Adicionando clientes
banco.adicionar_cliente(1001, "João Silva", "12345678901")
banco.adicionar_cliente(1002, "Maria Oliveira", "10987654321")

# Adicionando contas
banco.adicionar_conta(10001, 500.0, 1001)
banco.adicionar_conta(10002, 1000.0, 1002)

# Realizando operações
banco.realizar_deposito(10001, 200.0)
banco.realizar_saque(10002, 500.0)

# Verificando contas
conta_joao = banco.buscar_conta(10001)
conta_maria = banco.buscar_conta(10002)
print(conta_joao)
print(conta_maria)

#for i in banco.clientes:
#    print(i)
#for i in banco.contas:
#    print(i)

#banco._save_data()

#with open("dados_banco.txt","r") as file:
#    print(file.read())