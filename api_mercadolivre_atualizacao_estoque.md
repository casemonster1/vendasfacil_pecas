

# Documentação da API do Mercado Livre - Atualização de Estoque

## Visão Geral

Para sincronizar o estoque entre seu sistema interno e o Mercado Livre, é necessário utilizar a API para atualizar a quantidade disponível de seus anúncios. Isso é feito através de uma requisição `PUT` para o recurso de `items`.

## Atualizando o Estoque de um Item

Para atualizar o estoque de um item, você deve fazer uma requisição `PUT` para o endpoint do item, incluindo o campo `available_quantity` no corpo da requisição.

**Chamada:**

```
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -H "Accept: application/json" -d
{
  "available_quantity": 10
}
https://api.mercadolibre.com/items/$ITEM_ID
```

**Parâmetros Importantes:**

*   `$ACCESS_TOKEN`: O token de acesso obtido através do processo de autenticação OAuth 2.0.
*   `$ITEM_ID`: O ID do item (anúncio) no Mercado Livre que você deseja atualizar.
*   `available_quantity`: A nova quantidade disponível do item. Este é o campo crucial para a atualização do estoque.

**Considerações:**

*   Quando um item está `active` (ativo), você pode modificar a `available_quantity`.
*   Se o item tiver variações, a atualização do estoque pode ser mais complexa e exigir a manipulação de variações específicas.
*   É importante garantir que o `ITEM_ID` corresponda ao produto correto no seu sistema interno para evitar inconsistências.

## Próximos Passos

Com as informações sobre autenticação, notificações, pedidos e atualização de estoque, temos uma base sólida para o design da arquitetura e banco de dados do sistema. O próximo passo é consolidar todas essas informações e projetar o esquema do banco de dados e a arquitetura geral do sistema, considerando a integração com o Mercado Livre e as funcionalidades de controle interno.


