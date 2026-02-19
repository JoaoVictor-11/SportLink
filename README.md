# ⚽ SportLink

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap&logoColor=white)

> **SportLink** é uma plataforma web fullstack desenvolvida para conectar entusiastas de esportes, facilitando a organização de partidas amadoras e a formação de times locais.

---

## 📖 Sobre o Projeto

Este projeto foi desenvolvido como parte do portfólio acadêmico de Ciência da Computação. O objetivo principal foi criar uma aplicação robusta utilizando a arquitetura **MVC (Model-View-Controller)**, focando em boas práticas de desenvolvimento web, segurança de dados e experiência do usuário (UX).

A aplicação resolve o problema de encontrar parceiros para esportes coletivos (Futebol, Vôlei, Basquete) através de um sistema de grupos geolocalizados.

---

## 📸 Screenshots

| Landing Page (Capa) | Feed de Grupos |
|:---:|:---:|
| ![Landing Page](https://via.placeholder.com/600x300/1e3c72/ffffff?text=Landing+Page+SportLink) | ![Feed](https://via.placeholder.com/600x300/27ae60/ffffff?text=Feed+de+Grupos) |

| Perfil do Usuário | Criação de Grupo |
|:---:|:---:|
| ![Perfil](https://via.placeholder.com/600x300/e67e22/ffffff?text=Perfil+e+Upload) | ![Criar Grupo](https://via.placeholder.com/600x300/8e44ad/ffffff?text=Formulario+de+Grupo) |

> *Nota: As imagens acima são ilustrativas. O projeto está em constante evolução visual.*

---

## 🛠️ Tecnologias Utilizadas

### Backend (Python)
- **Flask**: Micro-framework para roteamento e lógica de servidor.
- **SQLAlchemy (ORM)**: Abstração do banco de dados, eliminando SQL puro e aumentando a segurança.
- **Werkzeug Security**: Implementação de hash (SHA-256) para armazenamento seguro de senhas.
- **OS & Secure Filename**: Manipulação segura de arquivos para upload de imagens.

### Frontend
- **Jinja2**: Template engine para renderização dinâmica de HTML.
- **Bootstrap 5**: Framework CSS para layout responsivo (Mobile-First) e componentes de UI.
- **Bootstrap Icons**: Biblioteca de ícones vetoriais.

### Banco de Dados
- **SQLite**: Banco de dados relacional leve e serverless.
- **Modelagem**:
  - Relacionamento **1:N** (Um usuário cria vários grupos).
  - Relacionamento **N:N** (Muitos usuários participam de muitos grupos - Tabela de Associação).

---

## ✨ Funcionalidades Principais

1.  **Autenticação Completa:**
    *   Cadastro e Login seguros.
    *   Gestão de Sessão (Cookies server-side).
    *   Proteção de rotas (Decorators para impedir acesso não autorizado).

2.  **Gestão de Grupos (CRUD):**
    *   Criação de novos grupos com Esporte, Local e Horário.
    *   Visualização de grupos disponíveis no Feed.

3.  **Sistema de Inscrição Inteligente:**
    *   Botão dinâmico "Entrar/Sair".
    *   Validação para impedir duplicidade de inscrição.

4.  **Perfil do Usuário:**
    *   Edição de dados cadastrais.
    *   **Upload de Foto de Perfil** com salvamento em disco e referência no banco.
    *   Visualização da foto na Navbar e no Perfil.

---

## 🚀 Como rodar o projeto localmente

Pré-requisitos: Python 3.x instalado.

### 1. Clone o repositório
```bash
git clone https://github.com/JoaoVictor-11/SportLink.git
cd SportLink
```
### 2. Crie um Ambiente Virtual (Recomendado)
```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
```
### 3. Instale as dependências
```bash
    pip install -r requirements.txt
```
### 4. Execute a aplicação
```bash
    python app_web.pyO 
    servidor iniciará em http://127.0.0.1:5000. O banco de dados será criado automaticamente na primeira execução.
```
📂 Estrutura de Arquivos

    SportLink/
    ├── instance/            # Banco de dados SQLite (gerado automaticamente)
    ├── static/              # Arquivos Estáticos
    │   └── fotos/           # Uploads de fotos de perfil dos usuários
    ├── templates/           # Arquivos HTML (Frontend)
    │   ├── landing.html     # Capa do site
    │   ├── feed.html        # Lista de grupos
    │   ├── login.html       # Tela de login
    │   ├── cadastro.html    # Tela de registro
    │   ├── perfil.html      # Edição de perfil
    │   └── criar_grupo.html # Formulário de novo grupo
    ├── app_web.py           # Core da aplicação (Rotas e Models)
    ├── requirements.txt     # Lista de bibliotecas
    └── README.md            # Documentação

🔮 Roadmap (Próximos Passos)
 Adicionar filtro de busca por esporte no Feed.
 Implementar chat em tempo real para cada grupo.
 Integração com Google Maps API para localização das quadras.
 Sistema de recuperação de senha por e-mail.