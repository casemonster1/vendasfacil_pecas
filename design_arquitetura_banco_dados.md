# Design da Arquitetura e Banco de Dados do Sistema de Estoque

## 1. Visão Geral da Arquitetura

O sistema de estoque será construído com uma arquitetura em camadas, visando modularidade, escalabilidade e manutenibilidade. A arquitetura proposta é composta por três camadas principais:

*   **Camada de Apresentação (Frontend):** Responsável pela interface do usuário, onde os membros da equipe interagirão com o sistema. Será desenvolvida utilizando React.
*   **Camada de Lógica de Negócios (Backend/API):** Contém a lógica central do sistema, gerenciando as operações de estoque, produtos, pedidos e a integração com a API do Mercado Livre. Será desenvolvida utilizando Python com Flask.
*   **Camada de Dados (Banco de Dados):** Responsável pelo armazenamento persistente de todas as informações do sistema. Será utilizado PostgreSQL.

### Fluxo de Dados Simplificado

1.  **Usuário (Frontend):** Interage com a interface web para adicionar/editar produtos, visualizar estoque, etc.
2.  **Requisição (Frontend para Backend):** O frontend envia requisições HTTP (GET, POST, PUT, DELETE) para a API do backend.
3.  **Processamento (Backend):** O backend recebe a requisição, valida os dados, executa a lógica de negócios (ex: atualiza o estoque, busca informações de produtos) e interage com o banco de dados e/ou a API do Mercado Livre.
4.  **Resposta (Backend para Frontend):** O backend retorna uma resposta HTTP (dados, status de sucesso/erro) para o frontend.
5.  **Integração com Mercado Livre (Backend):** O backend se comunica com a API do Mercado Livre para:
    *   Receber notificações de novos pedidos/pagamentos (via webhooks).
    *   Obter detalhes completos de pedidos.
    *   Atualizar o estoque de anúncios no Mercado Livre.

## 2. Design do Banco de Dados (PostgreSQL)

O banco de dados será projetado para armazenar todas as informações necessárias para o controle interno de estoque e a integração com o Mercado Livre. Abaixo está o esquema proposto para as tabelas principais.

### Entidades e Atributos

#### `produtos` (Tabela Principal de Produtos)

Esta tabela armazenará as informações gerais de cada peça de carro no estoque.

| Coluna                 | Tipo de Dado      | Restrições        | Descrição                                         |
| :--------------------- | :---------------- | :---------------- | :------------------------------------------------ |
| `id`                   | `SERIAL`          | `PRIMARY KEY`     | ID único do produto.                              |
| `nome`                 | `VARCHAR(255)`    | `NOT NULL`        | Nome da peça de carro.                            |
| `descricao`            | `TEXT`            | `NOT NULL`        | Descrição detalhada do produto.                   |
| `referencia_sku`       | `VARCHAR(100)`    | `UNIQUE`, `NOT NULL` | SKU (Stock Keeping Unit) ou referência interna.   |
| `preco_venda`          | `NUMERIC(10, 2)`  | `NOT NULL`        | Preço de venda do produto.                        |
| `quantidade_estoque`   | `INTEGER`         | `NOT NULL`, `>= 0` | Quantidade atual em estoque.                      |
| `localizacao_galpao`   | `VARCHAR(100)`    |                   | Localização física da peça no galpão.             |
| `categoria`            | `VARCHAR(100)`    |                   | Categoria da peça (ex: Motor, Suspensão).         |
| `subcategoria`         | `VARCHAR(100)`    |                   | Subcategoria da peça (ex: Bloco do Motor).        |
| `marca_peca`           | `VARCHAR(100)`    |                   | Marca do fabricante da peça.                      |
| `condicao`             | `VARCHAR(50)`     | `NOT NULL`        | Condição da peça (Novo, Usado, Recondicionado).   |
| `data_cadastro`        | `TIMESTAMP`       | `DEFAULT NOW()`   | Data e hora do cadastro do produto.               |
| `data_atualizacao`     | `TIMESTAMP`       | `DEFAULT NOW()`   | Última data e hora de atualização do produto.     |
| `ml_item_id`           | `VARCHAR(50)`     | `UNIQUE`          | ID do item no Mercado Livre (se houver).          |
| `ml_last_sync`         | `TIMESTAMP`       |                   | Última sincronização com o Mercado Livre.         |

