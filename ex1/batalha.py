"""
batalha.py - Exercício 1: batalha por turnos.

Conteúdos: laços (while e for), estruturas de decisão (if/elif/else),
funções e parâmetros (inclusive parâmetros com valor padrão).

Cada lutador é um dicionário, por exemplo:
    {"nome": "Gork", "vida": 100, "vida_max": 100, "ataque": 18, "defesa": 5}

TAREFA: complete as funções marcadas com TODO. Apague a linha
"raise NotImplementedError" de cada função que você completar.
Para conferir, rode o arquivo testes_ex1.py.
"""


import random, os

try:
    import pygame
    pygame.mixer.init()
    AUDIO_DISPONIVEL = True
    print("Sistema de áudio iniciado!")
except Exception as erro:
    AUDIO_DISPONIVEL = False
    print("Erro ao iniciar áudio:", erro)

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def tocar_audio(nome):

    # Se não tiver Pygame, ignora o áudio
    if not AUDIO_DISPONIVEL:
        return

    caminho_audio = None

    # Procura o áudio nas pastas e subpastas
    for raiz, pastas, arquivos in os.walk(PASTA):
        if nome in arquivos:
            caminho_audio = os.path.join(raiz, nome)
            break

    # Se não encontrar o áudio, ignora
    if caminho_audio is None:
        return

    # Tenta reproduzir o áudio
    try:
        pygame.mixer.music.load(caminho_audio)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception:
        pass

def calcular_dano(ataque, defesa, critico=False, erro_critico=False):
    """Dano = ataque - defesa, mas nunca menos que 1.
    Se for um golpe crítico, o dano dobra.
    Exemplos: calcular_dano(18, 3) -> 15    calcular_dano(18, 3, True) -> 30
              calcular_dano(5, 12) -> 1"""
    dano = max(1, ataque - defesa)
    if critico == True:
        dano = dano *2
        print("Golpe crítico!")
        tocar_audio("critico.mp3")
    elif erro_critico == True:
        dano = 0
        print("Você errou o ataque!")
        tocar_audio("falha.mp3")
    return dano

def aplicar_dano(nome, vida, dano, vida_max):
    """Devolve a vida depois do golpe (nunca fica negativa).
    Exemplos: aplicar_dano(60, 15) -> 45    aplicar_dano(10, 15) -> 0"""
    vida -= dano
    if vida < 0:
        vida = 0
    tocar_audio("bonk.mp3")
    print(f"{nome} sofreu {dano} de dano!\n VIDA ATUAL: {vida}/{vida_max}")
    
    return vida


def curar(vida, vida_max, cura=30):
    """Devolve a vida depois de tomar uma poção (nunca passa de vida_max).
    Exemplos: curar(50, 100) -> 80    curar(90, 100) -> 100"""
    vida += cura
    if vida > vida_max:
        vida = vida_max
    tocar_audio("cura.mp3")
    print(f"Você tomou uma poção e recuperou {cura} de vida!\n SUA VIDA ATUAL: {vida}/{vida_max}")
    return vida


def barra_de_vida(vida, vida_max, tamanho=10):
    """Monta uma barra de texto com 'tamanho' caracteres, por exemplo:
        barra_de_vida(60, 100) -> "[######----] 60/100"
    Quantidade de '#':  vida * tamanho // vida_max   (o resto é '-')
    Use um laço for com range(tamanho)."""
    barra = ''
    for i in range(tamanho):
        if i < vida * tamanho // vida_max:
            barra += '#'
        else:
            barra += '-'
    return f"[{barra}] {vida}/{vida_max}"

def classificar_resultado(resultado, vida, vida_max):
    """Diz como foi a batalha olhando a vida que sobrou para o herói:
        vida igual a 0              -> "Derrota" K.O
        vida igual a vida_max       -> "Vitória perfeita" PERFECT
        vida >= metade de vida_max  -> "Vitória" smash bros
        senão                       -> "Vitória apertada" SENA WIN """
    if vida == 0:
        tocar_audio("defeat.mp3")
        print("Derrota")
        return "Derrota"

    elif resultado == "fuga":
        tocar_audio("cagao.mp3")
        print("Medroso!")
        return "Fuga"


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



def ler_acao():
    """Mostra as ações e repete a pergunta ATÉ a pessoa digitar 1, 2 ou 3.
    Devolve o texto digitado ("1", "2" ou "3").
        1 - Atacar   2 - Tomar poção   3 - Fugir
    Se digitar outra coisa, mostre "Ação inválida!" e pergunte de novo."""
    while True:
        print("Escolha sua ação:")
        acao = input("1 - Atacar   2 - Tomar poção   3 - Fugir\n")
        if acao == "1":
            return 1
        elif acao == "2":
            return 2
        elif acao == "3":
            return 3
        else:
            print("Ação inválida!")


def batalha(heroi, inimigo, pocoes=3):
    turno = 0
    resultado = None

    while heroi["vida"] > 0 and inimigo["vida"] > 0:
        turno += 1

        print(f"\n--- Turno {turno} ---")
        print(f"{heroi['nome']:<12} {barra_de_vida(heroi['vida'], heroi['vida_max'])}")
        print(f"{inimigo['nome']:<12} {barra_de_vida(inimigo['vida'], inimigo['vida_max'])}")

        acao = ler_acao()

        if acao == 1:
            r = random.randint(1, 10)

            critico = (r == 10)
            erro_critico = (r == 1)
            dano = calcular_dano(
                heroi["ataque"], inimigo["defesa"], critico, erro_critico
            )

            inimigo["vida"] = aplicar_dano(
                inimigo["nome"], inimigo["vida"],
                dano, inimigo["vida_max"]
            )

        elif acao == 2:
            if pocoes > 0:
                pocoes -= 1
                heroi["vida"] = curar(
                    heroi["vida"], heroi["vida_max"]
                )
                print(f"Você tem {pocoes} poções restantes.")
            else:
                print("Você não tem poções restantes!")
                continue

        elif acao == 3:
            resultado = "fuga"
            break

        # Verifica se o inimigo foi derrotado
        if inimigo["vida"] <= 0:
            print(f"{inimigo['nome']} foi derrotado!")
            tocar_audio("K.O.mp3")
            resultado = "vitoria"
            break

        # Vez do inimigo atacar
        r = random.randint(1, 10)

        critico = (r == 10)
        erro_critico = (r == 1)
        dano = calcular_dano(
            inimigo["ataque"], heroi["defesa"], critico, erro_critico
        )

        heroi["vida"] = aplicar_dano(
            heroi["nome"], heroi["vida"],
            dano, heroi["vida_max"]
        )

    if heroi["vida"] <= 0:
        resultado = "derrota"
        tocar_audio("K.O.mp3")

    elif resultado is None:
        resultado = "vitoria"

    print(
        "\n" + classificar_resultado(
            resultado, heroi["vida"], heroi["vida_max"]
        ) + "!"
    )

    return {
        "resultado": resultado,
        "turnos": turno,
        "vida_restante": heroi["vida"],
        "pocoes": pocoes
    }



# Este bloco só roda quando executamos ESTE arquivo (python batalha.py).
# Quando outro arquivo faz "import batalha", ele NÃO roda.
if __name__ == "__main__":
    heroi = {"nome": "Gork", "vida": 100, "vida_max": 100, "ataque": 18, "defesa": 5}
    inimigo = {"nome": "Goblin", "vida": 60, "vida_max": 60, "ataque": 12, "defesa": 3}
    final = batalha(heroi, inimigo)
    print(final)
