# 🏦 Sistema Bancário em Python

Este projeto é uma demonstração de um **sistema bancário desenvolvido em Python**, utilizando conceitos de **Programação Orientada a Objetos (POO)**.

O arquivo `main.py` demonstra a criação de clientes e contas, operações bancárias, polimorfismo, métodos especiais e tratamento de erros.

## 📌 Funcionalidades

O sistema demonstra:

* Criação de clientes;
* Criação de contas correntes;
* Criação de contas poupança;
* Depósitos;
* Transferências;
* Fechamento do mês;
* Validação de dados;
* Tratamento de erros;
* Busca de contas;
* Ordenação de contas por saldo.

## 🧑‍💻 Conceitos utilizados

O projeto trabalha principalmente com:

* **Classes e objetos**
* **Herança**
* **Polimorfismo**
* **Exceções**
* **Métodos especiais**, como `__eq__`, `__lt__` e `__repr__`
* **Classe abstrata**
* **Try/except**

O polimorfismo é demonstrado quando diferentes tipos de conta executam o método `fechar_mes()` de maneiras diferentes.

## 💰 Operações

O programa realiza operações como:

```python
banco.transferir(1, 4, 300)
```

e:

```python
banco.buscar_conta(2).depositar(150)
```

Assim, é possível simular transferências e depósitos entre as contas.

## ⚠️ Tratamento de erros

O programa também testa situações inválidas, como:

* E-mail inválido;
* Nome vazio;
* Saldo negativo;
* Número de conta inválido;
* Depósito negativo;
* Depósito com texto;
* Conta duplicada;
* Conta inexistente;
* Saque acima do saldo.

Esses erros são tratados utilizando `try/except`.

## ▶️ Como executar

No terminal, execute:

```bash
python main.py
```

O programa apresentará no terminal as etapas da demonstração, incluindo a criação das contas, polimorfismo, operações e testes de entradas inválidas.

## 📁 Estrutura

O `main.py` utiliza classes e exceções importadas do arquivo `modelos.py`:

```text
projeto/
│
├── main.py
└── modelos.py
```

## 🎯 Objetivo

O objetivo do projeto é **demonstrar na prática conceitos de Programação Orientada a Objetos em Python**, utilizando um sistema bancário como exemplo.
