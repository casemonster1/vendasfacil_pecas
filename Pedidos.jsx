import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { 
  ShoppingCart, 
  Search, 
  Filter,
  Calendar,
  User,
  Package,
  DollarSign
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:5001/api'

export default function Pedidos() {
  const [pedidos, setPedidos] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('')

  useEffect(() => {
    fetchPedidos()
  }, [])

  const fetchPedidos = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/pedidos`)
      const data = await response.json()
      setPedidos(data.pedidos || [])
    } catch (error) {
      console.error('Erro ao buscar pedidos:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredPedidos = pedidos.filter(pedido => {
    const matchesSearch = pedido.id.toString().includes(searchTerm) ||
                         pedido.comprador_nickname?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = !selectedStatus || pedido.status === selectedStatus
    return matchesSearch && matchesStatus
  })

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getStatusBadge = (status) => {
    const statusMap = {
      'paid': { variant: 'default', label: 'Pago' },
      'pending': { variant: 'secondary', label: 'Pendente' },
      'cancelled': { variant: 'destructive', label: 'Cancelado' },
      'confirmed': { variant: 'default', label: 'Confirmado' }
    }
    
    const statusInfo = statusMap[status] || { variant: 'secondary', label: status }
    
    return (
      <Badge variant={statusInfo.variant}>
        {statusInfo.label}
      </Badge>
    )
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
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
        <h1 className="text-3xl font-bold text-gray-900">Pedidos</h1>
        <p className="text-gray-600">Gerencie os pedidos do Mercado Livre</p>
      </div>

      {/* Filtros */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar por ID do pedido ou comprador..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        
        <Select value={selectedStatus} onValueChange={setSelectedStatus}>
          <SelectTrigger className="w-full sm:w-48">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue placeholder="Todos os status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todos os status</SelectItem>
            <SelectItem value="paid">Pago</SelectItem>
            <SelectItem value="pending">Pendente</SelectItem>
            <SelectItem value="cancelled">Cancelado</SelectItem>
            <SelectItem value="confirmed">Confirmado</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Lista de pedidos */}
      <div className="space-y-4">
        {filteredPedidos.map((pedido) => (
          <Card key={pedido.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <ShoppingCart className="h-5 w-5" />
                    Pedido #{pedido.id}
                  </CardTitle>
                  <CardDescription className="flex items-center gap-4 mt-2">
                    <span className="flex items-center gap-1">
                      <Calendar className="h-4 w-4" />
                      {formatDate(pedido.data_criacao)}
                    </span>
                    {pedido.comprador_nickname && (
                      <span className="flex items-center gap-1">
                        <User className="h-4 w-4" />
                        {pedido.comprador_nickname}
                      </span>
                    )}
                  </CardDescription>
                </div>
                <div className="text-right">
                  {getStatusBadge(pedido.status)}
                  <div className="text-2xl font-bold text-green-600 mt-2">
                    {formatCurrency(pedido.total_amount)}
                  </div>
                </div>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              {/* Informações do pedido */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="font-medium text-gray-700">Valor Pago</p>
                  <p className="text-green-600 font-semibold">
                    {formatCurrency(pedido.paid_amount)}
                  </p>
                </div>
                <div>
                  <p className="font-medium text-gray-700">Moeda</p>
                  <p>{pedido.currency_id}</p>
                </div>
                {pedido.shipping_id && (
                  <div>
                    <p className="font-medium text-gray-700">ID do Envio</p>
                    <p>{pedido.shipping_id}</p>
                  </div>
                )}
              </div>

              {/* Itens do pedido */}
              {pedido.itens && pedido.itens.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <Package className="h-4 w-4" />
                    Itens do Pedido
                  </h4>
                  <div className="space-y-2">
                    {pedido.itens.map((item, index) => (
                      <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                        <div className="flex-1">
                          <p className="font-medium">{item.titulo_item}</p>
                          <p className="text-sm text-gray-600">
                            ID: {item.ml_item_id} | Qtd: {item.quantidade}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">
                            {formatCurrency(item.preco_unitario)}
                          </p>
                          <p className="text-sm text-gray-600">
                            Total: {formatCurrency(item.preco_unitario * item.quantidade)}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Informações de pagamento */}
              {pedido.pagamentos && pedido.pagamentos.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <DollarSign className="h-4 w-4" />
                    Pagamentos
                  </h4>
                  <div className="space-y-2">
                    {pedido.pagamentos.map((pagamento, index) => (
                      <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">
                            {pagamento.metodo_pagamento || 'Método não informado'}
                          </p>
                          <p className="text-sm text-gray-600">
                            ID: {pagamento.id}
                          </p>
                        </div>
                        <div className="text-right">
                          {getStatusBadge(pagamento.status)}
                          <p className="font-semibold mt-1">
                            {formatCurrency(pagamento.transaction_amount)}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Detalhes adicionais */}
              {pedido.status_detalhe && (
                <div className="text-sm text-gray-600">
                  <strong>Detalhe do Status:</strong> {pedido.status_detalhe}
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredPedidos.length === 0 && !loading && (
        <div className="text-center py-12">
          <ShoppingCart className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhum pedido encontrado
          </h3>
          <p className="text-gray-600">
            {searchTerm || selectedStatus 
              ? 'Tente ajustar os filtros de busca'
              : 'Os pedidos do Mercado Livre aparecerão aqui'
            }
          </p>
        </div>
      )}
    </div>
  )
}

