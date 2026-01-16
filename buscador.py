import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Por dentro do Sisema", page_icon="🌿")

st.title("Por dentro do Sisema 🌿")
st.markdown("### Período dos Destaques")

# --- FUNÇÕES AUXILIARES ---

def encurtar_link(url_longa):
    api_url = f"https://is.gd/create.php?format=simple&url={url_longa}"
    for tentativa in range(3):
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200 and "is.gd" in response.text:
                return response.text.strip()
        except:
            pass
        time.sleep(1)
    return url_longa

def obter_emoji_exclusivo(texto, emojis_ja_usados):
    """
    1. Identifica o tema.
    2. Tenta pegar um emoji daquele tema que ainda não foi usado.
    3. Se não tiver tema ou acabarem os do tema, pega um genérico não usado.
    """
    texto = texto.lower()
    pool_tematico = []
    
    # --- DEFINIÇÃO DOS GRUPOS DE EMOJIS ---
    
    # Água / Recursos Hídricos
    if any(x in texto for x in ["água", "hídric", "rio", "bacia", "chuva", "enchente", "nascente", "outorga", "pluvi", "saneamento"]):
        pool_tematico = ["💧", "🌊", "🌧️", "⛈️", "🚿", "⛲", "🧊", "🏞️", "☔"]
        
    # Fogo / Seca
    elif any(x in texto for x in ["fogo", "incêndio", "queimada", "calor", "seco", "previncêndio", "estiagem"]):
        pool_tematico = ["🔥", "🌡️", "🚒", "🌋", "🚬", "🎇", "🧨", "🥵"]
        
    # Fauna / Animais
    elif any(x in texto for x in ["fauna", "animal", "bicho", "gato", "cachorro", "resgate", "silvestre", "peixe", "cetas", "aves", "mamífero"]):
        pool_tematico = ["🐾", "🐆", "🐒", "🐟", "🦜", "🐍", "🐢", "🦅", "🦆", "🦚", "🐅", "🐸", "🐋"]
        
    # Flora / Floresta / Conservação
    elif any(x in texto for x in ["floresta", "mata", "parque", "unidade de conservação", "plantio", "árvore", "vegetação", "ief", "rppn"]):
        pool_tematico = ["🌳", "🌲", "🌿", "🌱", "🍃", "🌵", "🌴", "🪵", "🍄", "🌾"]
        
    # Resíduos / Lixo
    elif any(x in texto for x in ["lixo", "resíduo", "recicla", "coleta", "aterro", "limpeza", "catador", "logística reversa"]):
        pool_tematico = ["♻️", "🗑️", "🚯", "🚮", "🚛", "🧹", "🧴"]
        
    # Ar / Clima
    elif any(x in texto for x in ["ar", "poluição", "clima", "meteorologia", "atmosfera", "emissões", "tempo"]):
        pool_tematico = ["🌤️", "🌫️", "🌬️", "☁️", "⛈️", "🌪️", "🌡️", "😷"]
        
    # Barragens / Mineração
    elif any(x in texto for x in ["barragem", "mineração", "rejeito", "sigibar", "vale", "desastre"]):
        pool_tematico = ["🧱", "🏗️", "⛓️", "🛑", "🚧", "⛰️", "⛏️"]
        
    # Educação / Eventos
    elif any(x in texto for x in ["educação", "jovem", "escola", "curso", "capacitação", "ensino", "professor", "palestra", "seminário"]):
        pool_tematico = ["🎓", "📚", "🖊️", "🏫", "📝", "📢", "🗣️"]
        
    # Energia
    elif any(x in texto for x in ["solar", "energia", "fotovoltaica", "elétrica", "luz"]):
        pool_tematico = ["☀️", "⚡", "🔋", "💡", "🔌"]
        
    # Fiscalização / Leis
    elif any(x in texto for x in ["licenciamento", "fiscalização", "multa", "irregular", "apreensão", "operação", "polícia"]):
        pool_tematico = ["⚖️", "👮", "📝", "🚫", "🚓", "🚨", "🔨"]

    # --- LÓGICA DE SELEÇÃO ---
    
    # 1. Tenta selecionar do tema específico (sem repetir)
    candidatos_tematicos = [e for e in pool_tematico if e not in emojis_ja_usados]
    
    if candidatos_tematicos:
        escolhido = random.choice(candidatos_tematicos)
        emojis_ja_usados.append(escolhido)
        return escolhido

    # 2. Se não tem tema ou acabaram os do tema, vai para os GENÉRICOS (Natureza Geral)
    pool_genericos = [
        "🌍", "🌎", "🌏", "🗺️", "🏔️", "🏕️", "⛰️", "🌋", "🗻",
        "🌲", "🌳", "🌴", "🌵", "🌾", "🌿", "☘️", "🍀", "🍁", "🍂", "🍃",
        "🍄", "🐚", "🪨", "🪵", "🌻", "🌼", "🌷", "🌱", "🪴", "🌲",
        "🐝", "🪱", "🐛", "🦋", "🐌", "🐞", "🐜", "🦗", "🪳", "🦂", "🦟", "🪰",
        "🐢", "🐍", "🦎", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🦭",
        "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🦣", "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🦬", "🐃", "🐂", "🐄",
        "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🦮", "🐕‍🦺", "🐈", "🐈‍⬛", "🐓", "🦃", "🦚", "🦜", "🦢", "🦩", "🕊️", "🐇", "🦝", "🦨", "🦡", "🦦", "🦥", "🐁", "🐀", "🐿️", "🦔"
    ]
    
    candidatos_genericos = [e for e in pool_genericos if e not in emojis_ja_usados]
    
    if candidatos_genericos:
        escolhido = random.choice(candidatos_genericos)
        emojis_ja_usados.append(escolhido)
        return escolhido
        
    # 3. Se por um milagre acabarem TODOS os emojis do mundo, repete o genérico padrão
    return "🌿"

