# 🛡️ EPI Management System

**Controle inteligente de Equipamentos de Proteção Individual e Conformidade (NR-6)**

O **EPI Management System** é uma solução completa que desenvolvi para a automação da segurança do trabalho. O sistema substitui as antigas fichas de papel por um fluxo digital auditável, garantindo que a entrega, a substituição e o estoque de EPIs estejam sempre em conformidade com as normas regulamentadoras.

### 🎯 O Problema que Resolvi
* **Fim do Papel:** Digitalizei totalmente as fichas de entrega de EPI.
* **Segurança Jurídica:** Criei registros precisos com data, hora e confirmação digital.
* **Gestão de Estoque:** Implementei alertas de estoque baixo e controle de validade.
* **Transparência:** Desenvolvi um dashboard em tempo real para controle de gestão.

## 🚀 Tecnologias Utilizadas

O projeto foi construído com uma stack moderna, focada em estabilidade e escalabilidade:

| Camada | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| **Linguagem** | [Python 3.11+](https://www.python.org/) | Core do sistema e lógica de negócio. |
| **Framework** | [Django 5.0](https://www.djangoproject.com/) | Estrutura de backend, ORM e Admin. |
| **Banco de Dados** | [MySQL 8.0](https://www.mysql.com/) | Armazenamento seguro e relacional dos dados. |
| **Interface** | [Bootstrap 5](https://getbootstrap.com/) | UI Responsiva e componentes modernos. |
| **Relatórios** | [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) | Geração de Fichas de EPI em formato PDF. |
| **Estilos** | CSS3 Personalizado | Design System exclusivo do sistema. |

## ✨ Funcionalidades e Diferenciais

O **EPI Manager** foi projetado para cobrir todo o ciclo de vida do equipamento dentro de uma organização, unindo conformidade legal (NR-6) com automação inteligente:

* **🔐 Sistema de Autenticação com Hierarquia (RBAC): Controle de acesso granular com perfis de Administrador (gestão total), SST/Técnico (gestão operacional e de inventário, com permissão para cadastrar apenas Colaboradores), Almoxarife (foco em movimentações) e Colaborador (interface restrita para consulta de sua própria ficha e histórico).
* **📊 Dashboard de Indicadores (BI):** Visualização em tempo real do status do estoque, pendências de devolução e gráficos analíticos de movimentação semanal e ranking de EPIs.
* **🚨 Sistema de Alertas Proativo:** Monitoramento inteligente no Dashboard para:
    * **Validade de CA (NR-6):** Alerta visual crítico e bloqueio automático de novas entregas para equipamentos com Certificado de Aprovação vencido.
    * **Exames Médicos (ASO/NR-7):** Notificação de colaboradores com exames médicos vencendo, garantindo a saúde ocupacional.
    * **Análise Preditiva de Vida Útil:** Cálculo automático da durabilidade dos itens, gerando alertas de troca com margem de 5 dias para planejamento.
* **👥 Gestão de Colaboradores & Perfis:** Cadastro detalhado de funcionários com **upload de foto de perfil**, organização por setores/cargos e monitoramento de histórico de saúde.
* **📦 Gestão de Inventário Técnico & Visual: Controle completo de CA, fabricante e parâmetros de vida útil, com suporte a feedback visual por cores na listagem de equipamentos, sinalizando automaticamente níveis críticos de estoque para reposição.
* **🔄 Fluxo de Baixa Inteligente:** Lógica de retorno ao estoque baseada no estado do item (Devolvido, Danificado ou Extraviado), com ajuste automático de saldo no inventário.
* **📑 Registro de Movimentações:** Histórico imutável de custódia, garantindo a rastreabilidade total de quem utilizou cada equipamento e por quanto tempo.
* **📄 Emissão de Documentos (PDF):** Geração automática da ficha de EPI conforme a **NR-6**, com todo o histórico de entregas pronto para assinatura e auditorias fiscais.

## 📸 Demonstração do Sistema

Abaixo, as interfaces principais e os diferentes níveis de acesso do sistema:

| 🔐 Portal de Acesso (Login) | 📊 Dashboard (Visão Geral) |
| :---: | :---: |
| ![Login](https://github.com/user-attachments/assets/9f0459a0-1570-44ee-bdf9-9b70fd6ec52b) | ![Dashboard](https://github.com/user-attachments/assets/fc6141ca-2107-4206-bedd-bcd4ce699707) |
| *Autenticação segura e direcionamento por perfil.* | *Gráficos de estoque e alertas de conformidade.* |

| 📦 Gestão de EPIs (Inventário) | 👥 Gestão de Colaboradores |
| :---: | :---: |
| ![Inventário](https://github.com/user-attachments/assets/0870c495-fdb0-4bd6-81dc-1445f373691b) | ![Colaboradores](https://github.com/user-attachments/assets/c8e1826e-8086-4213-b1f1-58eae8bdd486) |
| *Controle de CA, Estoque e Validades.* | *Perfis com foto e monitoramento de ASO.* |

| 📑 Registro de Entrega (Almoxarife) | 👤 Visão Restrita (Colaborador) |
| :---: | :---: |
| ![Entrega](https://github.com/user-attachments/assets/0f007200-ebc6-4175-a7d7-d864171df33a) | ![Colaborador](https://github.com/user-attachments/assets/93380a40-cceb-4f28-92f9-a25885495230) |
| *Fluxo de baixa e gestão de custódia.* | *Interface simplificada e bloqueio de menus.* |

| 📄 Geração de Ficha NR-6 (PDF) | ⚙️ Edição de Perfil e Foto |
| :---: | :---: |
| ![Ficha PDF](https://github.com/user-attachments/assets/97006d9c-ee71-4a0e-a3c3-4d8651c63e02) | ![Edição de Perfil](https://github.com/user-attachments/assets/d952ac92-acf2-4185-8f61-eaab058b8e0a) |
| *Documento gerado automaticamente para assinatura.* | *Área para personalização e upload de foto.* |

## 🛠️ Stack Tecnológica

O sistema foi desenvolvido utilizando tecnologias modernas do ecossistema Python/Django, priorizando performance, segurança jurídica e escalabilidade. A arquitetura foi dividida da seguinte forma:

| Camada | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| **Backend** | Python 3.12+ | Lógica de negócio e processamento principal do sistema |
| **Framework** | Django 6.0.3 | Estrutura MVC, ORM, rotas e sistema de autenticação |
| **Banco de Dados** | MySQL + PyMySQL 1.1.2 | Persistência relacional e integridade dos dados |
| **Frontend** | HTML5, CSS3, JavaScript | Estrutura semântica e interatividade do lado do cliente |
| **UI/UX** | Bootstrap 5.3 | Interface responsiva e padronização de componentes |
| **Ícones & Fontes** | Font Awesome 6, Bootstrap Icons, Google Fonts | Identidade visual e sinalização de ações |
| **Gráficos (BI)** | Chart.js | Renderização de dashboards dinâmicos para tomada de decisão |
| **PDF (Geração)** | `xhtml2pdf`, `reportlab` | Criação autônoma das fichas de EPI (NR-6) |
| **PDF (Manipulação)** | `pypdf`, `pyHanko` | Segurança, validação e manipulação de documentos |
| **Imagens** | `Pillow` | Processamento inteligente e otimização de fotos de perfil |

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.12 ou superior instalado.
* Serviço do MySQL Server rodando localmente.

### Passo a Passo

**1. Clone o repositório**
```bash
git clone [https://github.com/seu-usuario/epi-manager.git](https://github.com/seu-usuario/epi-manager.git)
cd epi-manager
```

**2. Crie e ative o ambiente virtual**
```bash
# No Windows:
python -m venv venv
venv\Scripts\activate

# No Linux/macOS:
python -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure o Banco de Dados**
Crie um banco de dados no seu MySQL. Em seguida, atualize o arquivo `settings.py` com as credenciais de acesso:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_seu_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
> **Nota:** O projeto utiliza o driver `PyMySQL`. A injeção de compatibilidade (`pymysql.install_as_MySQLdb()`) já está configurada no `__init__.py` principal da aplicação.

**5. Execute as migrações e crie o administrador**
```bash
python manage.py migrate
python manage.py createsuperuser
```

**6. Inicie o servidor**
```bash
python manage.py runserver
```
O sistema estará disponível no navegador através do endereço: `http://127.0.0.1:8000`

---

## 📂 Estrutura do Projeto

A arquitetura do projeto segue o padrão modular do Django, separando regras de negócio, interface e arquivos estáticos:

```text
epi_manager/
├── core/                  # Configurações centrais do Django (settings.py, urls.py)
├── apps/                  # Aplicações do sistema (EPIs, Colaboradores, Entregas)
│   ├── models.py          # Regras de negócio e estrutura das tabelas
│   ├── views.py           # Lógica de processamento e controle de requisições
│   └── forms.py           # Validação de dados
├── templates/             # Arquivos HTML da interface (Dashboard, Modais, Base)
├── static/                # Arquivos estáticos (CSS customizado, JS, Chart.js)
├── media/                 # Uploads dinâmicos (ex: fotos de perfil dos colaboradores)
├── requirements.txt       # Lista de dependências do Python
└── manage.py              # Utilitário de linha de comando do Django
```

---

## 🔗 Rotas Principais (Endpoints)

O sistema possui mapeamento de rotas focado na gestão e emissão de relatórios:

* `/dashboard/` - Painel principal com gráficos de BI e alertas de vencimentos (CA e ASO).
* `/epis/` - CRUD de equipamentos e controle de estoque técnico.
* `/colaboradores/` - Gestão de funcionários, perfis de acesso e histórico de saúde.
* `/entregas/` - Registro de movimentações e fluxo de baixas inteligentes (Devolvido, Descartado, Extraviado).
* `/ficha-epi/<id_colaborador>/pdf/` - Geração sob demanda da Ficha NR-6 em formato PDF.

---

## 👨‍💻 Autor

Desenvolvido por **Pfeiffer**

* **LinkedIn:** [Adicione seu LinkedIn aqui](https://linkedin.com/in/seu-perfil)
* **GitHub:** [Adicione seu GitHub aqui](https://github.com/seu-usuario)

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
