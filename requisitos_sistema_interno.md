
## Requisitos Detalhados do Sistema de Controle Interno

### Gerenciamento de Produtos

*   **Adicionar Novo Produto:**
    *   Campos: Nome do Produto, Descrição Detalhada, Referência (SKU), Preço de Venda, Quantidade em Estoque, Localização no Galpão, Imagens do Produto (múltiplas), Categoria (ex: Motor, Suspensão, Freios), Subcategoria (ex: Bloco do Motor, Amortecedor Dianteiro), Marca da Peça, Condição (Novo, Usado, Recondicionado).
    *   Veículos Compatíveis: Marca do Veículo, Modelo do Veículo, Ano Inicial, Ano Final (para cada veículo compatível, permitindo múltiplos).
    *   Validação de campos obrigatórios.
    *   Upload de múltiplas imagens com pré-visualização.

*   **Editar Produto Existente:**
    *   Capacidade de modificar todos os campos de um produto existente.
    *   Adicionar/Remover imagens.
    *   Atualizar informações de compatibilidade de veículos.

*   **Visualização de Produtos:**
    *   Listagem de todos os produtos com filtros por nome, referência, categoria, marca, condição.
    *   Pesquisa por texto livre.
    *   Visualização detalhada de cada produto com todas as informações e imagens.

### Controle de Estoque

*   **Atualização de Quantidade:**
    *   Entrada de novas peças (aumento de estoque).
    *   Saída de peças (diminuição de estoque).
    *   Ajuste de estoque (para perdas, danos, etc.).
    *   Registro de histórico de movimentação de estoque por produto.

*   **Alertas de Estoque Mínimo:**
    *   Configuração de um nível de estoque mínimo para cada produto.
    *   Notificações automáticas quando o estoque de um produto atinge ou fica abaixo do nível mínimo.

### Gerenciamento de Pedidos (Interno)

*   **Status do Pedido:**
    *   Integração com o Mercado Livre para receber informações de pedidos.
    *   Status: "Aguardando Pagamento", "Pagamento Confirmado", "Vendido, Aguardando Entrega", "Enviado", "Entregue", "Cancelado".
    *   Atualização automática do status do estoque quando o pagamento é confirmado (descontar item ou marcar como "Vendido, Aguardando Entrega").

*   **Detalhes do Pedido:**
    *   Informações do comprador (nome, endereço, contato).
    *   Itens do pedido (produto, quantidade, preço).
    *   Informações de pagamento.
    *   Informações de envio.

### Relatórios

*   **Relatório de Estoque:**
    *   Produtos em estoque, quantidade, valor total.
    *   Produtos com estoque baixo.

*   **Relatório de Vendas:**
    *   Vendas por período, por produto, por categoria.
    *   Receita total.

### Interface do Usuário (UI/UX)

*   **Design Intuitivo e Atraente:**
    *   Interface limpa e fácil de usar.
    *   Responsivo para diferentes tamanhos de tela (desktop, tablet).
    *   Visualmente bonito, conforme solicitado pelo usuário.

*   **Navegação Clara:**
    *   Menu de navegação lógico.
    *   Funcionalidades agrupadas de forma coerente.

### Segurança

*   **Autenticação de Usuários:**
    *   Login e senha.
    *   Possibilidade de diferentes níveis de acesso (ex: administrador, operador de estoque).

*   **Proteção de Dados:**
    *   Armazenamento seguro de informações de produtos e pedidos.




### Integração com Mercado Livre

*   **Autenticação:**
    *   O sistema precisará se autenticar com a API do Mercado Livre para acessar os dados do vendedor.
    *   Será necessário um processo de autorização OAuth 2.0 para obter tokens de acesso.

*   **Sincronização de Produtos (Opcional, mas útil):**
    *   Considerar a possibilidade de sincronizar produtos do sistema interno para o Mercado Livre, ou vice-versa, para evitar duplicação de trabalho.
    *   Isso pode incluir a criação de novos anúncios ou a atualização de anúncios existentes.