# --- ENTRADA DE DADOS ---
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data Início:", format="DD/MM/YYYY")
with col2:
    data_fim = st.date_input("Data Fim:", format="DD/MM/YYYY")

botao_buscar = st.button("🔍 Gerar Boletim Completo", type="primary")

# --- LÓGICA DE BUSCA ---
if botao_buscar:
    st.info("Gerando boletim... A inteligência artificial está escolhendo os melhores emojis.")
    
    # Lista para controlar repetições GLOBALMENTE
    emojis_usados_na_sessao = []

    start_date = datetime.combine(data_inicio, datetime.min.time())
    end_date = datetime.combine(data_fim, datetime.max.time())

    # --- CABEÇALHO ---
    header = "*Confira os destaques da semana no Sistema Estadual de Meio Ambiente e Recursos Hídricos de MG*\n\n"
    header += f"*📅 De {data_inicio.strftime('%d/%m/%y')} a {data_fim.strftime('%d/%m/%y')}*\n\n"
    
    resultado_final = header

    URLS = [
        "https://semad.mg.gov.br/noticias",
        "https://www.ief.mg.gov.br/noticias",
        "https://feam.br/noticias",
        "https://igam.mg.gov.br/noticias"
    ]

    headers_nav = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    encontrou_algo = False
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_urls = len(URLS)

    for i, url in enumerate(URLS):
        progress_bar.progress((i) / total_urls)
        
        try:
            orgao = "DESCONHECIDO"
            if "semad" in url: orgao = "SEMAD"
            elif "ief" in url: orgao = "IEF"
            elif "feam" in url: orgao = "FEAM"
            elif "igam" in url: orgao = "IGAM"
            
            status_text.text(f"Lendo notícias do {orgao}...")

            response = requests.get(url, headers=headers_nav, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('a')
            
            noticias_orgao = []

            for link in articles:
                text = link.get_text(" ", strip=True)
                href = link.get('href')

                if not href or not text: continue
                if "assetCategoryIds" in href: continue
                if text.strip().lower() in ["destaque", "leia mais", "voltar"]: continue

                if href.startswith('/'):
                    base_url = "/".join(url.split('/')[:3])
                    full_link = base_url + href
                else:
                    full_link = href
                
                if "?" in full_link: full_link = full_link.split('?')[0]

                match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
                if not match and link.parent:
                    parent_text = link.parent.get_text(" ", strip=True)
                    match = re.search(r'(\d{2}/\d{2}/\d{4})', parent_text)

                if match:
                    data_str = match.group(1)
                    try:
                        news_date = datetime.strptime(data_str, "%d/%m/%Y")
                        if start_date <= news_date <= end_date:
                            clean_title = text.replace(data_str, "").strip()
                            clean_title = clean_title.replace(" - ", "").strip()
                            
                            if clean_title:
                                titulo_existe = False
                                for item in noticias_orgao:
                                    if clean_title in item['titulo']:
                                        titulo_existe = True; break
                                
                                if not titulo_existe:
                                    emoji = obter_emoji_exclusivo(clean_title, emojis_usados_na_sessao)
                                    status_text.text(f"Encurtando: {clean_title[:30]}...")
                                    short_link = encurtar_link(full_link)
                                    
                                    noticias_orgao.append({
                                        'titulo': clean_title,
                                        'link': short_link,
                                        'emoji': emoji
                                    })
                    except ValueError: continue

            if noticias_orgao:
                resultado_final += f"*{orgao}*\n\n"
                for noticia in noticias_orgao:
                    resultado_final += f"{noticia['emoji']} {noticia['titulo']}\n{noticia['link']}\n\n"
                encontrou_algo = True

        except Exception as e:
            st.error(f"Erro no {orgao}: {e}")

    # --- RODAPÉ ---
    footer = "Quer saber mais? Acesse o site e siga nossas redes sociais:\n"
    footer += "Instagram: @meioambienteminasgerais\n"
    footer += "Facebook: facebook.com/meioambienteminasgerais\n"
    footer += "Youtube: youtube.com/\n"
    footer += "Linkedin: linkedin.com/company/semadmg/\n"
    footer += "Site: meioambiente.mg.gov.br\n"
    footer += "Contato: ascom@meioambiente.mg.gov.br"
    
    resultado_final += footer

    progress_bar.progress(100)
    status_text.empty()
    time.sleep(0.5)
    progress_bar.empty()

    if encontrou_algo:
        st.success("Boletim gerado com sucesso!")
        st.markdown("---")
        st.markdown("**Copie o texto abaixo:**")
        st.code(resultado_final, language="text")
    else:
        st.warning("Nenhuma notícia encontrada neste período.")