#### `imagens_produto` (Tabela para Imagens de Produtos)

Armazenará os caminhos das imagens associadas a cada produto.

| Coluna         | Tipo de Dado   | Restrições        | Descrição                                         |
| :------------- | :------------- | :---------------- | :------------------------------------------------ |
| `id`           | `SERIAL`       | `PRIMARY KEY`     | ID único da imagem.                               |
| `produto_id`   | `INTEGER`      | `NOT NULL`, `FOREIGN KEY` | Chave estrangeira para a tabela `produtos`.       |
| `caminho_imagem` | `VARCHAR(255)` | `NOT NULL`        | Caminho ou URL da imagem.                         |
| `ordem`        | `INTEGER`      |                   | Ordem de exibição da imagem (opcional).           |

#### `veiculos_compativeis` (Tabela para Compatibilidade de Veículos)

Armazenará os veículos compatíveis com cada peça.

| Coluna             | Tipo de Dado   | Restrições        | Descrição                                         |
| :----------------- | :------------- | :---------------- | :------------------------------------------------ |
| `id`               | `SERIAL`       | `PRIMARY KEY`     | ID único da compatibilidade.                      |
| `produto_id`       | `INTEGER`      | `NOT NULL`, `FOREIGN KEY` | Chave estrangeira para a tabela `produtos`.       |
| `marca_veiculo`    | `VARCHAR(100)` | `NOT NULL`        | Marca do veículo (ex: Ford, Chevrolet).           |
| `modelo_veiculo`   | `VARCHAR(100)` | `NOT NULL`        | Modelo do veículo (ex: Ka, Onix).                 |
| `ano_inicial`      | `INTEGER`      |                   | Ano inicial de compatibilidade.                   |
| `ano_final`        | `INTEGER`      |                   | Ano final de compatibilidade.                     |

#### `pedidos_ml` (Tabela para Pedidos do Mercado Livre)

Armazenará os dados dos pedidos recebidos do Mercado Livre.

| Coluna                   | Tipo de Dado      | Restrições        | Descrição                                         |
| :----------------------- | :---------------- | :---------------- | :------------------------------------------------ |
| `id`                     | `BIGINT`          | `PRIMARY KEY`     | ID do pedido no Mercado Livre.                    |
| `data_criacao`           | `TIMESTAMP`       | `NOT NULL`        | Data e hora de criação do pedido.                 |
| `data_fechamento`        | `TIMESTAMP`       |                   | Data e hora de fechamento do pedido.              |
| `ultima_atualizacao`     | `TIMESTAMP`       | `NOT NULL`        | Última data e hora de atualização do pedido.      |
| `total_amount`           | `NUMERIC(10, 2)`  | `NOT NULL`        | Valor total do pedido.                            |
| `paid_amount`            | `NUMERIC(10, 2)`  | `NOT NULL`        | Valor pago pelo pedido.                           |
| `currency_id`            | `VARCHAR(10)`     | `NOT NULL`        | Moeda do pedido (ex: BRL).                        |
| `status`                 | `VARCHAR(50)`     | `NOT NULL`        | Status geral do pedido (ex: paid, pending).       |
| `status_detalhe`         | `VARCHAR(100)`    |                   | Detalhe do status do pedido (ex: accredited).     |
| `ml_user_id`             | `BIGINT`          | `NOT NULL`        | ID do usuário (vendedor) no Mercado Livre.        |
| `comprador_id`           | `BIGINT`          |                   | ID do comprador no Mercado Livre.                 |
| `comprador_nickname`     | `VARCHAR(100)`    |                   | Nickname do comprador.                            |
| `comprador_email`        | `VARCHAR(255)`    |                   | Email do comprador.                               |
| `shipping_id`            | `BIGINT`          |                   | ID do envio associado ao pedido.                  |

#### `itens_pedido_ml` (Tabela para Itens de Pedidos do Mercado Livre)

Armazenará os itens de cada pedido do Mercado Livre.

