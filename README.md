# Portfólio de Jerbesson Silva

Eita, mah! Bem-vindo(a) ao repositório do meu portfólio. Aqui é onde eu mostro um pouco do que faço, dos projetos que já criei e das tecnologias que uso no dia a dia. Se você tá curioso(a) pra saber mais ou só quer dar uma olhada no que eu ando aprontando, chegou no lugar certo, man!

## O que tem aqui?

Esse portfólio foi feito com Django, um framework top em Python, e tá cheio de funcionalidades pra você explorar. Vou te contar rapidinho o que você vai encontrar:

- **Projetos**: Uma lista dos meus trabalhos, com título, descrição, status e até tags que eu usei.
- **Detalhes dos Projetos**: Clicou? Vai ver tudo sobre ele: imagens, links, conteúdo organizado e até projetos parecidos.
- **Filtros**: Quer ver só projetos de web ou os que ainda tão rolando? É só escolher as tags ou status.
- **Modo Claro/Escuro**: Escolhe o tema que combina com seu clima. E relaxa, ele lembra sua preferência!
- **Painel de Admin**: Se você for superusuário (tipo eu), pode criar, editar ou apagar projetos. É tipo ter poderes especiais.

## Tecnologias que eu usei

Pra fazer isso tudo virar realidade, juntei umas ferramentas maneiras:

### Front-end:
- HTML5, CSS3, JavaScript (o combo clássico)
- Bootstrap 5 (pra deixar tudo bonito em qualquer tela)
- TinyMCE (pra editar texto com superpoderes)
- Font Awesome (ícones que dão um tchan)

### Back-end:
- Django 5.1.6 (o cérebro do projeto)
- SQLite3 (banco de dados simples pra desenvolvimento)
- Django Cleanup (pra não deixar bagunça de arquivo)

### Extras:
- Pillow (pra lidar com imagens)
- Bleach (pra deixar o HTML seguro)
- Django JS Asset (pra organizar os scripts)

## O que você vai ver por aqui?

### Página Inicial
Uma foto minha, uma descrição rápida do que faço e uns botões pra você explorar meus projetos ou mandar um "E aí?". Tudo direto, sem firula.

### Lista de Projetos
Todos os projetos que já fiz, cada um com capa, título, descrição curta e tags. Os favoritos têm uma estrelinha pra você notar!

### Detalhes do Projeto
Clicou em um? Vai ver tudo: conteúdo formatado, links, projetos relacionados e até como foi feito. Ah, e tudo organizado com TinyMCE, então tá facinho de ler.

### Painel de Admin
Modo cheat ativado! Aqui eu crio, edito ou apago projetos, gerencio tags e contatos. Só pra quem tem acesso, claro.

### Responsividade
Funciona em qualquer tela: celular, tablet, PC... Até no seu videogame se você quiser (brincadeira, mas quase).

## 2. Requisitos

### 2.1 Requisitos Funcionais Geral (Usuários Não-Autenticados e Administradores)

