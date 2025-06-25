# 🧠 Sistema Multiagente de Mercado com MESA

Este projeto simula um **mercado artificial** usando **Sistemas Multiagentes** com o framework [Mesa](https://mesa.readthedocs.io/en/stable/). Agentes do tipo **vendedores** e **compradores** se movimentam e interagem em um grid, realizando transações com base em oferta e demanda.

---

## 📂 Estrutura do Projeto

├── market_model.py # Código principal com os agentes e simulação

├── requirements.txt # Dependências para execução

├── .gitignore # Ignora arquivos desnecessários

└── README.md # Este arquivo

---

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- [Mesa](https://mesa.readthedocs.io/en/stable/) – Framework para Sistemas Multiagentes
- matplotlib – Gráficos
- random – Geração de aleatoriedade

---

## 🧱 Como Funciona o Modelo?

### 👤 `TraderAgent`

Agente individual do sistema, podendo ser:
- **Seller (vendedor)**: tem recursos para vender.
- **Buyer (comprador)**: tem orçamento para comprar.

Cada agente:
- Se move aleatoriamente.
- Tenta interagir com outros na mesma célula.
- Realiza transações e ajusta preço com base na demanda.

### 🌍 `MarketModel`

O ambiente:
- Grade toroidal (os agentes saem de um lado e entram pelo outro).
- Agendador de ativação aleatória.
- Criação de agentes vendedores e compradores.
- Coleta de dados com `mesa.DataCollector`.

---

X: passos da simulação (tempo)

Y: número total de transações realizadas

Mostra a dinâmica de atividade econômica no ambiente simulado.

---

# 💵 Evolução do Preço Médio dos Vendedores

plot_average_price(model)

X: passos da simulação

Y: preço médio dos vendedores

Demonstra como os preços sobem ou descem conforme a demanda e recursos disponíveis.

---

# 🔁 O que é um Step?

Um step representa uma unidade de tempo no modelo. A cada step:

Todos os agentes são ativados e tomam decisões.

O ambiente é atualizado.

Dados são coletados para análise.

---

# 🧪 Personalização

Você pode adaptar facilmente:

O produto sendo vendido (ex: energia, alimentos, itens digitais).

As regras de negociação e ajuste de preços.

O tamanho do grid ou o número de agentes.
