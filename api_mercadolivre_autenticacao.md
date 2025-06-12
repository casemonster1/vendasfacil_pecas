# Documentação da API do Mercado Livre - Autenticação e Autorização

## Visão Geral

Para começar a utilizar os recursos da API do Mercado Livre, é fundamental entender os processos de Autenticação e Autorização. Estes processos permitem que sua aplicação interaja com os dados privados do usuário (vendedor) de forma segura.

## Envio do Access Token no Header

Todas as chamadas para a API do Mercado Livre devem incluir o `access_token` no cabeçalho `Authorization` no formato `Bearer`.

Exemplo:

```
curl -H 'Authorization: Bearer APP_USR-12345678-031820-X-12345678' \
https://api.mercadolibre.com/users/me
```

## Autenticação

O Mercado Livre utiliza um processo de autenticação baseado em senhas para verificar a identidade do usuário.

## Autorização (OAuth 2.0)

A autorização é o processo que concede acesso a recursos privados. O Mercado Livre utiliza o protocolo OAuth 2.0, especificamente o `Authorization Code Grant Type (Server Side)`, para este fim. Este protocolo garante confidencialidade, integridade e disponibilidade dos dados.

### Fluxo Server Side (Passo a Passo)

1.  **Redirecionamento para o Mercado Livre:** A aplicação redireciona o usuário para uma URL de autorização do Mercado Livre.
2.  **Autenticação do Usuário:** O Mercado Livre cuida da autenticação do usuário.
3.  **Página de Autorização:** O usuário é apresentado a uma página onde deve autorizar a aplicação a acessar seus dados.
4.  **Troca do Código por Token:** Após a autorização, o Mercado Livre redireciona o usuário de volta para a `redirect_uri` configurada na aplicação, incluindo um `code` temporário. A aplicação então faz uma requisição POST para um endpoint do Mercado Livre para trocar este `code` por um `access_token` e um `refresh_token`.
5.  **Utilização do Access Token:** Com o `access_token`, a aplicação pode realizar chamadas à API do Mercado Livre para acessar os dados privados do usuário.

### Detalhes da Autorização

Para iniciar o processo de autorização, a aplicação deve redirecionar o usuário para a seguinte URL (exemplo para Brasil):

```
https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=$APP_ID&redirect_uri=$YOUR_URL&code_challenge=$CODE_CHALLENGE&code_challenge_method=$CODE_METHOD
```

**Parâmetros Importantes:**

*   `response_type`: Deve ser `code` para obter um `access_token`.
*   `redirect_uri`: A URL para a qual o Mercado Livre redirecionará o usuário após a autorização. Deve corresponder **exatamente** à URL registrada nas configurações da sua aplicação.
*   `client_id`: O ID da sua aplicação, obtido após a criação da mesma no painel de desenvolvedores do Mercado Livre.
*   `state` (recomendado): Um parâmetro para aumentar a segurança, garantindo que a resposta pertence a uma solicitação iniciada pela sua aplicação.
*   `code_challenge` e `code_challenge_method` (opcionais, mas obrigatórios se PKCE habilitado): Usados para o fluxo PKCE (Proof Key for Code Exchange), que adiciona uma camada extra de segurança.

### Troca do Code por um Token

Após o redirecionamento para a `redirect_uri` com o `code`, a aplicação deve fazer uma requisição POST para o endpoint de token do Mercado Livre para obter o `access_token` e o `refresh_token`.

### Refresh Token

O `access_token` tem um tempo de expiração (geralmente 6 horas). Após a expiração, é necessário usar o `refresh_token` para obter um novo `access_token` sem a necessidade de o usuário autorizar novamente a aplicação. O `refresh_token` geralmente tem uma validade mais longa (6 meses).

## Próximos Passos

Para continuar a pesquisa da API, é necessário encontrar a documentação sobre:

*   **Webhooks:** Como configurar e receber notificações de pagamento e pedido.
*   **Pedidos:** Endpoints para obter detalhes de pedidos (itens, comprador, status).
*   **Estoque:** Endpoints para atualizar a quantidade de produtos.
*   **Anúncios (Opcional):** Endpoints para criar e atualizar anúncios de produtos.