*   **Recebimento de Informações de Pagamento e Pedido:**
    *   O sistema deve ser capaz de receber notificações do Mercado Livre sobre novos pagamentos e pedidos.
    *   Isso pode ser feito através de webhooks (preferencial) ou polling regular da API.
    *   As informações recebidas devem incluir: ID do pedido, detalhes do comprador, itens comprados, valor total, status do pagamento.

*   **Atualização de Estoque:**
    *   Quando um pagamento é confirmado no Mercado Livre, o sistema interno deve automaticamente descontar o item do estoque ou marcar seu status como "Vendido, Aguardando Entrega".
    *   Se um item for vendido internamente, o estoque no Mercado Livre também deve ser atualizado para evitar vendas duplicadas.

*   **Atualização de Status do Pedido:**
    *   O sistema pode, opcionalmente, atualizar o status do pedido no Mercado Livre (ex: "Enviado", "Entregue") com base nas ações realizadas no sistema interno.

*   **Tratamento de Erros e Reconciliação:**
    *   Mecanismos para lidar com falhas na comunicação com a API do Mercado Livre.
    *   Processos para reconciliar discrepâncias de estoque entre o sistema interno e o Mercado Livre.




### Tecnologias e Ferramentas Sugeridas

Com base nos requisitos e nas tendências atuais de desenvolvimento web, as seguintes tecnologias são sugeridas para o desenvolvimento do sistema:

*   **Backend:** Python com Flask
    *   **Justificativa:** Python é uma linguagem versátil, com uma vasta comunidade e muitas bibliotecas. Flask é um microframework web leve e flexível, ideal para construir APIs RESTful, que serão essenciais para a comunicação entre o frontend, o banco de dados e a API do Mercado Livre. É uma escolha excelente para prototipagem rápida e escalabilidade.

*   **Banco de Dados:** PostgreSQL
    *   **Justificativa:** PostgreSQL é um sistema de gerenciamento de banco de dados relacional robusto, de código aberto e altamente extensível. É conhecido por sua confiabilidade, integridade de dados e desempenho, sendo adequado para armazenar informações detalhadas de produtos, estoque e pedidos. Ele suporta tipos de dados complexos e tem um bom suporte para operações transacionais.

*   **Frontend:** React
    *   **Justificativa:** React é uma biblioteca JavaScript popular para construir interfaces de usuário interativas e reativas. Sua abordagem baseada em componentes facilita o desenvolvimento de interfaces complexas e reutilizáveis, garantindo uma experiência de usuário fluida e visualmente atraente, conforme solicitado. A grande comunidade e o ecossistema de ferramentas do React também são vantagens significativas.

*   **Gerenciamento de Pacotes (Frontend):** npm ou Yarn
    *   **Justificativa:** Ferramentas padrão para gerenciar dependências de projetos JavaScript.

*   **Controle de Versão:** Git
    *   **Justificativa:** Essencial para o desenvolvimento colaborativo e para o controle de todas as alterações no código-fonte.

*   **Ambiente de Desenvolvimento:** Docker (opcional, mas recomendado)
    *   **Justificativa:** Para garantir a consistência do ambiente de desenvolvimento e produção, facilitando a implantação e evitando problemas de compatibilidade.

Esta combinação de tecnologias oferece um equilíbrio entre flexibilidade, desempenho, escalabilidade e facilidade de desenvolvimento, permitindo a construção de um sistema robusto e moderno.




## Resumo e Conclusão da Análise de Requisitos

Este documento detalha os requisitos funcionais e não funcionais para o sistema de estoque de peças de carro, com foco no controle interno e na integração com o Mercado Livre. A arquitetura proposta, utilizando Python com Flask para o backend, PostgreSQL para o banco de dados e React para o frontend, visa fornecer uma solução robusta, escalável e amigável ao usuário.

O sistema permitirá um gerenciamento eficiente do vasto inventário de peças, automatizando processos críticos como a atualização de estoque após vendas no Mercado Livre e fornecendo insights valiosos através de relatórios. A interface intuitiva garantirá que os membros da equipe possam operar o sistema com facilidade, enquanto a integração com o Mercado Livre otimizará o processo de vendas online.

Os próximos passos envolverão a pesquisa aprofundada da API do Mercado Livre para entender suas capacidades e limitações, seguida pelo design detalhado da arquitetura do banco de dados e o desenvolvimento do sistema.


