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

Abaixo, os diferentes níveis de acesso e funcionalidades principais:

| 🔐 Portal de Acesso (Login) | 📊 Dashboard (Visão Admin) |
| :---: | :---: |
| ![Login]<img width="1901" height="902" alt="Image" src="https://github.com/user-attachments/assets/9f0459a0-1570-44ee-bdf9-9b70fd6ec52b" /> | ![Dashboard]<img width="1878" height="904" alt="Image" src="https://github.com/user-attachments/assets/fc6141ca-2107-4206-bedd-bcd4ce699707" /> |
| *Autenticação segura e direcionamento por perfil.* | *Gráficos de estoque e alertas de conformidade.* |

| 📦 Gestão de EPIs (Inventário) | 👥 Gestão de Colaboradores |
| :---: | :---: |
| ![Inventário](https://github.com/user-attachments/assets/0870c495-fdb0-4bd6-81dc-1445f373691b) | ![Colaboradores]<img width="1896" height="906" alt="Image" src="https://github.com/user-attachments/assets/153b3170-1a78-48d0-a651-a1cab500d3eb" /> |
| *Controle de CA, Estoque e Validades.* | *Perfis com foto e monitoramento de ASO.* |

| 📑 Registro de Entrega (Almoxarife) | 👤 Visão Restrita (Colaborador) |
| :---: | :---: |
| ![Entrega](LINK_DA_IMAGEM_ENTREGA) | ![Colaborador](LINK_DA_IMAGEM_COLABORADOR) |
| *Fluxo de baixa e geração de ficha digital.* | *Interface simplificada e bloqueio de menus.* |

| 📄 Geração de Ficha NR-6 (PDF) | ⚙️ Edição de Perfil e Foto |
| :---: | :---: |
| ![Ficha PDF](LINK_DA_IMAGEM_PDF) | ![Edição de Perfil](LINK_DA_IMAGEM_PERFIL) |
| *Documento gerado automaticamente para assinatura.* | *Área para personalização e upload de foto.* |

## 🛠️ Como Rodar o Projeto

### 1. Clonar o Repositório
```bash
git clone [https://github.com/Pfeifferr/epi-management-system.git](https://github.com/Pfeifferr/epi-management-system.git)
cd epi-management-system
