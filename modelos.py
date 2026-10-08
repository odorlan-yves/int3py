"""Modelos do sistema bancário (Programação Orientada a Objetos).

Classes:
    Cliente         -> dados da pessoa titular (composição: a conta "tem um" cliente)
    Conta (ABC)     -> classe abstrata com o comportamento comum
    ContaCorrente   -> "é uma" Conta; cobra tarifa mensal
    ContaPoupanca   -> "é uma" Conta; rende juros mensais
    Banco           -> agrega contas (composição: o banco "tem" contas)
"""

import re
from abc import ABC, abstractmethod

PADRAO_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)*\.[a-zA-Z]{2,}$")


def formatar_moeda(valor):
    """Formata um número como moeda brasileira (ex.: R$ 1.234,50)."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def eh_numero(valor):
    """True se for int ou float (e não bool)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


# --------------------------------------------------------------------
# Exceções de negócio
# --------------------------------------------------------------------
class SaldoInsuficienteError(Exception):
    """Operação pede mais dinheiro do que a conta possui."""

    def __init__(self, saldo, valor):
        super().__init__(
            f"saldo insuficiente (saldo: {formatar_moeda(saldo)}, necessário: {formatar_moeda(valor)})"
        )


class ContaNaoEncontradaError(Exception):
    """Número de conta inexistente no banco."""


# --------------------------------------------------------------------
# Cliente
# --------------------------------------------------------------------
class Cliente:
    """Pessoa titular de uma ou mais contas."""

    def __init__(self, nome, email):
        self.nome = nome    # passa pelo setter (validação)
        self.email = email  # passa pelo setter (validação)

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValueError("nome deve ser um texto com pelo menos 2 caracteres")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not PADRAO_EMAIL.match(valor.strip()):
            raise ValueError(f"e-mail inválido: {valor!r}")
        self._email = valor.strip().lower()

    def __str__(self):
        return f"{self.nome} <{self.email}>"

    def __repr__(self):
        return f"Cliente(nome={self.nome!r}, email={self.email!r})"

    def __eq__(self, outro):
        if not isinstance(outro, Cliente):
            return NotImplemented
        return self.email == outro.email

    def __hash__(self):
        return hash(self.email)


# --------------------------------------------------------------------
# Conta (classe abstrata)
# --------------------------------------------------------------------
class Conta(ABC):
    """Contrato e comportamento comum a todas as contas."""

    NOME_TIPO = "Conta"  # sobrescrito nas filhas

    def __init__(self, numero, titular, saldo_inicial=0.0):
        if not isinstance(numero, int) or isinstance(numero, bool) or numero <= 0:
            raise ValueError(f"número da conta deve ser um inteiro positivo, recebido: {numero!r}")
        self._numero = numero  # somente leitura (sem setter)
        self.titular = titular  # setter valida o tipo
        self._saldo = 0.0
        self.saldo = saldo_inicial  # setter valida (nunca negativo)

    # --- propriedades com validação ---
    @property
    def numero(self):
        return self._numero

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, valor):
        if not isinstance(valor, Cliente):
            raise TypeError("titular deve ser um objeto Cliente")
        self._titular = valor

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if not eh_numero(valor):
            raise TypeError(f"saldo deve ser numérico, recebido: {valor!r}")
        if valor < 0:
            raise ValueError("saldo não pode ser negativo")
        self._saldo = round(float(valor), 2)

    # --- operações ---
    @staticmethod
    def _validar_valor(valor):
        if not eh_numero(valor):
            raise TypeError(f"valor deve ser numérico, recebido: {valor!r}")
        if valor <= 0:
            raise ValueError("valor da operação deve ser maior que zero")

    def depositar(self, valor):
        """Adiciona dinheiro à conta e retorna o novo saldo."""
        self._validar_valor(valor)
        self.saldo += valor
        return self.saldo

    def sacar(self, valor):
        """Retira dinheiro da conta e retorna o novo saldo."""
        self._validar_valor(valor)
        if valor > self.saldo:
            raise SaldoInsuficienteError(self.saldo, valor)
        self.saldo -= valor
        return self.saldo

    @abstractmethod
    def fechar_mes(self):
        """Rotina de fim de mês (cada tipo de conta faz algo diferente)."""

    # --- métodos especiais ---
    def __str__(self):
        return (
            f"[{self.NOME_TIPO}] Conta {self.numero:04d} | "
            f"{self.titular.nome} | Saldo: {formatar_moeda(self.saldo)}"
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}(numero={self.numero}, "
            f"titular={self.titular.nome!r}, saldo={self.saldo})"
        )

    def __eq__(self, outra):
        if not isinstance(outra, Conta):
            return NotImplemented
        return self.numero == outra.numero

    def __hash__(self):
        return hash(self.numero)

    def __lt__(self, outra):
        """Compara contas pelo saldo (permite sorted(), min(), max())."""
        if not isinstance(outra, Conta):
            return NotImplemented
        return self.saldo < outra.saldo


