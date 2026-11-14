"""Repete pelo SDK o que foi feito no Language Studio.

Para cada arquivo de texto: idioma, sentimento (com mineração de opinião),
frases-chave, entidades nomeadas e dados pessoais (PII).

Uso:
    set LANGUAGE_ENDPOINT=https://<seu-recurso>.cognitiveservices.azure.com/
    set LANGUAGE_KEY=<sua-chave>
    python scripts/analisar_texto.py exemplos/textos/review1.txt [outros arquivos...]

Endpoint e chave ficam em "Chaves e Ponto de Extremidade" no portal do Azure.
Nunca coloque a chave no código nem no GitHub.
"""

import os
import sys

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def criar_cliente():
    endpoint = os.environ.get("LANGUAGE_ENDPOINT")
    chave = os.environ.get("LANGUAGE_KEY")
    if not endpoint or not chave:
        sys.exit("Defina as variáveis de ambiente LANGUAGE_ENDPOINT e LANGUAGE_KEY.")
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(chave))


def analisar(cliente, texto):
    idioma = cliente.detect_language([texto])[0]
    print(f"Idioma: {idioma.primary_language.name} ({idioma.primary_language.confidence_score:.2f})")
    codigo = idioma.primary_language.iso6391_name

    sentimento = cliente.analyze_sentiment([texto], language=codigo, show_opinion_mining=True)[0]
    s = sentimento.confidence_scores
    print(f"Sentimento: {sentimento.sentiment} (positivo {s.positive:.2f} | neutro {s.neutral:.2f} | negativo {s.negative:.2f})")
    for frase in sentimento.sentences:
        for opiniao in frase.mined_opinions:
            avaliacoes = ", ".join(f"{a.text} ({a.sentiment})" for a in opiniao.assessments)
            print(f"  - {opiniao.target.text}: {avaliacoes}")

    frases = cliente.extract_key_phrases([texto], language=codigo)[0]
    print("Frases-chave:", ", ".join(frases.key_phrases))

    entidades = cliente.recognize_entities([texto], language=codigo)[0]
    print("Entidades:")
    for e in entidades.entities:
        print(f"  - {e.text} [{e.category}] ({e.confidence_score:.2f})")

    pii = cliente.recognize_pii_entities([texto], language=codigo)[0]
    if pii.entities:
        print("Dados pessoais:", ", ".join(f"{e.text} [{e.category}]" for e in pii.entities))
        print("Texto mascarado:", pii.redacted_text)


def main():
    arquivos = sys.argv[1:]
    if not arquivos:
        sys.exit(__doc__)
    cliente = criar_cliente()
    for caminho in arquivos:
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        print(f"\n===== {caminho}")
        analisar(cliente, texto)


if __name__ == "__main__":
    main()
