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
icone  = pygame.image.load("recursos/garra.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
garra = pygame.image.load("recursos/garra.png")
fundoStart = pygame.image.load("recursos/telaStartQuit.png")
fundoJogo = pygame.image.load("recursos/fundoJogo.png")
fundoPause = pygame.image.load("recursos/telaPause.png")
#fundoDead = pygame.image.load("assets/fundoDead.png")
urso = pygame.image.load("recursos/ursinho.png")
#missileSound = pygame.mixer.Sound("assets/missile.wav")
#explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
clique = pygame.mixer.Sound("recursos/click.wav")
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
    

    posicaoXGarra = 400
    posicaoYGarra = 175
    movimentoXGarra  = 0
    movimentoYGarra  = 0
    posicaoXUrso = 445
    posicaoYUrso = 400
    #pygame.mixer.Sound.play(missileSound)
    #pygame.mixer.music.play(-1)
    pontos = 0
    larguraGarra = 100
    alturaGarra = 80
    larguraUrso  = 75
    alturaUrso  = 75
    dificuldade  = 30
    ursoPego = False

    ursosVogais = {
        "ursoA" : [pygame.image.load("recursos/ursinho.png"), random.randint(110,250),300],
        "ursoE" : ["CAMINHO URSO E", random.randint(260,300),300],
        "ursoI" : ["CAMINHO URSO I", random.randint(310,350),300],
        "ursoO" : ["CAMINHO URSO O", random.randint(360,400),300],
        "ursoU" : ["CAMINHO URSO U", random.randint(410,450),400],
    }
    ursosConsoantes = {
        "ursoT" : [pygame.image.load("recursos/ursinho.png"), random.randint(110,250),300],
        "ursoP" : ["CAMINHO URSO E", random.randint(260,300),300],
        "ursoC" : ["CAMINHO URSO I", random.randint(310,350),300],
        "ursoB" : ["CAMINHO URSO O", random.randint(360,400),300],
        "ursoM" : ["CAMINHO URSO U", random.randint(410,450),400],
    }

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
                movimentoYGarra = -10
                movimentoXGarra = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYGarra = 10
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
        
        if posicaoXGarra < 130 :
            posicaoXGarra = 135
        elif posicaoXGarra >770:
            posicaoXGarra = 765
            
        if posicaoYGarra < 170 :
            posicaoYGarra = 175
        elif posicaoYGarra > 370:
            posicaoYGarra = 360

        if posicaoYGarra > 175:
            movimentoXGarra = 0
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        tela.blit(garra, (posicaoXGarra, posicaoYGarra))

        for chave in ursosVogais.keys():    
            tela.blit(ursosVogais[chave][0], (ursosVogais[chave][1], ursosVogais[chave][2]))
        
        texto = fonteMenu.render("Points: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        texto = fonteMenu.render("Press Space to Pause Game", True, branco)
        tela.blit(texto, (15,45))
        
        pixelsGarraX = list(range(posicaoXGarra, posicaoXGarra+larguraGarra))
        pixelsGarraY = list(range(posicaoYGarra, posicaoYGarra+alturaGarra))
        pixelsUrsoX = list(range(posicaoXUrso, posicaoXUrso + larguraUrso))
        pixelsUrsoY = list(range(posicaoYUrso, posicaoYUrso + alturaUrso))
        
        os.system("cls")
        
        if len(list(set(pixelsUrsoY).intersection(set(pixelsGarraY)))) > dificuldade:
            if len(list(set(pixelsUrsoX).intersection(set(pixelsGarraX)))) > dificuldade:
                escreverDados(nome, pontos)
                pygame.mixer.Sound.play(clique)
                pygame.mixer.music.play(-1)
                ursoPego = True
                #dead()
                
        if ursoPego:
            posicaoXUrso = posicaoXGarra + 5
            posicaoYUrso = posicaoYGarra + alturaGarra - 20
        
        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 375
    alturaButtonStart  = 110

    larguraButtonQuit = 225
    alturaButtonQuit  = 95
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startRect.collidepoint(evento.pos):
                    larguraButtonStart = 375
                    alturaButtonStart  = 110
                if quitRect.collidepoint(evento.pos):
                    larguraButtonQuit = 225
                    alturaButtonQuit  = 95
                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startRect.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonStart = 375
                    alturaButtonStart  = 110
                    jogar()
                if quitRect.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    larguraButtonQuit = 225
                    alturaButtonQuit  = 95
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart,(0,0))

        startButton = pygame.image.load("recursos/botaoStart.png")
        startRect = startButton.get_rect(topleft=(270, 250))
        tela.blit(startButton, (270,250))
        
        quitButton = pygame.image.load("recursos/botaoQuit.png")
        quitRect = quitButton.get_rect(topleft=(350, 380))
        tela.blit(quitButton, (350,380))
        
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

