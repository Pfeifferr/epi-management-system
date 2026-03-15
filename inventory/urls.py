from django.urls import path
from . import views

urlpatterns = [
    # Gestão de Catálogo de EPIs (Equipamentos)
    path('lista/', views.lista_inventory, name='lista_epis'),
    path('novo/', views.criar_epi, name='criar_epi'),
    path('editar/<int:pk>/', views.editar_epi, name='editar_epi'),
    path('excluir/<int:pk>/', views.excluir_epi, name='excluir_epi'),
    
    # Fluxo de Movimentação e Custódia (Entregas e Devoluções)
    path('entregas/', views.lista_entregas, name='lista_entregas'),
    path('entregas/registrar/', views.registrar_entrega, name='registrar_entrega'),
    path('entregas/devolucao/<int:pk>/', views.registrar_devolucao, name='registrar_devolucao'),
    
    # Inteligência e Compliance (Busca e Documentação Legal)
    path('busca/', views.busca_geral, name='busca_geral'),
    path('entregas/recibo/<int:pk>/', views.gerar_recibo_pdf, name='gerar_recibo_pdf'),
    path('entregas/ficha-nr6/<int:usuario_id>/', views.gerar_ficha_nr6_pdf, name='gerar_ficha_nr6_pdf'),
]