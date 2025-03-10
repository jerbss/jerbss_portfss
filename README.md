# 😎 Portfólio de Jerbesson Silva

**Eae, meu chapa!**<br>
Achou meu portfólio, hein? Seja bem-vindo ao meu cantinho digital. Aqui você encontra os projetos que eu ando criando, as tecnologias que eu curto mexer e um pouco sobre o que me interessa. Se veio só dar uma olhada ou tá curioso pra saber mais, fica à vontade!

## 💻 Que diaxo é isso aqui?!

Esse aqui é o meu portfólio pessoal feito com Django 🐍💪! É tipo minha vitrine digital: projetos, habilidades e quem é o carinha que fez tudo isso.

### ✨ O que você vai encontrar por aqui:

- 🏠 **Página inicial** com uma apresentação descontraída sobre mim
- 🗂️ **Lista de projetos** filtrável por tags, status e tipo
- 🔍 **Detalhes dos projetos** com descrições completas e links
- 🌙 **Modo escuro** porque ninguém merece queimar a retina, né?
- 📱 **Design responsivo** que funciona até no celular da sua vovó

## 🔧 Tecnologias Usadas

- Django (Backend)
- Bootstrap (Frontend)
- PostgreSQL (Banco de dados)
- JavaScript (Interatividade)
- Cloudinary (Armazenamento de imagens)
- TinyMCE (Edição de textos)


## 💭 Como surgiu essa doideira de portfólio?

Simples: um dia, me peguei pensando: "Onde estão todos os projetos e trabalhos que já fiz?" 🤔

Aí, a luz piscou e pensei: "Por que não criar o jerbssfolio?" Esse portfólio tem como missão mostrar meu trabalho de forma dinâmica, sem a chatice de ficar mexendo em código toda vez que eu quiser adicionar algo novo.

E aqui está, de forma simples e cheia de personalidade! 🔥

## 📋 Requisitos do Sistema

### 2.1 Requisitos Funcionais Geral (Usuários Não-Autenticados e Administradores)

|     ID    	|                                                  REQUISITOS GERAIS                                                  	|     STATUS     	|
|:---------:	|:-------------------------------------------------------------------------------------------------------------------:	|:--------------:	|
| RF-GER001 	|   Garantir que o site seja exibido corretamente em dispositivos móveis, tablets e desktops, com layout adaptável.   	| ✅ Implementado 	|
| RF-GER002 	|              Permitir que o usuário alterne entre os temas claro e escuro, com persistência da escolha.             	| ✅ Implementado 	|
| RF-GER003 	|                  Exibir uma lista de projetos com informações básicas (título, status, tags, etc.).                 	| ✅ Implementado 	|
| RF-GER004 	|            Permitir filtrar a lista de projetos por tags, facilitando a busca por categorias específicas.           	| ✅ Implementado 	|
| RF-GER005 	|                   Permitir filtrar a lista de projetos por status (ex.: concluído, em andamento).                   	| ✅ Implementado 	|
| RF-GER006 	|          Oferecer um botão para limpar todos os filtros aplicados e retornar à lista completa de projetos.          	| ✅ Implementado 	|
| RF-GER007 	|       Exibir cards de projetos com metadados (título, status, tags, datas, etc.) de forma clara e organizada.       	| ✅ Implementado 	|
| RF-GER008 	|               Permitir que o usuário visualize detalhes completos de um projeto ao clicar em um card.               	| ✅ Implementado 	|
| RF-GER009 	|  Disponibilizar links relacionados a cada projeto (ex.: repositório GitHub, Drive, YouTube, Site em Deploy, etc.).  	| ✅ Implementado 	|
| RF-GER010 	|               Incluir um botão flutuante para retornar ao topo da página, melhorando a navegabilidade.              	| ✅ Implementado 	|
| RF-GER011 	| Exibir um "caminho" ou "camadas de acesso" na página de detalhes do projeto, indicando a localização atual no site. 	| ✅ Implementado 	|
| RF-GER012 	|       Permitir que o usuário envie um e-mail para contato diretamente pelo site, usando um formulário simples.      	| ✅ Implementado 	|
| RF-GER013 	|                                 Exibir links para redes sociais em um menu suspenso.                                	| ✅ Implementado 	|
| RF-GER014 	|       Garantir que todos os textos sejam legíveis em ambos os temas (claro e escuro), com contraste adequado.       	| ⚠️ Parcialmente 	|
| RF-GER015 	|              Aplicar um efeito de "vidro" (glassmorphism) na barra de navegação para um visual moderno.             	| ✅ Implementado 	|
| RF-GER016 	|        Permitir a exclusão de tags que não estão mais em uso no sistema, mantendo a base de dados organizada.       	| ⏳ Não Iniciado 	|
| RF-GER017 	|             Permitir a ordenação da lista de projetos por data de criação, data de conclusão ou título.             	| ⏳ Não Iniciado 	|
| RF-GER018 	|            Exibir um indicador visual (ex.: ícone ou badge) nos Cards de Projetos para destacar o status.           	| ⏳ Não Iniciado 	|
| RF-GER019 	|                                       Exibir um contador de projetos na lista.                                      	| ⏳ Não Iniciado 	|

### 2.2 Requisitos Funcionais do Administrador

|     ID     	|                                                   REQUISITOS DO ADMINISTRADOR                                                  	|     STATUS     	|
|:----------:	|:----------------------------------------------------------------------------------------------------------------------------:	|:--------------:	|
| RF-ADM001  	|                    Implementar painel de administração para gerenciamento de projetos (CRUD completo).                        	| ✅ Implementado 	|
| RF-ADM002  	|             Permitir que o administrador adicione novos projetos, incluindo título, descrição, imagem de capa, etc.           	| ✅ Implementado 	|
| RF-ADM003  	|                         Permitir a edição de projetos existentes, incluindo todos os metadados.                              	| ✅ Implementado 	|
| RF-ADM004  	|                      Implementar exclusão segura de projetos, com confirmação para evitar exclusões acidentais.              	| ✅ Implementado 	|
| RF-ADM005  	| Permitir o upload, armazenamento e gerenciamento de imagens para os projetos, com redimensionamento automático quando necessário. | ✅ Implementado 	|
| RF-ADM006  	|                    Permitir a associação e gerenciamento de tags nos projetos para melhor organização.                       	| ✅ Implementado 	|
| RF-ADM007  	|                  Incluir um editor de texto rico (WYSIWYG) para formatação do conteúdo dos projetos.                        	| ✅ Implementado 	|
| RF-ADM008  	|            Oferecer uma previsualização (preview) do projeto durante a criação/edição, antes da publicação final.            	| ✅ Implementado 	|
| RF-ADM009  	|                  Garantir que o editor de conteúdo também se adapte ao tema atual (claro ou escuro).                        	| ✅ Implementado 	|
| RF-ADM010  	|               Permitir a definição do status do projeto (ex.: em andamento, concluído) durante a criação/edição.             	| ✅ Implementado 	|

## 👋 Vamos trocar ideia?

- 📧 [Mande um e-mail](mailto:jerbessonc@gmail.com)
- 🔗 [LinkedIn](https://www.linkedin.com/in/jerbs/)
- 🐙 [GitHub](https://github.com/jerbss)

---

Feito com 💙 e muita cafeína por Jerbesson Silva
