import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Package, 
  ShoppingCart, 
  TrendingUp, 
  AlertTriangle,
  DollarSign,
  Users
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:5001/api'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalProdutos: 0,
    produtosEstoqueBaixo: 0,
    totalPedidos: 0,
    valorTotalVendas: 0
  })
  const [produtosEstoqueBaixo, setProdutosEstoqueBaixo] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Buscar estatísticas de produtos
      const produtosResponse = await fetch(`${API_BASE_URL}/produtos`)
      const produtosData = await produtosResponse.json()
      
      // Buscar produtos com estoque baixo
      const estoqueBaixoResponse = await fetch(`${API_BASE_URL}/produtos/estoque-baixo`)
      const estoqueBaixoData = await estoqueBaixoResponse.json()
      
      // Buscar estatísticas de pedidos
      const pedidosStatsResponse = await fetch(`${API_BASE_URL}/pedidos/estatisticas`)
      const pedidosStatsData = await pedidosStatsResponse.json()

      setStats({
        totalProdutos: produtosData.total || 0,
        produtosEstoqueBaixo: estoqueBaixoData.length || 0,
        totalPedidos: pedidosStatsData.total_pedidos || 0,
        valorTotalVendas: pedidosStatsData.valor_total_vendas || 0
      })
      
      setProdutosEstoqueBaixo(estoqueBaixoData.slice(0, 5)) // Mostrar apenas os primeiros 5
      
    } catch (error) {
      console.error('Erro ao buscar dados do dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Visão geral do sistema de estoque</p>
      </div>

      {/* Cards de estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Produtos</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalProdutos}</div>
            <p className="text-xs text-muted-foreground">
              Produtos cadastrados no sistema
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Estoque Baixo</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">{stats.produtosEstoqueBaixo}</div>
            <p className="text-xs text-muted-foreground">
              Produtos com estoque ≤ 5 unidades
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Pedidos</CardTitle>
            <ShoppingCart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalPedidos}</div>
            <p className="text-xs text-muted-foreground">
              Pedidos do Mercado Livre
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Valor Total Vendas</CardTitle>
            <DollarSign className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {formatCurrency(stats.valorTotalVendas)}
            </div>
            <p className="text-xs text-muted-foreground">
              Vendas pagas no ML
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Produtos com estoque baixo */}
      {produtosEstoqueBaixo.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-500" />
              Produtos com Estoque Baixo
            </CardTitle>
            <CardDescription>
              Produtos que precisam de reposição urgente
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {produtosEstoqueBaixo.map((produto) => (
                <div key={produto.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium">{produto.nome}</h4>
                    <p className="text-sm text-muted-foreground">
                      SKU: {produto.referencia_sku} | {produto.categoria}
                    </p>
                  </div>
                  <div className="text-right">
                    <Badge variant={produto.quantidade_estoque === 0 ? "destructive" : "secondary"}>
                      {produto.quantidade_estoque} unidades
                    </Badge>
                    <p className="text-sm text-muted-foreground mt-1">
                      {formatCurrency(produto.preco_venda)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Resumo rápido */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Resumo do Sistema</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm">Produtos ativos</span>
              <span className="font-medium">{stats.totalProdutos}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Alertas de estoque</span>
              <span className="font-medium text-orange-600">{stats.produtosEstoqueBaixo}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Pedidos processados</span>
              <span className="font-medium">{stats.totalPedidos}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Ações Rápidas</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-sm space-y-2">
              <p>• Verificar produtos com estoque baixo</p>
              <p>• Atualizar preços de produtos</p>
              <p>• Sincronizar com Mercado Livre</p>
              <p>• Gerar relatório de vendas</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

