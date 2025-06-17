import pygame, random, math, threading
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.funcoesVoz import ouvir
from recursos.funcoesVoz import falar
import json
from queue import Queue


pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho) 
pygame.display.set_caption("A Garra")
icone  = pygame.image.load("recursos/imagens/icoUrsinho_dourado.ico")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
garra = pygame.image.load("recursos/imagens/garraLongasemfundo.png")
fundoStart = pygame.image.load("recursos/imagens/startAndQuit.png")
fundoJogo = pygame.image.load("recursos/imagens/telaJogo.png")
fundoPerdeu = pygame.image.load("recursos/imagens/telaPerdeu.png")
maquinaCima = pygame.image.load("recursos/imagens/telaJogoMaquinaCima.png")
joyStick = pygame.image.load("recursos/imagens/telaJoySticksemfundo.png")
buracoUrso = pygame.image.load("recursos/imagens/buracoUrso.png")
engrenagem = pygame.image.load("recursos/imagens/engrenagemSemfundo.png").convert_alpha()
somCaptura = pygame.mixer.Sound("recursos/sons/pickup_2.wav")
somGameOver = pygame.mixer.Sound("recursos/sons/game_over.wav")
somClique = pygame.mixer.Sound("recursos/sons/click.wav")
somPegar = pygame.mixer.Sound("recursos/sons/pickup_2.wav")
fonteMenu = pygame.font.Font("recursos/fontes/PressStart2P.ttf",14)
fontePontos = pygame.font.Font("recursos/fontes/PressStart2P.ttf",24)
fonteMorte = pygame.font.Font("recursos/fontes/PressStart2P.ttf",18)
fonteNome = pygame.font.Font("recursos/fontes/PressStart2P.ttf",42)
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.load("recursos/sons/Boppy1minloop.mp3")
nomeDigitado = False
falaResultado = None
fila_falas = Queue()