| Coluna             | Tipo de Dado   | Restrições        | Descrição                                         |
| :----------------- | :------------- | :---------------- | :------------------------------------------------ |
| `id`               | `SERIAL`       | `PRIMARY KEY`     | ID único do item do pedido.                       |
| `pedido_ml_id`     | `BIGINT`       | `NOT NULL`, `FOREIGN KEY` | Chave estrangeira para a tabela `pedidos_ml`.     |
| `ml_item_id`       | `VARCHAR(50)`  | `NOT NULL`        | ID do item (produto) no Mercado Livre.            |
| `titulo_item`      | `VARCHAR(255)` | `NOT NULL`        | Título do item no momento da compra.              |
| `quantidade`       | `INTEGER`      | `NOT NULL`, `>= 1` | Quantidade comprada deste item.                   |
| `preco_unitario`   | `NUMERIC(10, 2)` | `NOT NULL`        | Preço unitário do item no momento da compra.      |
| `produto_interno_id` | `INTEGER`      | `FOREIGN KEY`     | Chave estrangeira para `produtos` (se mapeado).   |

#### `pagamentos_ml` (Tabela para Pagamentos de Pedidos do Mercado Livre)

Armazenará os detalhes de pagamento de cada pedido do Mercado Livre.

| Coluna                   | Tipo de Dado      | Restrições        | Descrição                                         |
| :----------------------- | :---------------- | :---------------- | :------------------------------------------------ |
| `id`                     | `BIGINT`          | `PRIMARY KEY`     | ID do pagamento no Mercado Livre.                 |
| `pedido_ml_id`           | `BIGINT`          | `NOT NULL`, `FOREIGN KEY` | Chave estrangeira para a tabela `pedidos_ml`.     |
| `payer_id`               | `BIGINT`          |                   | ID do pagador.                                    |
| `metodo_pagamento`       | `VARCHAR(100)`    |                   | Método de pagamento (ex: account_money).          |
| `status`                 | `VARCHAR(50)`     | `NOT NULL`        | Status do pagamento (ex: approved, pending).      |
| `status_detalhe`         | `VARCHAR(100)`    |                   | Detalhe do status do pagamento (ex: accredited).  |
| `transaction_amount`     | `NUMERIC(10, 2)`  | `NOT NULL`        | Valor da transação.                               |
| `data_aprovacao`         | `TIMESTAMP`       |                   | Data e hora de aprovação do pagamento.           |
| `data_criacao`           | `TIMESTAMP`       | `NOT NULL`        | Data e hora de criação do registro de pagamento.  |

#### `usuarios` (Tabela para Usuários do Sistema Interno)

Armazenará os usuários que terão acesso ao sistema de controle interno.

| Coluna     | Tipo de Dado   | Restrições        | Descrição                                         |
| :--------- | :------------- | :---------------- | :------------------------------------------------ |
| `id`       | `SERIAL`       | `PRIMARY KEY`     | ID único do usuário.                              |
| `nome`     | `VARCHAR(100)` | `NOT NULL`        | Nome completo do usuário.                         |
| `email`    | `VARCHAR(255)` | `UNIQUE`, `NOT NULL` | Email do usuário (usado para login).              |
| `senha_hash` | `VARCHAR(255)` | `NOT NULL`        | Hash da senha do usuário.                         |
| `role`     | `VARCHAR(50)`  | `NOT NULL`        | Nível de acesso (ex: admin, estoque, visualizador).|
| `ativo`    | `BOOLEAN`      | `DEFAULT TRUE`    | Indica se o usuário está ativo.                   |

### Relacionamentos

*   `produtos` 1:N `imagens_produto` (Um produto pode ter várias imagens)
*   `produtos` 1:N `veiculos_compativeis` (Um produto pode ser compatível com vários veículos)
*   `pedidos_ml` 1:N `itens_pedido_ml` (Um pedido pode ter vários itens)
*   `pedidos_ml` 1:N `pagamentos_ml` (Um pedido pode ter vários pagamentos)
*   `itens_pedido_ml` N:1 `produtos` (Um item de pedido pode se referir a um produto interno, se mapeado)

## 3. Diagrama de Entidade-Relacionamento (ERD)

(Neste ponto, um diagrama visual seria gerado. Como sou um modelo de texto, descrevo as relações acima. O diagrama seria uma representação visual das tabelas e seus relacionamentos, com chaves primárias e estrangeiras indicadas.)

