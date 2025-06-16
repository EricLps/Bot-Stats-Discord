# 🤖 Bot de Estatísticas Premier para Discord
## 📌 Descrição

Bot para Discord que coleta estatísticas de partidas Premier do Valorant via Tracker.gg e envia relatórios automáticos semanais para um canal do servidor.
Inclui kills, assists, deaths, first bloods (FB), first deaths (FD), e histórico de vitórias e derrotas.
O bot pode ser acionado manualmente por comando ou automaticamente toda segunda às 09h.

--- 

## 📁 Estrutura de Pastas

Bot-Discord/
├── bot.py             → Código principal do bot
├── tracker_api.py     → Funções para acessar e tratar dados da Tracker.gg
├── config.py          → Token do Discord, API Key, IDs e configurações
├── requirements.txt   → Lista de dependências Python
├── data/
│   └── stats.json     → Histórico de partidas já processadas

## ⚙️ Requisitos

✅ Python 3.8 ou superior
✅ Conta no Discord com permissão para criar bots
✅ API Key da Tracker.gg: https://tracker.gg/developers
✅ Permissões no servidor Discord para adicionar e configurar bots

--- 

### 🧩 Instalação

## 1️⃣ Clone o repositório:

git clone <url-do-repositorio>
cd Bot-Discord

## 2️⃣ (Opcional) Crie e ative um ambiente virtual:

    Windows:

python -m venv venv
venv\Scripts\activate

    Linux / macOS:

python3 -m venv venv
source venv/bin/activate

## 3️⃣ Instale as dependências:

pip install -r requirements.txt

--- 

### 🛠️ Configuração

## 1️⃣ Crie o arquivo config.py na raiz do projeto com o conteúdo abaixo:

DISCORD_TOKEN = 'seu_token_do_bot'
TRACKER_API_KEY = 'sua_api_key_da_tracker'
CANAL_ID = 123456789012345678  # Substitua pelo ID do canal do Discord
RIOT_IDS_PRINCIPAIS = [
    'Jogador1#TAG',
    'Jogador2#TAG',
    'Jogador3#TAG'
]
NOME_DA_EQUIPE = "Nome da Equipe"

## 2️⃣ Crie a pasta data/, se ela ainda não existir:

mkdir data

## 3️⃣ ⚠️ Segurança
Adicione os arquivos sensíveis ao seu .gitignore:

config.py
data/
venv/
__pycache__/

## ▶️ Como Rodar

Execute o bot com:

python bot.py

O bot ficará online e começará a monitorar os jogadores e agendar o envio automático de relatórios.
# 💬 Comandos Disponíveis

    !stats → Envia manualmente o relatório das partidas Premier jogadas nos últimos 6 dias.

## ⏰ Funcionamento Automático

    🕚 Horário: Toda Segunda às 09:00 da manhã

    🧠 O bot busca partidas Premier jogadas nos últimos 6 dias

    📤 Envia um resumo semanal automaticamente para o canal configurado

    🗃️ Salva as partidas processadas no arquivo data/stats.json para evitar duplicatas

## 🔍 Como Funciona

    Acessa a API da Tracker.gg para cada jogador listado no config.py

    Filtra apenas as partidas do modo Premier

    Coleta os seguintes dados por jogador:

        🔫 Kills

        💀 Deaths

        🧠 Assists

        🩸 First Bloods (FB)

        ☠️ First Deaths (FD)

    Conta as 🟩 vitórias e 🟥 derrotas por time

    Gera um relatório visual em formato de embed no Discord

## 📊 Exemplo de Relatório no Discord

📊 Estatísticas Semanais – Equipe Alpha
🗓️ Semana: 09/06 a 15/06

Jogador1#Tag
Kills: 54 | Deaths: 34 | Assists: 12 | FB: 6 | FD: 4

Jogador2#Tag
Kills: 48 | Deaths: 30 | Assists: 15 | FB: 5 | FD: 3

✅ Vitórias: 2
❌ Derrotas: 1
✏️ Personalização

    ➕ Adicionar/remover jogadores: edite a lista RIOT_IDS_PRINCIPAIS no config.py

    🕒 Alterar o horário de envio automático: edite o agendamento no bot.py

    🏷️ Alterar o nome da equipe: edite NOME_DA_EQUIPE no config.py

    📺 Alterar o canal de envio: modifique CANAL_ID no config.py

---

### ☁️ Dicas de Deploy

## 💻 Linux:

    Utilize screen, tmux ou crie um serviço com systemd para manter o bot ativo 24/7

## 🪟 Windows:

    Use o NSSM (Non-Sucking Service Manager) para rodar o bot como serviço em segundo plano

### 🚨 Problemas Comuns

## ❌ Erro 401 na API da Tracker.gg
→ Verifique se a chave da API está correta e sem espaços extras.

## 🤖 Bot não responde no Discord
→ Certifique-se de que está online, com o token correto e com permissões no servidor.

## 📉 Partidas Premier não aparecem
→ A Tracker.gg pode demorar para atualizar os dados. Verifique se as partidas foram públicas e realmente Premier.
🧾 Licença

## 👨‍💻 Autor
Desenvolvido por [Eric Lopes]
