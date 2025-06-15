import pygame, random, os, math
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
import json

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho) 
pygame.display.set_caption("A Garra")
icone  = pygame.image.load("recursos/ursinho_dourado.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
garra = pygame.image.load("recursos/garraLongasemfundo.png")
fundoStart = pygame.image.load("recursos/startAndQuit.png")
fundoJogo = pygame.image.load("recursos/telaJogo.png")
fundoPerdeu = pygame.image.load("recursos/telaPerdeu.png")
maquinaCima = pygame.image.load("recursos/telaJogoMaquinaCima.png")
joyStick = pygame.image.load("recursos/telaJoySticksemfundo.png")
fundoPause = pygame.image.load("recursos/paused.png")
buracoUrso = pygame.image.load("recursos/buracoUrso.png")
somCaptura = pygame.mixer.Sound("recursos/pickup_2.wav")
somGameOver = pygame.mixer.Sound("recursos/game_over.wav")
somClique = pygame.mixer.Sound("recursos/click.wav")
somPegar = pygame.mixer.Sound("recursos/pickup_2.wav")
fonteMenu = pygame.font.Font("recursos/PressStart2P.ttf",14)
fontePontos = pygame.font.Font("recursos/PressStart2P.ttf",24)
fonteMorte = pygame.font.Font("recursos/PressStart2P.ttf",18)
fonteNome = pygame.font.Font("recursos/PressStart2P.ttf",42)
pygame.mixer.music.load("recursos/Boppy1minloop.mp3")
nomeDigitado = False


def jogar():
    largura_janela = 300
    altura_janela = 50
    if not nomeDigitado:
        def obter_nome():
            global nome, nomeDigitado
            nome = entry_nome.get()  # Obtém o texto digitado
            if not nome:  # Se o campo estiver vazio
                messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
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
        root.title("Informe seu nickname")
        root.protocol("WM_DELETE_WINDOW", obter_nome)

        # Entry (campo de texto)
        entry_nome = tk.Entry(root)
        entry_nome.pack()

        # Botão para pegar o nome
        botao = tk.Button(root, text="Enviar", command=obter_nome)
        botao.pack()

        # Inicia o loop da interface gráfica
        root.mainloop()
    
    cadastroRealizado = True
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
        "ursoA" : [pygame.image.load("recursos/ursoAsemfundoPequeno.png"), random.randint(160,170),280],
        "ursoE" : [pygame.image.load("recursos/ursoEsemfundoPequeno.png"), random.randint(270,280),280],
        "ursoI" : [pygame.image.load("recursos/ursoIsemfundoPequeno.png"), random.randint(380,390),280],
        "ursoO" : [pygame.image.load("recursos/ursoOsemfundoPequeno.png"), random.randint(470,480),280],
        "ursoU" : [pygame.image.load("recursos/ursoUsemfundoPequeno.png"), random.randint(585,595),280],
    }
    ursosConsoantes = {
        "ursoH" : [pygame.image.load("recursos/ursoHsemfundoPequeno.png"), random.randint(100,120),315],
        "ursoJ" : [pygame.image.load("recursos/ursoJsemfundoPequeno.png"), random.randint(230,240),300],
        "ursoK" : [pygame.image.load("recursos/ursoKsemfundoPequeno.png"), random.randint(330,340),315],
        "ursoB" : [pygame.image.load("recursos/ursoBsemfundoPequeno.png"), random.randint(430,440),315],
        "ursoG" : [pygame.image.load("recursos/ursoGsemfundoPequeno.png"), random.randint(535,545),315],
    }

    ursos = {**ursosVogais, **ursosConsoantes}
    ursosPegos = []
    ursosVogaisPegos = []
    ursosConsoantesPegos = []

    urso_img = pygame.image.load("recursos/ursinho_dourado.png").convert_alpha()
    tamanho = 64
    urso_img = pygame.transform.scale(urso_img, (tamanho, tamanho))

    ursoAleatorioXMin = 375
    ursoAleatorioXMax = 550
    ursoAleatorioYMin = 500
    ursoAleatorioYMax = 575

    # Posição inicial aleatória
    x = random.randint(ursoAleatorioXMin, ursoAleatorioXMax)
    y = random.randint(ursoAleatorioYMin, ursoAleatorioYMax)

    # Direção de movimento aleatória
    velocidade = 0.5
    dx = random.uniform(-1, 1)
    dy = random.uniform(-1, 1)


        # Temporizador para trocar a direção
    tempo_mudanca = 5000  # a cada 2 segundos
    ultimo_tempo = pygame.time.get_ticks()

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
        tela.blit(texto, (470,65))
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
        x += dx * velocidade
        y += dy * velocidade


        if x < ursoAleatorioXMin or x > ursoAleatorioXMax:
            dx *= -1
        if y < ursoAleatorioYMin or y > ursoAleatorioYMax:
            dy *= -1

        # Trocar direção a cada intervalo de tempo
        agora = pygame.time.get_ticks()
        if agora - ultimo_tempo > tempo_mudanca:
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            ultimo_tempo = agora

        # Desenhar o ursinho na tela
        tela.blit(urso_img, (int(x - tamanho // 2), int(y - tamanho // 2)))

        pygame.display.update()
        relogio.tick(60)


def telaVitoria():
    fundoVitoria = pygame.image.load("recursos/telaVitoria.png")
    textoVitoria = fonteNome.render(f"{nome}", True, branco)

    larguraButtonStart = 350
    alturaButtonStart  = 100
    larguraButtonQuit = 350
    alturaButtonQuit  = 100

    while True:
        tela.fill(branco)
        tela.blit(fundoVitoria, (0, 0))  # Exibe a imagem de fundo de boas-vindas
        tela.blit(textoVitoria, (500,180))

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
        startTexto = fonteMenu.render("Jogar novamente", True, preto)
        tela.blit(startTexto, (400,440))
        
        quitButton = pygame.draw.rect(tela, branco, (325,510, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (410,540))

        pygame.display.update()
        relogio.tick(60)


def telaBoasVindas():
    # Carregar fundo da tela de boas-vindas
    fundoBoasVindas = pygame.image.load("recursos/telaBoasVindas.png")
    textoBemVindo = fonteNome.render(f"{nome}", True, branco)

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
    global ptbr
    ptbr = True
    def botoes(caminhoButtonPlay, caminhoButtonQuit):
            global startRect, quitRect, botaoPtBrRect, botaoEnUsRect
            startButton = pygame.image.load(caminhoButtonPlay)
            startRect = startButton.get_rect(topleft=(405, 210))
            tela.blit(startButton, (405,210))

            quitButton = pygame.image.load(caminhoButtonQuit)
            quitRect = quitButton.get_rect(topleft=(425, 330))
            tela.blit(quitButton, (425,330))

            botaoPtBr = pygame.image.load("recursos/botaoPTBR.png")
            botaoPtBrRect = botaoPtBr.get_rect(topleft=(800,15))
            tela.blit(botaoPtBr, (800,15))

            botaoEnUs = pygame.image.load("recursos/botaoENUS.png")
            botaoEnUsRect = botaoEnUs.get_rect(topleft=(800,115))
            tela.blit(botaoEnUs,(800,115))    


    larguraButtonStart = 355
    alturaButtonStart  = 105

    larguraButtonQuit = 330
    alturaButtonQuit  = 100

    larguraButtonPtBr = 150
    alturaButtonPtBr = 84

    larguraButtonEnUs = 150
    alturaButtonEnUs = 81
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startRect.collidepoint(evento.pos):
                    larguraButtonStart = 355
                    alturaButtonStart  = 105
                if quitRect.collidepoint(evento.pos):
                    larguraButtonQuit = 330
                    alturaButtonQuit  = 110
                if botaoPtBrRect.collidepoint(evento.pos):
                    larguraButtonPtBr = 150
                    alturaButtonPtBr = 84
                if botaoEnUsRect.collidepoint(evento.pos):
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
                if quitRect.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonQuit = 330
                    alturaButtonQuit  = 110
                    pygame.mixer.Sound.play(somClique)
                    quit()
                if botaoPtBrRect.collidepoint(evento.pos):
                    larguraButtonPtBr = 150
                    alturaButtonPtBr = 84
                    ptbr = True
                if botaoEnUsRect.collidepoint(evento.pos):
                    larguraButtonEnUs = 150
                    alturaButtonEnUs = 81
                    ptbr = False
                    
        tela.fill(branco)
        tela.blit(fundoStart,(0,0))

        if ptbr:
            botoes("recursos/botaoInicie.png", "recursos/botaoSair.png")
        else:
            botoes("recursos/botaoStartv2.png","recursos/botaoQuitv2.png")    
        
        pygame.display.update()
        relogio.tick(60)


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
        titulo = fontePontos.render("Últimos Registros", True, branco)
        tela.blit(titulo,(300,150))

        yOffSet = 200
        for linha in logsRenderizados:
            tela.blit(linha, (200, yOffSet))
            yOffSet += 40

        
        startButton = pygame.draw.rect(tela, branco, (325,400, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Jogar novamente", True, preto)
        tela.blit(startTexto, (400,440))
        
        quitButton = pygame.draw.rect(tela, branco, (325,510, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (410,540))


        pygame.display.update()
        relogio.tick(60)


start()

