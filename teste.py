import random, pygame, os
pygame.mixer.init()
PASTA = os.path.dirname(os.path.abspath(__file__))

def tocar_audio(nome):
    caminho_audio = None

    # Procura o áudio na pasta do projeto e em todas as subpastas
    for raiz, pastas, arquivos in os.walk(PASTA):
        if nome in arquivos:
            caminho_audio = os.path.join(raiz, nome)
            break

    # Verifica se encontrou o arquivo
    if caminho_audio is None:
        print(f"Áudio não encontrado: {nome}")
        return

    # Reproduz o áudio
    pygame.mixer.music.load(caminho_audio)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def classificar_resultado(vida, vida_max):
    """Diz como foi a batalha olhando a vida que sobrou para o herói:
        vida igual a 0              -> "Derrota" K.O
        vida igual a vida_max       -> "Vitória perfeita" PERFECT
        vida >= metade de vida_max  -> "Vitória" smash bros
        senão                       -> "Vitória apertada" SENA WIN """
    if vida == 0:
        tocar_audio("defeat.mp3")
        print("Derrota")
        return "Derrota"

    elif vida == vida_max:
        tocar_audio("perfect.mp3")
        print("Vitória perfeita")
        return "Vitória perfeita"

    elif vida >= vida_max / 2:
        tocar_audio("victory.mp3")
        print("Vitória")
        return "Vitória"

    else:
        tocar_audio("vitória-apertada.mp3")
        print("Vitória apertada")
        return "Vitória apertada"
classificar_resultado(0, 100)
