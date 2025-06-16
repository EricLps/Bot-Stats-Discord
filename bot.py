import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
from datetime import datetime, timedelta
from config import DISCORD_TOKEN, CANAL_ID
from tracker_api import buscar_todas_partidas, somar_stats_teammates

intents = discord.Intents.default()
intents.message_content = True  # Permite ler o conteúdo das mensagens
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

STATS_PATH = "data/stats.json"

# Carrega stats salvos em disco
def carregar_stats():
    try:
        with open(STATS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Salva stats em disco
def salvar_stats(stats):
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

# Faz a coleta e envia stats se houver partidas novas
async def coletar_e_enviar_stats():
    stats_geral = carregar_stats()
    hoje = datetime.now()
    data_inicio = (hoje - timedelta(days=6)).strftime("%Y-%m-%d")
    data_fim = hoje.strftime("%Y-%m-%d")

    partidas_processadas = stats_geral.get("ids_processados", [])

    # Busca todas as partidas Premier dos Riot IDs principais
    partidas = await buscar_todas_partidas(data_inicio, data_fim)
    stats_semana, ids_processados = somar_stats_teammates(partidas, partidas_processadas)

    canal = bot.get_channel(CANAL_ID)
    # Só envia se houver pelo menos uma partida nova
    if not stats_semana:
        if canal:
            await canal.send("Nenhuma partida Premier encontrada nos últimos 6 dias.")
        return

    # Atualiza stats acumulados
    for riot_id, stats in stats_semana.items():
        if riot_id not in stats_geral:
            stats_geral[riot_id] = {
                "kills": 0, "deaths": 0, "assists": 0, "fb": 0, "fd": 0, "wins": 0, "losses": 0
            }
        for key in ["kills", "deaths", "assists", "fb", "fd", "wins", "losses"]:
            stats_geral[riot_id][key] += stats[key]

    stats_geral["ids_processados"] = ids_processados

    # Monta o embed com os dados
    embed = discord.Embed(
        title="📊 Estatísticas Premier – Últimos 6 dias",
        description=f"🗓️ Período: {data_inicio} a {data_fim}",
        color=0x00ff99
    )

    total_wins = sum(stats["wins"] for stats in stats_semana.values())
    total_losses = sum(stats["losses"] for stats in stats_semana.values())

    for riot_id, stats in stats_semana.items():
        embed.add_field(
            name=f"**{riot_id}**",
            value=f"Kills: {stats_geral[riot_id]['kills']} | Deaths: {stats_geral[riot_id]['deaths']} | Assists: {stats_geral[riot_id]['assists']} | FB: {stats_geral[riot_id]['fb']} | FD: {stats_geral[riot_id]['fd']}",
            inline=False
        )

    embed.add_field(name="✅ Vitórias", value=str(total_wins))
    embed.add_field(name="❌ Derrotas", value=str(total_losses))
    embed.set_footer(text="Próximo envio automático: segunda-feira às 09h.")

    if canal:
        await canal.send(embed=embed)
    salvar_stats(stats_geral)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    # Agendamento para toda segunda-feira às 09h00
    scheduler.add_job(coletar_e_enviar_stats, "cron", day_of_week="mon", hour=9, minute=0)
    scheduler.start()

# Comando manual para testar o envio a qualquer momento
@bot.command()
async def stats(ctx):
    """Envia as estatísticas dos últimos 6 dias manualmente."""
    await coletar_e_enviar_stats()
    await ctx.send("Estatísticas enviadas!")

if __name__ == "__main__":
    print("Iniciando o bot...")
    bot.run(DISCORD_TOKEN)