## 4. Diagrama de Componentes da Arquitetura

(Neste ponto, um diagrama visual seria gerado. Como sou um modelo de texto, descrevo os componentes e fluxos de dados. O diagrama mostraria as três camadas (Frontend, Backend, Banco de Dados) e a interação com a API do Mercado Livre, além de setas indicando o fluxo de comunicação.)

## 5. Considerações de Design

*   **Normalização:** O esquema do banco de dados é projetado para ser normalizado, minimizando a redundância de dados e garantindo a integridade.
*   **Escalabilidade:** A arquitetura em camadas permite que cada componente seja escalado independentemente, se necessário.
*   **Segurança:** A autenticação de usuários e o uso de tokens de acesso para a API do Mercado Livre são pontos chave. A comunicação entre frontend e backend será via HTTPS.
*   **Flexibilidade:** A separação de responsabilidades entre as camadas facilita futuras modificações e a adição de novas funcionalidades.
*   **Mapeamento de Produtos:** O campo `ml_item_id` na tabela `produtos` e `produto_interno_id` na tabela `itens_pedido_ml` são cruciais para mapear os produtos do Mercado Livre com os produtos internos, permitindo a atualização automática do estoque.

Este design fornece uma base sólida para o desenvolvimento do sistema, garantindo que todos os requisitos funcionais e não funcionais sejam atendidos.




## 3. Diagrama de Entidade-Relacionamento (ERD) - Descrição Detalhada

Um Diagrama de Entidade-Relacionamento (ERD) visualizaria as tabelas (`produtos`, `imagens_produto`, `veiculos_compativeis`, `pedidos_ml`, `itens_pedido_ml`, `pagamentos_ml`, `usuarios`) e seus relacionamentos da seguinte forma:

*   **Entidades (Tabelas):** Cada tabela seria representada por um retângulo, contendo o nome da tabela no topo e uma lista de seus atributos (colunas) abaixo. As chaves primárias seriam sublinhadas.
    *   `produtos`: `id` (PK), `nome`, `descricao`, `referencia_sku`, `preco_venda`, `quantidade_estoque`, `localizacao_galpao`, `categoria`, `subcategoria`, `marca_peca`, `condicao`, `data_cadastro`, `data_atualizacao`, `ml_item_id`, `ml_last_sync`.
    *   `imagens_produto`: `id` (PK), `produto_id` (FK), `caminho_imagem`, `ordem`.
    *   `veiculos_compativeis`: `id` (PK), `produto_id` (FK), `marca_veiculo`, `modelo_veiculo`, `ano_inicial`, `ano_final`.
    *   `pedidos_ml`: `id` (PK), `data_criacao`, `data_fechamento`, `ultima_atualizacao`, `total_amount`, `paid_amount`, `currency_id`, `status`, `status_detalhe`, `ml_user_id`, `comprador_id`, `comprador_nickname`, `comprador_email`, `shipping_id`.
    *   `itens_pedido_ml`: `id` (PK), `pedido_ml_id` (FK), `ml_item_id`, `titulo_item`, `quantidade`, `preco_unitario`, `produto_interno_id` (FK).
    *   `pagamentos_ml`: `id` (PK), `pedido_ml_id` (FK), `payer_id`, `metodo_pagamento`, `status`, `status_detalhe`, `transaction_amount`, `data_aprovacao`, `data_criacao`.
    *   `usuarios`: `id` (PK), `nome`, `email`, `senha_hash`, `role`, `ativo`.

*   **Relacionamentos:** Linhas conectariam as entidades, com notações de cardinalidade (1:N, N:1) em cada extremidade para indicar o tipo de relacionamento.
    *   **Um para Muitos (1:N):**
        *   `produtos` para `imagens_produto`: Uma linha da entidade `produtos` para `imagens_produto`, com um '1' no lado de `produtos` e um 'N' no lado de `imagens_produto`. A chave estrangeira `produto_id` em `imagens_produto` apontaria para `id` em `produtos`.
        *   `produtos` para `veiculos_compativeis`: Similar ao anterior, com `produto_id` em `veiculos_compativeis` apontando para `id` em `produtos`.
        *   `pedidos_ml` para `itens_pedido_m
(Content truncated due to size limit. Use line ranges to read in chunks)