| ID         | REQUISITOS GERAIS                                                                                                                                                                                      | STATUS          |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| RF-GER001  | Garantir que o site seja exibido corretamente em dispositivos móveis, tablets e desktops, com layout adaptável.                                                                                        | ✅ Implementado |
| RF-GER002  | Permitir que o usuário alterne entre os temas claro e escuro, com persistência da escolha.                                                                                                              | ✅ Implementado |
| RF-GER003  | Exibir uma lista de projetos com informações básicas (título, status, tags, etc.).                                                                                                                      | ✅ Implementado |
| RF-GER004  | Permitir filtrar a lista de projetos por tags, facilitando a busca por categorias específicas.                                                                                                          | ✅ Implementado |
| RF-GER005  | Permitir filtrar a lista de projetos por status (ex.: concluído, em andamento).                                                                                                                         | ✅ Implementado |
| RF-GER006  | Oferecer um botão para limpar todos os filtros aplicados e retornar à lista completa de projetos.                                                                                                       | ✅ Implementado |
| RF-GER007  | Exibir cards de projetos com metadados (título, status, tags, datas, etc.) de forma clara e organizada.                                                                                                 | ✅ Implementado |
| RF-GER008  | Permitir que o usuário visualize detalhes completos de um projeto ao clicar em um card.                                                                                                                 | ✅ Implementado |
| RF-GER009  | Disponibilizar links relacionados a cada projeto (ex.: repositório GitHub, Drive, YouTube, Site em Deploy, etc.).                                                                                       | ✅ Implementado |
| RF-GER010  | Incluir um botão flutuante para retornar ao topo da página, melhorando a navegabilidade.                                                                                                                | ✅ Implementado |
| RF-GER011  | Exibir um "caminho" ou "camadas de acesso" na página de detalhes do projeto, indicando a localização atual no site.                                                                                     | ✅ Implementado |
| RF-GER012  | Permitir que o usuário envie um e-mail para contato diretamente pelo site, usando um formulário simples.                                                                                                | ✅ Implementado |
| RF-GER013  | Exibir links para redes sociais em um menu suspenso.                                                                                                                                                    | ✅ Implementado |
| RF-GER014  | Garantir que todos os textos sejam legíveis em ambos os temas (claro e escuro), com contraste adequado.                                                                                                 | ⚠️ Parcialmente |
| RF-GER015  | Aplicar um efeito de "vidro" (glassmorphism) na barra de navegação para um visual moderno.                                                                                                              | ✅ Implementado |
| RF-GER016  | Permitir a exclusão de tags que não estão mais em uso no sistema, mantendo a base de dados organizada.                                                                                                   | ⏳ Não Iniciado |
| RF-GER017  | Permitir a ordenação da lista de projetos por data de criação, data de conclusão ou título.                                                                                                             | ⏳ Não Iniciado |
| RF-GER018  | Exibir um indicador visual (ex.: ícone ou badge) nos Cards de Projetos para destacar o status.                                                                                                          | ⏳ Não Iniciado |
| RF-GER019  | Exibir um contador de projetos na lista.                                                                                                                                                                | ⏳ Não Iniciado |

### 2.2 Requisitos Funcionais para Administradores

| ID         | REQUISITOS ADMINISTRADORES                                                                                                                                                     | STATUS          |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| RF-ADM001  | Permitir a criação de novos projetos, com campos para capa, título, descrição, tags, status, datas, conteúdo principal e links.                                                | ✅ Implementado |
| RF-ADM002  | Integrar o editor tinyMCE para facilitar a formatação de textos nos conteúdos dos projetos (ex.: negrito, listas, links).                                                      | ✅ Implementado |
| RF-ADM003  | Permitir o upload de imagens para serem usadas como capa dos projetos.                                                                                                         | ✅ Implementado |
| RF-ADM004  | Garantir que o tema do editor tinyMCE mude automaticamente ao alternar entre os temas claro e escuro do sistema.                                                                | ✅ Implementado |
| RF-ADM005  | Permitir a edição de projetos já criados, com atualização em tempo real dos dados.                                                                                             | ✅ Implementado |
| RF-ADM006  | Permitir a exclusão de projetos, com confirmação do usuário antes da remoção definitiva.                                                                                       | ✅ Implementado |
| RF-ADM007  | Exibir uma tela de confirmação antes da exclusão de um projeto, para evitar remoções acidentais.                                                                               | ✅ Implementado |
| RF-ADM008  | Implementar um sistema de pré-visualização de projetos antes de publicá-los.                                                                                                   | ⏳ Não Iniciado |

## Quer ajudar? Bora!

Se curtiu o projeto e quer botar a mão na massa, fique à vontade:

- Melhorar a interface: Deixar mais bonito ou intuitivo? Manda ver!
- Corrigir bugs: Achou algo errado? Me avisa que a gente arruma.
- Novas funcionalidades: Tem uma ideia? Vamo conversar!
- Otimizar: Se souber como deixar mais rápido, é só mandar.

## Licença

Esse projeto tá sob a licença MIT. Quer saber mais? Dá uma olhada no LICENSE.

## Contato

Quer trocar uma ideia, dar um feedback ou falar de um projeto? Me chama em qualquer rede:

- LinkedIn: [Jerbesson Silva](https://linkedin.com/in/jerbesson-silva)
- GitHub: [@jerbss](https://github.com/jerbss)
- Email: [Seu email aqui]

É isso, man! Espero que curta o portfólio. Qualquer coisa, é só me chamar. Vamo codar junto! 🚀

(Ah, e se passar pelo Benfica, me avisa que a gente toma um caldo de cana!) 😉
