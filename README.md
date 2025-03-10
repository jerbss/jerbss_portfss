# 🚀 Portfólio de Jerbesson Silva

Eita, pois não é que você achou meu repositório!? Seja bem-vindo(a) ao meu cantinho digital. Aqui é onde mostro um pouco do que faço, projetos que já criei e as tecnologias que uso no meu dia a dia. Se você tá curioso(a) pra saber mais ou só quer dar uma espiadinha, chegou no lugar certo, viu?!

## 💻 Que diaxo é isso aqui?

Este projeto é meu portfólio pessoal desenvolvido com Django. É basicamente um espaço onde mostro meus projetos, habilidades e um pouquinho sobre minha pessoa. Tudo isso com um visual arretado!

### ✨ O que você vai encontrar por aqui:

- 🏠 **Página inicial** com uma apresentação descontraída sobre mim
- 🗂️ **Lista de projetos** filtrável por tags, status e tipo
- 🔍 **Detalhes dos projetos** com descrições completas e links
- 🌙 **Modo escuro** porque ninguém merece queimar a retina, né?
- 📱 **Design responsivo** que funciona até no celular da sua vovó

## 🔧 Tecnologias Usadas

- Django (Backend)
- Bootstrap (Frontend)
- JavaScript (Interatividade)
- Cloudinary (Armazenamento de imagens)
- PostgreSQL (Banco de dados)

## 💡 Por que criei esse portfólio?

Rapaz, eu sou daqueles que acredita que uma imagem vale mais que mil palavras. Mas um portfólio interativo vale umas 10 mil, no mínimo! 

A ideia aqui é simples: mostrar meus projetos de um jeito organizado e bonito, que qualquer pessoa consiga navegar sem estresse. Queria uma plataforma onde eu pudesse:

- Exibir meus trabalhos com uma cara profissional, mas sem perder o bom humor
- Categorizar tudo direitinho pra facilitar a navegação
- Mostrar tanto o resultado final quanto os bastidores dos projetos
- Ter um espaço pra contar um pouco da minha história e habilidades

Ah, e claro, eu queria fazer isso tudo do meu jeito, sem depender de plataformas prontas. Porque programador que é programador gosta mesmo é de complicar... ops, de personalizar tudo! 😂

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

- 📧 [Mande um e-mail](mailto:seuemail@example.com)
- 🔗 [LinkedIn](https://linkedin.com/in/seulinkedin)
- 🐙 [GitHub](https://github.com/seugithub)

---

Feito com 💙 e muita cafeína por Jerbesson Silva
