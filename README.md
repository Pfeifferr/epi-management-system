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

* **🔐 Sistema de Autenticação com Hierarquia:**
    * **Administrador/Gestor:** Acesso total ao sistema, gestão de usuários, inventário e relatórios.
    * **Operador de Estoque:** Permissão para realizar entregas e baixas, sem acesso às configurações sensíveis.
    * **Colaborador:** Acesso restrito para consulta de sua própria ficha de EPIs recebidos.
* **📊 Dashboard de Indicadores:** Visualização clara e em tempo real do status do estoque, EPIs mais retirados e alertas críticos.
* **👥 Gestão de Colaboradores:** Cadastro detalhado de funcionários, permitindo vincular fotos e organizar por setores/cargos.
* **📦 Controle de Inventário:** Gerenciamento de Equipamentos com registro de CA (Certificado de Aprovação), fabricante e data de validade.
* **📑 Registro de Movimentações:** Histórico completo de entregas e devoluções, garantindo a rastreabilidade de cada item.
* **📄 Emissão de Documentos:** Geração automática da ficha de entrega de EPI em conformidade com a NR-6 (Pronto para impressão).

## 📸 Demonstração do Sistema

Abaixo, apresento a interface principal do sistema, focada em usabilidade e eficiência operacional.

| 📊 Dashboard de Indicadores | 📦 Gestão de Inventário (EPIs) |
| :---: | :---: |
| ![Dashboard](LINK_DA_IMAGEM_DASHBOARD) | ![Inventário](LINK_DA_IMAGEM_INVENTARIO) |
| *Visão geral de estoque e alertas críticos.* | *Controle de CA, Fabricante e Validades.* |

| 👥 Cadastro de Colaboradores | 🔐 Login & Hierarquia |
| :---: | :---: |
| ![Colaboradores](LINK_DA_IMAGEM_COLABORADORES) | ![Login](LINK_DA_IMAGEM_LOGIN) |
| *Gestão de perfis com foto e setor.* | *Acesso seguro baseado em níveis de permissão.* |

| 📑 Geração de Ficha NR-6 (PDF) |
| :---: |
| ![Ficha PDF](LINK_DA_IMAGEM_PDF) |
| *Documento gerado automaticamente para conformidade legal.* |
