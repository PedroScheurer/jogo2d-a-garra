import pygame
import random
import os
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
icone  = pygame.image.load("recursos/garraLongasemfundo.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
garra = pygame.image.load("recursos/garraLongasemfundo.png")
fundoStart = pygame.image.load("recursos/startAndQuit.png")
fundoJogo = pygame.image.load("recursos/telaJogo.png")
maquinaCima = pygame.image.load("recursos/telaJogoMaquinaCima.png")
joyStick = pygame.image.load("recursos/telaJoySticksemfundo.png")
fundoPause = pygame.image.load("recursos/paused.png")
#fundoDead = pygame.image.load("assets/fundoDead.png")
#urso = pygame.image.load("recursos/ursinho.png")
#missileSound = pygame.mixer.Sound("assets/missile.wav")
#explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
somClique = pygame.mixer.Sound("recursos/click.wav")
somPegar = pygame.mixer.Sound("recursos/pickup_2.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/Boppy1minloop.mp3")

def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida

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
    

    posicaoXGarra = 500
    posicaoYGarra = -200
    movimentoXGarra  = 0
    movimentoYGarra  = 0
    pontos = 0
    larguraGarra = 115
    alturaGarra = 400
    larguraUrso  = 90
    alturaUrso  = 120
    dificuldade  = 30
    ursoPego = False
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

    while True:
        for evento in pygame.event.get():
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
                    tela.blit(fundoPause, (0,0) )
                    pygame.display.update()
        
                    for evento_pausa in pygame.event.get():
                        if evento_pausa.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif evento_pausa.type == pygame.KEYDOWN and evento_pausa.key == pygame.K_SPACE:
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
        tela.blit(fundoJogo, (0,0) )

        for chave in ursos.keys():    
            tela.blit(ursos[chave][0], (ursos[chave][1], ursos[chave][2]))
        
        tela.blit(garra, (posicaoXGarra, posicaoYGarra))
        tela.blit(maquinaCima,(1,0))
        tela.blit(joyStick,(190,415))

        
        texto = fonteMenu.render("Points: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        texto = fonteMenu.render("Press Space to Pause Game", True, branco)
        tela.blit(texto, (15,45))
        
        garraRect = pygame.Rect(posicaoXGarra, posicaoYGarra, larguraGarra, alturaGarra)
        pygame.draw.rect(tela, (255, 0, 0), garraRect, 2)
        
        for nomeUrso, dadosUrso in ursos.items():
            ursoRect = pygame.Rect(dadosUrso[1], dadosUrso[2], larguraUrso, alturaUrso)
            pygame.draw.rect(tela, (0, 255, 0), ursoRect, 2) 
            print(f"Garra: X={posicaoXGarra}, Y={posicaoYGarra}, Largura={larguraGarra}, Altura={alturaGarra}")
            print(f"Urso {nomeUrso}: X={dadosUrso[1]}, Y={dadosUrso[2]}, Largura={larguraUrso}, Altura={alturaUrso}")
        
        
            if garraRect.colliderect(ursoRect):
                escreverDados(nome, pontos)
                pygame.mixer.Sound.play(somPegar)
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
                ursoPego = True
                ursoSelecionado = nomeUrso
                break   
                    
        if ursoSelecionado:
            ursos[ursoSelecionado][1] = posicaoXGarra
            ursos[ursoSelecionado][2] = posicaoYGarra + alturaGarra
        
            
            print(f"Verificando colisão com {nomeUrso} na posição ({dadosUrso[1]}, {dadosUrso[2]})")
            os.system("cls")


        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 355
    alturaButtonStart  = 105

    larguraButtonQuit = 330
    alturaButtonQuit  = 100
    

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
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart,(0,0))

        startButton = pygame.image.load("recursos/botaoStartv2.png")
        startRect = startButton.get_rect(topleft=(405, 210))
        tela.blit(startButton, (405,210))
        
        quitButton = pygame.image.load("recursos/botaoQuitv2.png")
        quitRect = quitButton.get_rect(topleft=(425, 330))
        tela.blit(quitButton, (425,330))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
  #  pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 350
    alturaButtonStart  = 100
    larguraButtonQuit = 350
    alturaButtonQuit  = 100
    
    
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 350
                    alturaButtonStart  = 100
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 450
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
                    
        
            
            
        tela.fill(branco)
       # tela.blit(fundoDead, (0,0) )

        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)


start()

