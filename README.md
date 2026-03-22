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

## ✨ Funcionalidades

O sistema foi projetado para cobrir todo o ciclo de vida do EPI dentro de uma organização:

* **🔐 Sistema de Autenticação com Hierarquia (RBAC):**
    * **Administrador/SST:** Acesso total, gestão de usuários, inventário e relatórios analíticos.
    * **Almoxarife:** Foco operacional em entregas e baixas de estoque.
    * **Colaborador:** Interface restrita para consulta de sua própria ficha e histórico.
* **📊 Dashboard de Indicadores:** Visualização clara do status do estoque e alertas críticos de validade.
* **👥 Gestão de Colaboradores:** Cadastro detalhado com foto, setor e controle de vencimento de ASO (NR-7).
* **📦 Controle de Inventário:** Gestão de CA (Certificado de Aprovação), fabricante e parâmetros de vida útil.
* **📑 Registro de Movimentações:** Histórico completo de custódia, garantindo a rastreabilidade total.
* **📄 Emissão de Documentos:** Geração automática da ficha de EPI em PDF conforme a NR-6.

## 📸 Demonstração do Sistema

Abaixo, os diferentes níveis de acesso e funcionalidades principais:

| 🔐 Portal de Acesso (Login) | 📊 Dashboard (Visão Admin) |
| :---: | :---: |
| ![Login](LINK_DA_IMAGEM_LOGIN) | ![Dashboard](LINK_DA_IMAGEM_DASHBOARD) |
| *Autenticação segura e direcionamento por perfil.* | *Gráficos de estoque e alertas de conformidade.* |

| 📦 Gestão de EPIs (Inventário) | 👥 Gestão de Colaboradores |
| :---: | :---: |
| ![Inventário](LINK_DA_IMAGEM_INVENTARIO) | ![Colaboradores](LINK_DA_IMAGEM_COLABORADORES) |
| *Controle de CA, Estoque e Validades.* | *Perfis com foto e monitoramento de ASO.* |

| 📑 Registro de Entrega (Almoxarife) | 👤 Visão Restrita (Colaborador) |
| :---: | :---: |
| ![Entrega](LINK_DA_IMAGEM_ENTREGA) | ![Colaborador](LINK_DA_IMAGEM_COLABORADOR) |
| *Fluxo de baixa e geração de ficha digital.* | *Interface simplificada e bloqueio de menus.* |

| 📄 Geração de Ficha NR-6 (PDF) |
| :---: |
| ![Ficha PDF](LINK_DA_IMAGEM_PDF) |
| *Documento gerado automaticamente para assinatura.* |

## 🛠️ Como Rodar o Projeto

### 1. Clonar o Repositório
```bash
git clone [https://github.com/Pfeifferr/epi-management-system.git](https://github.com/Pfeifferr/epi-management-system.git)
cd epi-management-system
