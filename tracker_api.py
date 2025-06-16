import aiohttp
from config import TRN_API_KEY, RIOT_IDS_PRINCIPAIS

API_URL = "https://public-api.tracker.gg/v2/valorant/standard/profile/riot/{}/matches"
HEADERS = {"TRN-Api-Key": TRN_API_KEY}

# Busca partidas Premier de um Riot ID no período informado
async def buscar_partidas_premier(riot_id, start_date, end_date):
    riot_id_url = riot_id.replace("#", "%23").replace(" ", "%20")
    url = API_URL.format(riot_id_url)
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "limit": 50
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as resp:
            print(f"Buscando partidas para {riot_id} | Status: {resp.status}")
            try:
                data = await resp.json()
            except Exception as e:
                print(f"Erro ao decodificar resposta da API para {riot_id}: {e}")
                return []
            # Mostra o retorno para depuração
            print(f"Retorno da API para {riot_id}: {data}")
            if resp.status == 200:
                todas_partidas = data.get("data", {}).get("matches", [])
                partidas_premier = []
                # Filtra apenas partidas Premier
                for partida in todas_partidas:
                    modo = (
                        partida.get("metadata", {}).get("playlistName") or
                        partida.get("metadata", {}).get("modeName") or
                        partida.get("metadata", {}).get("mode") or
                        partida.get("metadata", {}).get("playlist") or
                        ""
                    )
                    if "premier" in modo.lower():
                        partidas_premier.append(partida)
                return partidas_premier
            else:
                return []

# Busca partidas Premier de todos os Riot IDs principais
async def buscar_todas_partidas(start_date, end_date):
    todas_partidas = []
    for riot_id in RIOT_IDS_PRINCIPAIS:
        partidas = await buscar_partidas_premier(riot_id, start_date, end_date)
        todas_partidas.extend(partidas)
    return todas_partidas

# Soma os stats dos teammates do time principal, evitando duplicidade
def somar_stats_teammates(partidas, partidas_processadas):
    stats = {}
    ids_processados = set(partidas_processadas)
    for partida in partidas:
        match_id = partida.get("id")
        if match_id in ids_processados:
            continue  # Ignora partidas já processadas
        ids_processados.add(match_id)
        # Procura o time do(s) riot_id principal
        your_team = None
        for team in partida.get("teams", []):
            for player in team.get("players", []):
                riot_id = f"{player.get('name', '')}#{player.get('tag', '')}"
                if riot_id.lower() in [id.lower() for id in RIOT_IDS_PRINCIPAIS]:
                    your_team = team
                    break
            if your_team:
                break
        if not your_team:
            continue
        for player in your_team.get("players", []):
            riot_id = f"{player.get('name', '')}#{player.get('tag', '')}"
            if riot_id not in stats:
                stats[riot_id] = {
                    "kills": 0, "deaths": 0, "assists": 0, "fb": 0, "fd": 0, "wins": 0, "losses": 0
                }
            stats[riot_id]["kills"] += player.get("stats", {}).get("kills", 0)
            stats[riot_id]["deaths"] += player.get("stats", {}).get("deaths", 0)
            stats[riot_id]["assists"] += player.get("stats", {}).get("assists", 0)
            stats[riot_id]["fb"] += player.get("stats", {}).get("firstBloods", 0)
            stats[riot_id]["fd"] += player.get("stats", {}).get("firstDeaths", 0)
            resultado = partida.get("outcome", "").lower()
            if resultado == "win":
                stats[riot_id]["wins"] += 1
            elif resultado == "loss":
                stats[riot_id]["losses"] += 1
    return stats, list(ids_processados)