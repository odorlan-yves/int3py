"""Demonstração do sistema bancário: instâncias, polimorfismo e exceções."""

from modelos import (
    Banco,
    Cliente,
    Conta,
    ContaCorrente,
    ContaNaoEncontradaError,
    ContaPoupanca,
    SaldoInsuficienteError,
    formatar_moeda,
)


def titulo(texto):
    print(f"\n{'=' * 8} {texto} {'=' * 8}")


def main():
    # ---------------- 1. Criação de objetos (11 instâncias) ----------------
    titulo("1. CRIAÇÃO DE OBJETOS")
    ana = Cliente("Ana Souza", "ana@email.com")
    bruno = Cliente("Bruno Lima", "bruno@email.com")
    carla = Cliente("Carla Dias", "carla@email.com")
    diego = Cliente("Diego Rocha", "diego@email.com")

    banco = Banco("Sprint Bank")
    banco.adicionar_conta(ContaCorrente(1, ana, 1500.00))
    banco.adicionar_conta(ContaCorrente(2, bruno, 800.00, tarifa_mensal=20))
    banco.adicionar_conta(ContaCorrente(3, carla, 5.00))  # saldo menor que a tarifa
    banco.adicionar_conta(ContaPoupanca(4, ana, 3000.00))
    banco.adicionar_conta(ContaPoupanca(5, diego, 1200.00, taxa_rendimento=0.007))
    banco.adicionar_conta(ContaPoupanca(6, carla, 500.00))

    for cliente in (ana, bruno, carla, diego):
        print(cliente)
    print()
    for conta in banco:
        print(conta)
    print(f"\n{banco}")

    # ---------------- 2. Polimorfismo ----------------
    titulo("2. POLIMORFISMO: fechar_mes() em cada tipo de conta")
    for conta in banco:  # mesma chamada, comportamentos diferentes
        try:
            resultado = conta.fechar_mes()
        except SaldoInsuficienteError as erro:
            resultado = f"ERRO ao fechar o mês: {erro}"
        print(f"Conta {conta.numero:04d} ({conta.NOME_TIPO}): {resultado}")

    # ---------------- 3. Métodos especiais ----------------
    titulo("3. MÉTODOS ESPECIAIS (__eq__, __lt__, __repr__)")
    contas = list(banco)
    print("Ordenadas por saldo (usa __lt__):")
    for conta in sorted(contas):
        print(f"  {conta.numero:04d} -> {formatar_moeda(conta.saldo)}")
    print(f"Maior saldo: {max(contas)}")
    print(f"conta 1 == conta 1? {contas[0] == banco.buscar_conta(1)}")
    print(f"conta 1 == conta 2? {contas[0] == contas[1]}")
    print(f"repr: {contas[0]!r}")
    print(f"repr: {banco!r}")

    # ---------------- 4. Operações ----------------
    titulo("4. OPERAÇÕES")
    banco.transferir(1, 4, 300)
    print(f"Após transferir R$ 300,00 da conta 1 para a 4:\n  {banco.buscar_conta(1)}\n  {banco.buscar_conta(4)}")
    banco.buscar_conta(2).depositar(150)
    print(f"Após depósito na conta 2:\n  {banco.buscar_conta(2)}")

    # ---------------- 5. Entradas inválidas ----------------
    titulo("5. ENTRADAS INVÁLIDAS (try/except)")
    conta_um = banco.buscar_conta(1)

    def definir_saldo_negativo():
        conta_um.saldo = -100

    casos = [
        ("e-mail inválido", lambda: Cliente("Eva", "eva@@email")),
        ("nome vazio", lambda: Cliente("   ", "eva@email.com")),
        ("saldo inicial negativo", lambda: ContaCorrente(10, ana, -50)),
        ("saldo negativo via setter", definir_saldo_negativo),
        ("número de conta inválido", lambda: ContaPoupanca(-3, ana)),
        ("taxa de rendimento absurda", lambda: ContaPoupanca(11, ana, 100, taxa_rendimento=5)),
        ("titular que não é Cliente", lambda: ContaCorrente(12, "Ana")),
        ("saque acima do saldo", lambda: conta_um.sacar(999999)),
        ("depósito negativo", lambda: conta_um.depositar(-10)),
        ("depósito com texto", lambda: conta_um.depositar("cem")),
        ("conta duplicada", lambda: banco.adicionar_conta(ContaCorrente(1, bruno))),
        ("conta inexistente", lambda: banco.buscar_conta(99)),
        ("instanciar classe abstrata", lambda: Conta(20, ana)),
    ]
    for descricao, acao in casos:
        try:
            acao()
        except (ValueError, TypeError, SaldoInsuficienteError, ContaNaoEncontradaError) as erro:
            print(f"  [{type(erro).__name__}] {descricao}: {erro}")
        else:
            print(f"  [SEM ERRO] {descricao}: era esperado um erro!")

    titulo("RESUMO FINAL")
    print(banco)


if __name__ == "__main__":
    main()
