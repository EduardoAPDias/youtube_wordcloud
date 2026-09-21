from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api.formatters import TextFormatter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
from nltk.corpus import stopwords

URL = "https://www.youtube.com/watch?v=Q8IqC7L-NjQ"


def extrair_video_id(url: str) -> str:
    query = urlparse(url).query
    video_id = parse_qs(query)["v"][0]
    return video_id

PALAVRAS_EXTRAS = {
    "ta", "tá", "cara", "vai", "né", "tipo", "aí", "então", "assim", "tal", "gente", "irmão", "vamos", "agora", "pro", "aqui", "porque", "lá", "ter", "acho", "tô", "vou", "ali", "acha",
    "seguinte", "fala", "falou", "falar", "além", "__", "quero", "fez", "pode", "faz", "sei", "sabe", "tava", "vem", "conta", "coisa", "tudo", "qu", "ó", "pr", "falando", "mim" , "falei"
, "deixa", "deixar", "fazer" , "contra", "quer", "disso", "qualquer", "vão", "sob", "pessoas", "onde", "inclusive", "têm", "sobre", "pois", "deu", "ainda", ""
}

def limpar_texto(texto: str, palavras_extras: set[str] = PALAVRAS_EXTRAS) -> list[str]:
    stopwords_pt = set(stopwords.words('portuguese')) | palavras_extras
    palavras = re.findall(r'\b[^\W\d_]+\b', texto.lower())
    tokens_limpos = [
        palavra for palavra in palavras
        if palavra not in stopwords_pt and len(palavra) > 2
    ]
    return tokens_limpos

def contar_frequencias(tokens: list[str]) -> Counter:
    return Counter(tokens)

ytt_api = YouTubeTranscriptApi()
fetched_transcript = ytt_api.fetch(extrair_video_id(URL), languages=['pt'])

formatter = TextFormatter()
texto_bruto = formatter.format_transcript(fetched_transcript)

tokens = limpar_texto(texto_bruto)
frequencias = contar_frequencias(tokens)

print(frequencias.most_common(100))  # print 100 palavras mais frequentes, para conferir

nuvem = WordCloud(width=1200, height=800, background_color='white', max_words=80, prefer_horizontal=0.9).generate_from_frequencies(frequencias)
plt.imshow(nuvem, interpolation='bilinear')
plt.axis('off')
plt.show()