# --------------------------------------------------------------------
# Contas concretas (herança + polimorfismo)
# --------------------------------------------------------------------
class ContaCorrente(Conta):
    """Conta que cobra uma tarifa de manutenção mensal."""

    NOME_TIPO = "Corrente"

    def __init__(self, numero, titular, saldo_inicial=0.0, tarifa_mensal=15.0):
        super().__init__(numero, titular, saldo_inicial)
        self.tarifa_mensal = tarifa_mensal

    @property
    def tarifa_mensal(self):
        return self._tarifa_mensal

    @tarifa_mensal.setter
    def tarifa_mensal(self, valor):
        if not eh_numero(valor) or valor < 0:
            raise ValueError(f"tarifa mensal deve ser um número >= 0, recebido: {valor!r}")
        self._tarifa_mensal = float(valor)

    def fechar_mes(self):
        """Debita a tarifa de manutenção."""
        self.sacar(self.tarifa_mensal)
        return f"Tarifa de {formatar_moeda(self.tarifa_mensal)} debitada. Novo saldo: {formatar_moeda(self.saldo)}"

    def __str__(self):
        return f"{super().__str__()} | Tarifa: {formatar_moeda(self.tarifa_mensal)}"


class ContaPoupanca(Conta):
    """Conta que rende juros todo mês."""

    NOME_TIPO = "Poupança"

    def __init__(self, numero, titular, saldo_inicial=0.0, taxa_rendimento=0.005):
        super().__init__(numero, titular, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        if not eh_numero(valor) or not 0 <= valor <= 1:
            raise ValueError(f"taxa de rendimento deve estar entre 0 e 1, recebido: {valor!r}")
        self._taxa_rendimento = float(valor)

    def fechar_mes(self):
        """Credita o rendimento mensal."""
        rendimento = round(self.saldo * self.taxa_rendimento, 2)
        self.saldo += rendimento
        return f"Rendimento de {formatar_moeda(rendimento)} creditado. Novo saldo: {formatar_moeda(self.saldo)}"

    def __str__(self):
        return f"{super().__str__()} | Taxa: {self.taxa_rendimento * 100:.2f}% a.m."


# --------------------------------------------------------------------
# Banco (composição)
# --------------------------------------------------------------------
class Banco:
    """Guarda e gerencia um conjunto de contas."""

    def __init__(self, nome, contas=None):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("nome do banco não pode ser vazio")
        self._nome = nome.strip()
        self._contas = []  # lista nova para cada banco (nada de [] como padrão!)
        for conta in contas or []:
            self.adicionar_conta(conta)

    @property
    def nome(self):
        return self._nome

    @property
    def total_depositado(self):
        return sum(conta.saldo for conta in self._contas)

    def adicionar_conta(self, conta):
        if not isinstance(conta, Conta):
            raise TypeError("só é possível adicionar objetos do tipo Conta")
        if conta in self._contas:  # usa Conta.__eq__
            raise ValueError(f"já existe uma conta com o número {conta.numero}")
        self._contas.append(conta)

    def buscar_conta(self, numero):
        for conta in self._contas:
            if conta.numero == numero:
                return conta
        raise ContaNaoEncontradaError(f"conta {numero} não encontrada")

    def transferir(self, numero_origem, numero_destino, valor):
        origem = self.buscar_conta(numero_origem)
        destino = self.buscar_conta(numero_destino)
        origem.sacar(valor)  # se falhar, nada foi alterado no destino
        destino.depositar(valor)

    def __len__(self):
        return len(self._contas)

    def __iter__(self):
        return iter(self._contas)

    def __str__(self):
        return f"Banco {self.nome}: {len(self)} conta(s), total {formatar_moeda(self.total_depositado)}"

    def __repr__(self):
        return f"Banco(nome={self.nome!r}, contas={len(self)})"
