**Funcionalidades principais:** 

- [ ] Parser (Análise) de uma consulta SQL; 
- [ ] Gerar e exibir a ordem de execução da consulta; 
- [ ] Geração do grafo de operadores da consulta; 
- [ ] Exibição dos resultados na interface gráfica; 


**Exemplos de querys a serem feitas:**
```
    # Exemplo 1
    Select cliente.nome, pedido.idPedido, pedido.DataPedido, pedido.ValorTotalPedido
    from Cliente Join pedido on cliente.idcliente = pedido.Cliente_idCliente
    where cliente.TipoCliente_idTipoCliente = 1 and pedido.ValorTotalPedido = 0;

    # Exemplo 2
    Select cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido
    from Cliente Join pedido on cliente.idcliente = pedido.Cliente_idCliente
    Join Status on Status.idstatus = Pedido.status_idstatus
    where Status.descricao = 'Aberto' and cliente.TipoCliente_idTipoCliente = 1 and pedido.ValorTotalPedido = 0;

    # Exemplo 3
    Select cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido, produto.QuantEstoque
    from Cliente Join pedido on cliente.idcliente = pedido.Cliente_idCliente
    Join Status on Status.idstatus = Pedido.status_idstatus
    Join pedido_has_produto on pedido.idPedido = pedido_has_produto.Pedido_idPedido
    Join produto on produto.idProduto = pedido_has_produto.Produto_idProduto
    where Status.descricao = 'Aberto' and cliente.TipoCliente_idTipoCliente = 1 and pedido.ValorTotalPedido = 0 and produto.QuantEstoque > 0;

    # Exemplo 4
    Select cliente.nome, tipocliente.descricao, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido, categoria.descricao, produto.QuantEstoque
    from Cliente Join pedido on cliente.idcliente = pedido.Cliente_idCliente
    Join tipocliente on cliente.tipocliente_idtipocliente = tipocliente.idTipoCliente
    Join endereco on cliente.idcliente = endereco.Cliente_idCliente
    Join Status on Status.idstatus = Pedido.status_idstatus
    Join pedido_has_produto on pedido.idPedido = pedido_has_produto.Pedido_idPedido
    Join produto on produto.idProduto = pedido_has_produto.Produto_idProduto
    Join categoria on categoria.idcategoria = produto.Categoria_idCategoria
    where Status.descricao = 'Aberto' and cliente.email = 'Luffy@gmail.com' and pedido.ValorTotalPedido = 0 
    and produto.preco > 5000 and endereco.cidade = 'Gramado';
```