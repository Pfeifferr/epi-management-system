from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views 

# Configuração de Handlers de Erro Personalizados (Compliance de Acesso)
handler403 = 'accounts.views.custom_403'

urlpatterns = [
    # Interface Administrativa do Framework
    path('admin/', admin.site.urls),
    
    # Core do Sistema: Dashboard Principal
    path('', accounts_views.dashboard, name='dashboard'), 
    
    # Módulos Funcionais (Encapsulados via Include)
    path('accounts/', include('accounts.urls')), 
    path('inventory/', include('inventory.urls')),
]

# Servidor de Ativos de Mídia em Ambiente de Desenvolvimento (Media Serving)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)