

# Documentação da API do Mercado Livre - Notificações (Webhooks)

## Visão Geral

As notificações permitem que sua aplicação receba informações em tempo real sobre eventos que ocorrem no Mercado Livre, como alterações em itens, perguntas, compras, pagamentos e envios. Isso elimina a necessidade de consultar a API continuamente (polling).

## Como se Inscrever para Notificações

Para receber notificações, você precisa configurar sua aplicação no painel "Minhas Aplicações" no Mercado Livre. Lá, você deve:

*   **Notifications Callback URL:** Configurar a URL pública do seu domínio onde você deseja receber as notificações (ex: `http://myshoes-app.com/callbacks`).
*   **Topics:** Selecionar os tópicos (eventos) para os quais você deseja receber notificações.

## Tópicos Disponíveis Relevantes para o Sistema de Estoque

*   `items`: Notificações sobre quaisquer alterações em um item publicado.
*   `payments`: Notificações quando um pagamento é criado para um pedido, ou quando seu status muda.
*   `orders_v2`: Notificações após a criação e alterações em vendas confirmadas (recomendado).
*   `shipments`: Notificações após a criação e alterações de envio para suas vendas confirmadas.
*   `stock_locations`: Notificações quando as `stock_locations` de um `user_product` são modificadas, seja aumentando ou diminuindo o campo de quantidade.

## Eventos que Disparam Notificações

Qualquer alteração em qualquer tópico do JSON de um recurso irá disparar as notificações relevantes. Sua aplicação deve sempre processar as notificações e, em seguida, consultar o recurso relevante na API para verificar as mudanças.

## Considerações Importantes

*   Sua integração deve retornar um `HTTP 200` em até 500 milissegundos após receber a notificação para evitar que o Mercado Livre desative os tópicos de suas notificações.
*   Se o `HTTP 200` não for retornado, a mensagem será considerada "não recebida" e haverá novas tentativas de envio em intervalos de 1 hora. Após esse período, mensagens não aceitas serão descartadas.
*   É aconselhável trabalhar com filas (queues) para processar um grande volume de notificações. O servidor deve confirmar imediatamente o recebimento da notificação (`HTTP 200`) e, em seguida, enfileirar a tarefa de consultar a API para obter os detalhes, evitando novas tentativas de notificação e notificações duplicadas.

## Obtendo os Detalhes

Após receber uma notificação, você precisará fazer uma requisição `GET` para o recurso (`resource`) especificado na notificação para obter os detalhes completos. Por exemplo:

### Notificação de `items`

```json
{
  "_id":"f9f08571-1f65-4c46-9e0a-c0f43faas1557e",      
  "resource": "/items/MLA686791111",
  "user_id": 123456789,
  "topic": "items",
  "application_id": 2069392825111111,
  "attempts": 1,
  "sent": "2017-10-09T13:44:33.006Z",
  "received": "2017-10-09T13:44:32.984Z"
}
```

Requisição para obter detalhes do item:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID
```

### Notificação de `orders`

```json
{
  "_id":"f9f08571-1f65-4c46-9e0a-c0f43faas1557e",   
  "resource": "/orders/1499111111",
  "user_id": 123456789,
  "topic": "orders",
  "application_id": 2069392825111111,
  "attempts": 1,
  "sent": "2017-10-09T13:58:23.347Z",
  "received": "2017-10-09T13:58:23.329Z"
}
```

Requisição para obter detalhes do pedido:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/orders/$ORDER_ID
```

## Próximos Passos

Com as informações de autenticação e notificações, o próximo passo é detalhar os endpoints específicos para obter informações de pedidos e atualizar o estoque. Em seguida, será possível iniciar o design do banco de dados e a arquitetura geral do sistema.


