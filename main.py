import requests
from fake_useragent import UserAgent
import telebot
import time
import asyncio
from datetime import datetime

ua = UserAgent()


bot_token = '6297773878:AAHf-dwqVUjTlN4R8PN3wYELhDaUeGVC-a8'
chat_id = "-1001849167994"

bot = telebot.TeleBot(token=bot_token)

async def send_live_scores():
    headers = {'Accept': 'application/json', 'Origin': 'https://www.playscores.com', 'User-Agent': ua.random}
    
    url = f'https://playscores.sportsat.app/gateway/api/v1/fixtures-svc/v2/fixtures/livescores?include=weatherReport,additionalInfo,league,stats,pressureStats,probabilities&take=3000'
    sent_matches = {}
    while True:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            message = f"Erro ao acessar a API: {response.status_code}"
            bot.send_message(chat_id=chat_id, text=message)
        else:
            data = response.json()
            for match in data['data']:
                chance = match.get('probabilities', {}).get('over_0_5')                                             
                match_stats = match.get('stats')
                if match_stats is not None:
                    h_attk = match_stats.get('attacks', {}).get('home', 0)   
                    a_attk = match_stats.get('attacks', {}).get('away', 0)
                    dh_attk = match_stats.get('dangerousAttacks', {}).get('home', 0)
                    da_attk = match_stats.get('dangerousAttacks', {}).get('away', 0)
                    p_home = match_stats.get('possessiontime', {}).get('home', 0)
                    p_away = match_stats.get('possessiontime', {}).get('away', 0)
                    es_home = match_stats.get('corners', {}).get('home', 0)
                    es_away = match_stats.get('corners', {}).get('away', 0)
                    shotGol_h = match_stats.get('shotsOngoal', {}).get('home', 0)
                    shotGol_a = match_stats.get('shotsOngoal', {}).get('away', 0)
                    shotNo_h = match_stats.get('shotsOffgoal', {}).get('home', 0)
                    shotNo_a = match_stats.get('shotsOffgoal', {}).get('away', 0)
                    somaT = shotGol_h + shotNo_h if shotGol_h is not None and shotNo_h is not None else 0
                    somaH = shotGol_a + shotNo_a if shotGol_a is not None and shotNo_a is not None else 0
                    pressure_stats = match.get('pressureStats')
                    if pressure_stats is not None:
                        goal_home = pressure_stats.get('exg', {}).get('home')
                        goal_away = pressure_stats.get('exg', {}).get('away')     
                        mh1_home = pressure_stats.get('mh1', {}).get('home', 0)
                        mh1_away = pressure_stats.get('mh1', {}).get('away', 0)
                        mh2_home = pressure_stats.get('mh2', {}).get('home', 0)
                        mh2_away = pressure_stats.get('mh2', {}).get('away', 0)
                        mh3_home = pressure_stats.get('mh3', {}).get('home', 0)
                        mh3_away = pressure_stats.get('mh3', {}).get('away', 0)
                        appm1_home = pressure_stats.get('appm1', {}).get('home', 0)
                        appm1_away = pressure_stats.get('appm1', {}).get('away', 0)
                        appm2_home = pressure_stats.get('appm2', {}).get('home', 0)
                        appm2_away = pressure_stats.get('appm2', {}).get('away', 0)
                  
                    tempo = match.get('currentTime', {}).get('minute')
                    scores_h = match.get('scores', {}).get('homeTeamScore')
                    scores_a = match.get('scores', {}).get('awayTeamScore')
                    home = match.get('homeTeam', {}).get('name', {})
                    espc = home.replace(" ","%20")
                    away = match.get('awayTeam', {}).get('name', {})
                    tempo = match.get('currentTime', {}).get('minute')
                    link = f"https://www.bet365.com/#/AX/K^{espc}"

                # Verificar se a partida já foi enviada
                match_id = f"{home} - {away}"
                if match_id in sent_matches:
                    if scores_h > sent_matches[match_id]['scores_h'] or scores_a > sent_matches[match_id]['scores_a']:
                        # Houve um gol, então edite a mensagem original adicionando "GREEN"
                        if not sent_matches[match_id]['goal'] and tempo >= 18 and tempo <= 45:
                            
                            message = f"""
🤖Novo Jogo

{home} - {away}
⏰{tempo} minutos do 1° Tempo

📱<a href='{link}'><b>Link do jogo</b></a>

🤖Inteligencia Artificial DEZBET:
⭐️Mais de 0.5 no 1° tempo➜ {chance}%

📊 Eventos da Partida:
(Casa/Visitante)
--Ataques: {h_attk}/{a_attk}
--Ataques Perigosos: {dh_attk}/{da_attk}
--Posse de Bola: {p_home}/{p_away}
--Escanteios: {es_home}/{es_away}

🎯Chances de Gol:
(Casa/Fora)
--Chutes no Gol: {shotGol_h}/{shotGol_a}
--Chutes fora do Gol: {shotNo_h}/{shotNo_a}
--Chutes Total: {somaT}/{somaH}
--ExG: {goal_home}/{goal_away}
GREEN✅✅✅
"""
                            message_id = sent_matches[match_id]['message_id']
                            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message, parse_mode='html', disable_web_page_preview=True)
                            sent_matches[match_id]['goal'] = True
                else:
                    if scores_h == 0 and scores_a == 0 and h_attk is not None and a_attk is not None and h_attk >= 19 and a_attk >= 13 and tempo is not None and tempo >=16 and tempo <= 88 and mh1_home is not None and mh1_away is not None and mh1_home + mh1_away >= 31 and appm1_home is not None and appm1_away is not None and appm1_home >= 0.20 and appm1_away >= 0.15 and appm2_home is not None and appm2_away is not None and appm2_home >= 0.3 and appm2_away >= 0.2 and mh2_home is not None and mh2_away is not None and mh2_home + mh2_away >= 8 and mh3_home is not None and mh3_away is not None and mh3_home + mh3_away >= 4 and somaT is not None and somaH is not None and somaT + somaH / 2 >= 1 :
                        
                        message = f"""
🤖Novo Jogo

{home} - {away}
⏰{tempo} minutos do 1° Tempo

📱<a href='{link}'><b>Link do jogo</b></a>

🤖Inteligencia Artificial DEZ BET:
⭐️Mais de 0.5 no 1° tempo➜ {chance}%

📊 Eventos da Partida:
(Casa/Visitante)
--Ataques: {h_attk}/{a_attk}
--Ataques Perigosos: {dh_attk}/{da_attk}
--Posse de Bola: {p_home}/{p_away}
--Escanteios: {es_home}/{es_away}

🎯Chances de Gol:
(Casa/Fora)
--Chutes no Gol: {shotGol_h}/{shotGol_a}
--Chutes fora do Gol: {shotNo_h}/{shotNo_a}
--Chutes Total: {somaT}/{somaH}
--ExG: {goal_home}/{goal_away}
"""
                        msg = bot.send_message(chat_id=chat_id, text=message, parse_mode="html", disable_web_page_preview=True)
                        # Adicionar a partida enviada ao conjunto de partidas já enviadas
                        sent_matches[match_id] = {'message_id': msg.message_id, 'goal': False, 'scores_h': scores_h, 'scores_a': scores_a}
                  
        await asyncio.sleep(120)
                
if __name__ == '__main__':
    asyncio.run(send_live_scores())
