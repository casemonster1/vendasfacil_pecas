# Documentação da API do Mercado Livre - Gerenciamento de Pedidos (Orders)

## Visão Geral

Uma `order` (pedido) no Mercado Livre representa uma transação de compra realizada por um cliente em um anúncio. Ela contém todas as informações detalhadas sobre o produto, as condições de compra escolhidas pelo cliente e a possibilidade de reservar e/ou descontar o estoque. As informações da `order` são replicadas nas contas do comprador e do vendedor.

## Recebendo uma Ordem

Quando uma nova ordem é criada, seus detalhes podem ser consultados através de uma requisição `GET` para o recurso de `orders`.

**Chamada:**

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/orders/$ORDER_ID
```

**Exemplo de Resposta (JSON):**

```json
{
   "id": 2000003508897196,
   "date_created": "2022-04-08T17:01:30.000-04:00",
   "date_closed": "2022-04-08T17:01:33.000-04:00",
   "last_updated": "2022-04-08T17:03:32.000-04:00",
   "total_amount": 50,
   "paid_amount": 50,
   "order_items": [
       {
           "item": {
               "id": "MLB2608564035",
               "title": "Camiseta Basica",
               "category_id": "MLB31447",
               "variation_id": 174390848694,
               "variation_attributes": [
                   {
                       "id": "SIZE",
                       "name": "Tamanho",
                       "value_id": "2282666",
                       "value_name": "M"
                   },
                   {
                       "id": "COLOR",
                       "name": "Cor",
                       "value_id": "52049",
                       "value_name": "Preto"
                   }
               ],
               "warranty": "Sem garantia",
               "condition": "new",
               "seller_sku": null,
               "global_price": null,
               "net_weight": null
           },
           "quantity": 1,
           "requested_quantity": {
               "value": 1,
               "measure": "unit"
           },
           "picked_quantity": null,
           "unit_price": 50,
           "full_unit_price": 50,
           "currency_id": "BRL",
           "manufacturing_days": null,
           "sale_fee": 12,
           "listing_type_id": "gold_special"
       }
   ],
   "currency_id": "BRL",
   "payments": [
       {
           "id": 21463688923,
           "order_id": 2000003508897196,
           "payer_id": 266272126,
           "site_id": "MLB",
           "reason": "Camiseta Basica",
           "payment_method_id": "account_money",
           "currency_id": "BRL",
           "installments": 1,
           "status": "approved",
           "status_detail": "accredited",
           "transaction_amount": 50,
           "date_approved": "2022-04-08T17:01:32.000-04:00",
           "date_created": "2022-04-08T17:01:32.000-04:00",
           "date_last_modified": "2022-04-08T17:01:44.000-04:00"
       }
   ],
   "shipping": {
       "id": 41297142475
   },
   "status": "paid",
   "status_detail": null
}
```

**Campos Chave para o Sistema de Estoque:**

*   `id`: ID único do pedido.
*   `date_created`: Data de criação do pedido.
*   `last_updated`: Última atualização do pedido.
*   `total_amount`: Valor total do pedido.
*   `paid_amount`: Valor pago pelo pedido.
*   `order_items`: Array contendo os itens do pedido. Para cada item:
    *   `item.id`: ID do item (produto) no Mercado Livre.
    *   `item.title`: Título do item.
    *   `quantity`: Quantidade do item comprado.
    *   `unit_price`: Preço unitário do item.
*   `payments`: Array contendo os detalhes do pagamento. Para cada pagamento:
    *   `status`: Status do pagamento (ex: `approved`, `pending`, `rejected`).
    *   `status_detail`: Detalhe do status do pagamento (ex: `accredited`).
*   `shipping`: Informações de envio (contém o ID do envio, que pode ser usado para obter mais detalhes sobre o envio).
*   `status`: Status geral do pedido (ex: `paid`, `pending`, `cancelled`).

## Relação com a Atualização de Estoque

O campo `order_items.quantity` é crucial para o sistema de estoque. Quando o `payments.status` for `approved` e o `order.status` for `paid`, o sistema interno deve descontar a `quantity` de cada `item.id` correspondente do estoque. Alternativamente, o status do item no estoque interno pode ser alterado para "Vendido, Aguardando Entrega" até a confirmação do envio.

## Próximos Passos

Com as informações sobre autenticação, notificações e pedidos, o próximo passo é pesquisar como atualizar o estoque de um item no Mercado Livre via API. Em seguida, será possível consolidar todas as informações para o design da arquitetura e banco de dados.

