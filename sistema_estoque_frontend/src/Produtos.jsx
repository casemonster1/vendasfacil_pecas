import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog'
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { 
  Plus, 
  Search, 
  Edit, 
  Trash2, 
  Package,
  AlertTriangle,
  Filter
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:5001/api'

export default function Produtos() {
  const [produtos, setProdutos] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [categorias, setCategorias] = useState([])
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)
  const [formData, setFormData] = useState({
    nome: '',
    descricao: '',
    referencia_sku: '',
    preco_venda: '',
    quantidade_estoque: '',
    localizacao_galpao: '',
    categoria: '',
    subcategoria: '',
    marca_peca: '',
    condicao: 'Novo'
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    fetchProdutos()
    fetchCategorias()
  }, [])

  const fetchProdutos = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/produtos`)
      const data = await response.json()
      setProdutos(data.produtos || [])
    } catch (error) {
      console.error('Erro ao buscar produtos:', error)
      setError('Erro ao carregar produtos')
    } finally {
      setLoading(false)
    }
  }

  const fetchCategorias = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/produtos/categorias`)
      const data = await response.json()
      setCategorias(data || [])
    } catch (error) {
      console.error('Erro ao buscar categorias:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    try {
      const url = editingProduct 
        ? `${API_BASE_URL}/produtos/${editingProduct.id}`
        : `${API_BASE_URL}/produtos`
      
      const method = editingProduct ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          preco_venda: parseFloat(formData.preco_venda),
          quantidade_estoque: parseInt(formData.quantidade_estoque)
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess(editingProduct ? 'Produto atualizado com sucesso!' : 'Produto criado com sucesso!')
        setIsDialogOpen(false)
        resetForm()
        fetchProdutos()
        fetchCategorias()
      } else {
        setError(data.error || 'Erro ao salvar produto')
      }
    } catch (err) {
      setError('Erro de conexão com o servidor')
    }
  }

  const handleEdit = (produto) => {
    setEditingProduct(produto)
    setFormData({
      nome: produto.nome,
      descricao: produto.descricao,
      referencia_sku: produto.referencia_sku,
      preco_venda: produto.preco_venda.toString(),
      quantidade_estoque: produto.quantidade_estoque.toString(),
      localizacao_galpao: produto.localizacao_galpao || '',
      categoria: produto.categoria || '',
      subcategoria: produto.subcategoria || '',
      marca_peca: produto.marca_peca || '',
      condicao: produto.condicao
    })
    setIsDialogOpen(true)
  }

  const handleDelete = async (id) => {
    if (!confirm('Tem certeza que deseja deletar este produto?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/produtos/${id}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        setSuccess('Produto deletado com sucesso!')
        fetchProdutos()
      } else {
        setError('Erro ao deletar produto')
      }
    } catch (err) {
      setError('Erro de conexão com o servidor')
    }
  }

  const resetForm = () => {
    setFormData({
      nome: '',
      descricao: '',
      referencia_sku: '',
      preco_venda: '',
      quantidade_estoque: '',
      localizacao_galpao: '',
      categoria: '',
      subcategoria: '',
      marca_peca: '',
      condicao: 'Novo'
    })
    setEditingProduct(null)
  }

  const filteredProdutos = produtos.filter(produto => {
    const matchesSearch = produto.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         produto.referencia_sku.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = !selectedCategory || produto.categoria === selectedCategory
    return matchesSearch && matchesCategory
  })

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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-48 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Produtos</h1>
          <p className="text-gray-600">Gerencie o estoque de peças de carro</p>
        </div>
        
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="h-4 w-4 mr-2" />
              Novo Produto
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>
                {editingProduct ? 'Editar Produto' : 'Novo Produto'}
              </DialogTitle>
              <DialogDescription>
                {editingProduct ? 'Atualize as informações do produto' : 'Adicione um novo produto ao estoque'}
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="nome">Nome do Produto *</Label>
                  <Input
                    id="nome"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="referencia_sku">SKU/Referência *</Label>
                  <Input
                    id="referencia_sku"
                    value={formData.referencia_sku}
                    onChange={(e) => setFormData({...formData, referencia_sku: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="descricao">Descrição</Label>
                <Textarea
                  id="descricao"
                  value={formData.descricao}
                  onChange={(e) => setFormData({...formData, descricao: e.target.value})}
                  rows={3}
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="preco_venda">Preço de Venda *</Label>
                  <Input
                    id="preco_venda"
                    type="number"
                    step="0.01"
                    value={formData.preco_venda}
                    onChange={(e) => setFormData({...formData, preco_venda: e.target.value})}
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="quantidade_estoque">Quantidade em Estoque *</Label>
                  <Input
                    id="quantidade_estoque"
                    type="number"
                    value={formData.quantidade_estoque}
                    onChange={(e) => setFormData({...formData, quantidade_estoque: e.target.value})}
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="localizacao_galpao">Localização no Galpão</Label>
                  <Input
                    id="localizacao_galpao"
                    value={formData.localizacao_galpao}
                    onChange={(e) => setFormData({...formData, localizacao_galpao: e.target.value})}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="categoria">Categoria</Label>
                  <Input
                    id="categoria"
                    value={formData.categoria}
                    onChange={(e) => setFormData({...formData, categoria: e.target.value})}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="subcategoria">Subcategoria</Label>
                  <Input
                    id="subcategoria"
                    value={formData.subcategoria}
                    onChange={(e) => setFormData({...formData, subcategoria: e.target.value})}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="marca_peca">Marca da Peça</Label>
                  <Input
                    id="marca_peca"
                    value={formData.marca_peca}
                    onChange={(e) => setFormData({...formData, marca_peca: e.target.value})}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="condicao">Condição</Label>
                  <Select value={formData.condicao} onValueChange={(value) => setFormData({...formData, condicao: value})}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Novo">Novo</SelectItem>
                      <SelectItem value="Usado">Usado</SelectItem>
                      <SelectItem value="Recondicionado">Recondicionado</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div className="flex justify-end gap-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancelar
                </Button>
                <Button type="submit">
                  {editingProduct ? 'Atualizar' : 'Criar'} Produto
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Filtros */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar por nome ou SKU..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        
        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
          <SelectTrigger className="w-full sm:w-48">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue placeholder="Todas as categorias" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todas as categorias</SelectItem>
            {categorias.map((categoria) => (
              <SelectItem key={categoria} value={categoria}>
                {categoria}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Alertas */}
      {success && (
        <Alert>
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      )}

      {/* Lista de produtos */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProdutos.map((produto) => (
          <Card key={produto.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <CardTitle className="text-lg">{produto.nome}</CardTitle>
                  <CardDescription>SKU: {produto.referencia_sku}</CardDescription>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleEdit(produto)}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(produto.id)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-2xl font-bold text-green-600">
                  {formatCurrency(produto.preco_venda)}
                </span>
                <Badge 
                  variant={produto.quantidade_estoque <= 5 ? "destructive" : "secondary"}
                  className="flex items-center gap-1"
                >
                  <Package className="h-3 w-3" />
                  {produto.quantidade_estoque}
                </Badge>
              </div>
              
              {produto.quantidade_estoque <= 5 && (
                <div className="flex items-center gap-2 text-orange-600 text-sm">
                  <AlertTriangle className="h-4 w-4" />
                  Estoque baixo
                </div>
              )}
              
              <div className="space-y-1 text-sm text-muted-foreground">
                {produto.categoria && (
                  <p><strong>Categoria:</strong> {produto.categoria}</p>
                )}
                {produto.marca_peca && (
                  <p><strong>Marca:</strong> {produto.marca_peca}</p>
                )}
                {produto.localizacao_galpao && (
                  <p><strong>Localização:</strong> {produto.localizacao_galpao}</p>
                )}
                <p><strong>Condição:</strong> {produto.condicao}</p>
              </div>
              
              {produto.descricao && (
                <p className="text-sm text-gray-600 line-clamp-2">
                  {produto.descricao}
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredProdutos.length === 0 && !loading && (
        <div className="text-center py-12">
          <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhum produto encontrado
          </h3>
          <p className="text-gray-600">
            {searchTerm || selectedCategory 
              ? 'Tente ajustar os filtros de busca'
              : 'Comece adicionando seu primeiro produto'
            }
          </p>
        </div>
      )}
    </div>
  )
}