def jogar():
    largura_janela = 300
    altura_janela = 50
    if not nomeDigitado:
        def obter_nome():
            global nome, nomeDigitado
            nome = entry_nome.get()  # Obtém o texto digitado
            if not nome:  # Se o campo estiver vazio
                messagebox.showwarning("Aviso", "Por favor, digite seu nome!") if ptbr else messagebox.showwarning("Alert", "Please, type your name!")
            else:
                nomeDigitado = True
                #print(f'Nome digitado: {nome}')  # Exibe o nome no console
                root.destroy()  # Fecha a janela após a entrada válida
                telaBoasVindas()


        # Criação da janela principal
        root = tk.Tk()
        # Obter as dimensões da tela
        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        root.title("Informe seu nickname") if ptbr else root.title("Enter your nickname")
        root.protocol("WM_DELETE_WINDOW", obter_nome)

        # Entry (campo de texto)
        entry_nome = tk.Entry(root)
        entry_nome.pack()

        # Botão para pegar o nome
        if ptbr:
            botao = tk.Button(root, text="Enviar", command=obter_nome)
        else:
            botao = tk.Button(root, text="Send", command=obter_nome)
        botao.pack()

        # Inicia o loop da interface gráfica
        root.mainloop()
    
    posicaoXGarra = 500
    posicaoYGarra = -200
    movimentoXGarra  = 0
    movimentoYGarra  = 0
    pontos = 0
    larguraGarra = 115
    alturaGarra = 400
    larguraUrso  = 90
    alturaUrso  = 120
    larguraBuraco = 276
    alturaBuraco = 65
    posicaoXBuraco = 653
    posicaoYBuraco = 390

    ursoSelecionado = None

    ursosVogais = {
        "ursoA" : [pygame.image.load("recursos/imagens/ursoAsemfundoPequeno.png"), random.randint(160,170),280],
        "ursoE" : [pygame.image.load("recursos/imagens/ursoEsemfundoPequeno.png"), random.randint(270,280),280],
        "ursoI" : [pygame.image.load("recursos/imagens/ursoIsemfundoPequeno.png"), random.randint(380,390),280],
        "ursoO" : [pygame.image.load("recursos/imagens/ursoOsemfundoPequeno.png"), random.randint(470,480),280],
        "ursoU" : [pygame.image.load("recursos/imagens/ursoUsemfundoPequeno.png"), random.randint(585,595),280],
    }
    ursosConsoantes = {
        "ursoH" : [pygame.image.load("recursos/imagens/ursoHsemfundoPequeno.png"), random.randint(100,120),315],
        "ursoJ" : [pygame.image.load("recursos/imagens/ursoJsemfundoPequeno.png"), random.randint(230,240),300],
        "ursoK" : [pygame.image.load("recursos/imagens/ursoKsemfundoPequeno.png"), random.randint(330,340),315],
        "ursoB" : [pygame.image.load("recursos/imagens/ursoBsemfundoPequeno.png"), random.randint(430,440),315],
        "ursoG" : [pygame.image.load("recursos/imagens/ursoGsemfundoPequeno.png"), random.randint(535,545),315],
    }

    ursos = {**ursosVogais, **ursosConsoantes}
    ursosPegos = []
    ursosVogaisPegos = []
    ursosConsoantesPegos = []

    ursoDourado = pygame.image.load("recursos/imagens/ursinho_dourado.png").convert_alpha()
    tamanho = 36
    ursoDourado = pygame.transform.scale(ursoDourado, (tamanho, tamanho))

    ursoAleatorioXMin = 750
    ursoAleatorioXMax = 900
    ursoAleatorioYMin = 469
    ursoAleatorioYMax = 470

    # Posição inicial aleatória
    x = random.randint(ursoAleatorioXMin, ursoAleatorioXMax)
    y = random.randint(ursoAleatorioYMin, ursoAleatorioYMax)

    # Direção de movimento aleatória
    velocidade = 0.5
    direcaoAleatoriaX = random.uniform(-1, 1)
    direcaoAleatoriaY = random.uniform(-1, 1)


    # Temporizador para trocar a direção
    tempo_mudanca = 5000
    ultimo_tempo = pygame.time.get_ticks()

    angulo = 0
    tempo = 0
    raioBase = 64

    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXGarra = 2
                movimentoYGarra = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXGarra = -2
                movimentoYGarra = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXGarra = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXGarra = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYGarra = -5
                movimentoXGarra = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYGarra = 5
                movimentoXGarra = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYGarra = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYGarra = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pause = True
                while pause:
                    if ptbr:
                        fundoPause = pygame.image.load("recursos/imagens/pausado.png")
                    else:
                        fundoPause = pygame.image.load("recursos/imagens/paused.png")
                    tela.blit(fundoPause, (0,0))
                    pygame.display.update()
        
                    for eventoPausa in pygame.event.get():
                        if eventoPausa.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif eventoPausa.type == pygame.KEYDOWN and eventoPausa.key == pygame.K_SPACE:
                            pause = False

                
        posicaoXGarra += movimentoXGarra            
        posicaoYGarra += movimentoYGarra       
        
        if posicaoXGarra < 95 :
            posicaoXGarra = 100
        elif posicaoXGarra > 820:
            posicaoXGarra = 815
            
        if posicaoYGarra < -200 :
            posicaoYGarra = -195
        elif posicaoYGarra > 50:
            posicaoYGarra = 55

        if posicaoYGarra > -175:
            movimentoXGarra = 0
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0))

        for nomeUrso in ursos.keys():
            if nomeUrso not in ursosPegos:
                tela.blit(ursos[nomeUrso][0], (ursos[nomeUrso][1], ursos[nomeUrso][2]))
        
        tela.blit(garra, (posicaoXGarra, posicaoYGarra))
        tela.blit(maquinaCima,(1,0))
        tela.blit(joyStick,(190,415))
        if ptbr:
            texto = fontePontos.render("Pontos: "+str(pontos), True, branco) 
        else:
            texto = fontePontos.render("Points: "+str(pontos), True, branco)

        tela.blit(texto, (400,55))
        if ptbr:
            texto = fonteMenu.render("Pressione Espaço para Pausar o Jogo", True, branco) 
        else: 
            texto = fonteMenu.render("Press Space to Pause Game", True, branco)
        
        tela.blit(texto, (15,15))
        
        garraRect = pygame.Rect(posicaoXGarra, posicaoYGarra, larguraGarra, alturaGarra)

        for nomeUrso, dadosUrso in ursos.items():
            ursoRect = pygame.Rect(dadosUrso[1], dadosUrso[2], larguraUrso, alturaUrso)    
        
            for eventoAgarrar in eventos:
                if eventoAgarrar.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif eventoAgarrar.type == pygame.KEYDOWN and eventoAgarrar.key == pygame.K_RETURN: 
                    if garraRect.colliderect(ursoRect):
                        pygame.mixer.Sound.play(somPegar)
                        if not pygame.mixer.music.get_busy():
                            pygame.mixer.music.play(-1)
                        ursoSelecionado = nomeUrso
                        break   

        if ursoSelecionado:
            ursos[ursoSelecionado][1] = posicaoXGarra + 10
            ursos[ursoSelecionado][2] = posicaoYGarra + alturaGarra - 10
            if ursos[ursoSelecionado][2] > 335:
                ursos[ursoSelecionado][2] = 330
        
            if posicaoXBuraco + 45 < ursos[ursoSelecionado][1] + 45 < posicaoXBuraco + larguraBuraco:
                if ursos[ursoSelecionado][2] + 60 == posicaoYBuraco:
                    ursosPegos.append(ursoSelecionado)
                    ursoSelecionado = None
                    pygame.mixer.Sound.play(somPegar)
            
        for ursoPego in ursosPegos:
            if ursoPego in ursosVogais.keys():
                if ursoPego not in ursosVogaisPegos:
                    ursosVogaisPegos.append(ursoPego)
                    pontos = len(ursosVogaisPegos)
            elif ursoPego in ursosConsoantes.keys():
                if ursoPego not in ursosConsoantesPegos:
                    ursosConsoantesPegos.append(ursoPego)
            
        if len(ursosConsoantesPegos) == 2:
            escreverDados(nome, pontos)
            perdeu()

        if len(ursosVogaisPegos) == 5:
            print("vitoria")
            telaVitoria()

        # Mover o ursinho
        x += direcaoAleatoriaX * velocidade
        y += direcaoAleatoriaY * velocidade

        if x < ursoAleatorioXMin or x > ursoAleatorioXMax:
            direcaoAleatoriaX *= -1
        if y < ursoAleatorioYMin or y > ursoAleatorioYMax:
            direcaoAleatoriaY *= -1

        # Trocar direção a cada intervalo de tempo
        agora = pygame.time.get_ticks()
        if agora - ultimo_tempo > tempo_mudanca:
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            ultimo_tempo = agora

        tela.blit(ursoDourado, (int(x - tamanho // 2), int(y - tamanho // 2)))


        # Atualiza o ângulo e o fator de escala (pulsação)
        angulo += 0.75
        tempo += 0.05
        escala = 1 + 0.1 * math.sin(tempo)  # Efeito de pulsar
        tamanho = int(raioBase * 2 * escala)
        
        # Redimensiona e rotaciona a imagem
        engrenagemEscalada = pygame.transform.smoothscale(engrenagem, (tamanho, tamanho))
        engrenagemRotacionada = pygame.transform.rotate(engrenagemEscalada, angulo)

        engrenagemRect = engrenagemRotacionada.get_rect(topright=(1050, -50))

        tela.blit(engrenagemRotacionada, engrenagemRect)

        pygame.display.update()
        relogio.tick(60)


def telaVitoria():
    if ptbr:
        fundoVitoria = pygame.image.load("recursos/imagens/telaVitoria.png")
    else:
        fundoVitoria = pygame.image.load("recursos/imagens/telaVictory.png")
    textoVitoria = fonteNome.render(f"{nome}", True, branco)

    larguraButtonStart = 350
    alturaButtonStart  = 100
    larguraButtonQuit = 350
    alturaButtonQuit  = 100

    while True:
        tela.fill(branco)
        tela.blit(fundoVitoria, (0, 0))  # Exibe a imagem de fundo de boas-vindas
        tela.blit(textoVitoria, (425,180))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 350
                    alturaButtonStart  = 100
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 350
                    alturaButtonQuit  = 100
 
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonStart = 350
                    alturaButtonStart  = 100
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonQuit = 350
                    alturaButtonQuit  = 100
                    quit()


        startButton = pygame.draw.rect(tela, branco, (325,400, larguraButtonStart, alturaButtonStart), border_radius=15)
        if ptbr:
            startTexto = fonteMenu.render("Jogar novamente", True, preto) 
        else: 
            startTexto = fonteMenu.render("Play Again", True, preto)
        
        tela.blit(startTexto, (400,440))
        
        quitButton = pygame.draw.rect(tela, branco, (325,510, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        if ptbr:
            quitTexto = fonteMenu.render("Sair do Jogo", True, preto)
        else:
            quitTexto = fonteMenu.render("Quit Game", True, preto)
        
        tela.blit(quitTexto, (410,545))

        pygame.display.update()
        relogio.tick(60)


def telaBoasVindas():
    # Carregar fundo da tela de boas-vindas
    if ptbr:
        fundoBoasVindas = pygame.image.load("recursos/imagens/telaBoasVindas.png")
    else:
        fundoBoasVindas = pygame.image.load("recursos/imagens/telaWelcome.png")
    textoBemVindo = fonteNome.render(f"{nome}", True, branco)
    falar("Bem vindo", nome) if ptbr else falar("Welcome", nome)

    while True:
        tela.fill(branco)
        tela.blit(fundoBoasVindas, (0, 0))  # Exibe a imagem de fundo de boas-vindas
        tela.blit(textoBemVindo, (450,50))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                jogar()

        pygame.display.update()
        relogio.tick(60)


def start():
    import threading
    global ptbr, falaResultado
    ptbr = True
    def botoes(caminhoButtonPlay, caminhoButtonQuit):
            global startRect, quitRect, botaoPtBrRect, botaoEnUsRect
            startButton = pygame.image.load(caminhoButtonPlay)
            startRect = startButton.get_rect(topleft=(405, 210))
            tela.blit(startButton, (405,210))

            quitButton = pygame.image.load(caminhoButtonQuit)
            quitRect = quitButton.get_rect(topleft=(425, 330))
            tela.blit(quitButton, (425,330))

            botaoPtBr = pygame.image.load("recursos/imagens/botaoPTBR.png")
            botaoPtBrRect = botaoPtBr.get_rect(topleft=(800,15))
            tela.blit(botaoPtBr, (800,15))

            botaoEnUs = pygame.image.load("recursos/imagens/botaoENUS.png")
            botaoEnUsRect = botaoEnUs.get_rect(topleft=(800,115))
            tela.blit(botaoEnUs,(800,115))    

    thread_voz = threading.Thread(target=ouvir, daemon=True)
    thread_voz.start()

    larguraButtonStart = 355
    alturaButtonStart  = 105

    larguraButtonQuit = 330
    alturaButtonQuit  = 100

    larguraButtonPtBr = 150
    alturaButtonPtBr = 84

    larguraButtonEnUs = 150
    alturaButtonEnUs = 81

    while True:
        tela.fill(branco)
        tela.blit(fundoStart,(0,0))

        botoes("recursos/imagens/botaoInicie.png", "recursos/imagens/botaoSair.png") if ptbr else botoes("recursos/imagens/botaoStartv2.png","recursos/imagens/botaoQuitv2.png")
        
        pygame.display.update()
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startRect.collidepoint(evento.pos):
                    larguraButtonStart = 355
                    alturaButtonStart  = 105
                elif quitRect.collidepoint(evento.pos):
                    larguraButtonQuit = 330
                    alturaButtonQuit  = 110
                elif botaoPtBrRect.collidepoint(evento.pos):
                    larguraButtonPtBr = 150
                    alturaButtonPtBr = 84
                elif botaoEnUsRect.collidepoint(evento.pos):
                    larguraButtonEnUs = 150
                    alturaButtonEnUs = 81
                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startRect.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonStart = 355
                    alturaButtonStart  = 105
                    pygame.mixer.Sound.play(somClique)
                    jogar()
                elif quitRect.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonQuit = 330
                    alturaButtonQuit  = 110
                    pygame.mixer.Sound.play(somClique)
                    quit()
                elif botaoPtBrRect.collidepoint(evento.pos):
                    larguraButtonPtBr = 150
                    alturaButtonPtBr = 84
                    ptbr = True
                elif botaoEnUsRect.collidepoint(evento.pos):
                    larguraButtonEnUs = 150
                    alturaButtonEnUs = 81
                    ptbr = False

        if not fila_falas.empty():
            fala = fila_falas.get().strip().lower()
            if any(p in fala for p in ["começar", "iniciar", "jogar"]):
                pygame.mixer.music.play(-1)
                pygame.mixer.Sound.play(somClique)
                jogar()
            elif any(p in fala for p in ["sair", "fechar", "encerrar"]):
                pygame.mixer.music.play(-1)
                pygame.mixer.Sound.play(somClique)
                quit()



def perdeu():
    print("perdeu")
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(somGameOver)
    
    with open("log.dat", "r") as arquivo:
        log_partidas = json.load(arquivo)

    ultimosLogs = list(log_partidas.items())[-5:]    
    
    logsRenderizados = []
    for nome, dados in reversed(ultimosLogs):
        pontos, data, hora = dados
        textoLog = f"{nome} - {pontos} pts - {data} às {hora}"
        textoLogRender = fonteMorte.render(textoLog, True, branco)
        logsRenderizados.append(textoLogRender)



    larguraButtonStart = 350
    alturaButtonStart  = 100
    larguraButtonQuit = 350
    alturaButtonQuit  = 100
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 350
                    alturaButtonStart  = 100
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 350
                    alturaButtonQuit  = 100

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonStart = 350
                    alturaButtonStart  = 100
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonQuit = 350
                    alturaButtonQuit  = 100
                    quit()
                    
        
        tela.blit(fundoPerdeu, (0,0))
        if ptbr:
            titulo = fontePontos.render("Últimos Registros", True, branco)
        else:
            titulo = fontePontos.render("Latest Entries", True, branco)
        tela.blit(titulo,(300,150))

        yOffSet = 200
        for linha in logsRenderizados:
            tela.blit(linha, (200, yOffSet))
            yOffSet += 40

        
        startButton = pygame.draw.rect(tela, branco, (325,400, larguraButtonStart, alturaButtonStart), border_radius=15)
        if ptbr:
            startTexto = fonteMenu.render("Jogar novamente", True, preto) 
        else:
            startTexto = fonteMenu.render("Play Again", True, preto)
        tela.blit(startTexto, (400,440))
        
        quitButton = pygame.draw.rect(tela, branco, (325,510, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        if ptbr:
            quitTexto = fonteMenu.render("Sair do Jogo", True, preto) 
        else:
            quitTexto = fonteMenu.render("Quit Game", True, preto)
        tela.blit(quitTexto, (410,545))


        pygame.display.update()
        relogio.tick(60)


start()

