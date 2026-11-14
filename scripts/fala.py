"""Repete pelo SDK o que foi feito no Speech Studio.

    python scripts/fala.py transcrever exemplos/audio/time.wav
    python scripts/fala.py falar "Olá! Esta voz foi gerada pelo Azure." saida.wav

O primeiro comando converte fala em texto (o áudio do exemplo está em inglês).
O segundo converte texto em fala com uma voz neural em português e salva um .wav.

Antes, defina:
    set SPEECH_KEY=<sua-chave>
    set SPEECH_REGION=<sua-regiao, ex.: brazilsouth>
"""

import os
import sys

import azure.cognitiveservices.speech as speechsdk

VOZ_PT = "pt-BR-FranciscaNeural"


def configuracao():
    chave = os.environ.get("SPEECH_KEY")
    regiao = os.environ.get("SPEECH_REGION")
    if not chave or not regiao:
        sys.exit("Defina as variáveis de ambiente SPEECH_KEY e SPEECH_REGION.")
    return speechsdk.SpeechConfig(subscription=chave, region=regiao)


def transcrever(arquivo, idioma="en-US"):
    config = configuracao()
    config.speech_recognition_language = idioma
    audio = speechsdk.audio.AudioConfig(filename=arquivo)
    resultado = speechsdk.SpeechRecognizer(speech_config=config, audio_config=audio).recognize_once()
    if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Reconhecido:", resultado.text)
    else:
        print("Nada reconhecido:", resultado.reason)


def falar(texto, saida):
    config = configuracao()
    config.speech_synthesis_voice_name = VOZ_PT
    audio = speechsdk.audio.AudioOutputConfig(filename=saida)
    resultado = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio).speak_text_async(texto).get()
    if resultado.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Áudio salvo em", saida)
    else:
        print("Falhou:", resultado.reason)


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "transcrever":
        transcrever(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "falar":
        falar(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
