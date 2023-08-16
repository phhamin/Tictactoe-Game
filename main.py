import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

#Màu
colormain = (61,52,139)
colorsub = (224,226,219)

screen = pygame.display.set_mode(size)

#Font
mediumFont = pygame.font.Font("LilitaOne-Regular.ttf", 28)
largeFont = pygame.font.Font("LilitaOne-Regular.ttf", 40)
moveFont = pygame.font.Font("LilitaOne-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(colormain)

    if user is None:

        #Vẽ giao diện
        title = largeFont.render("Tic Tac Toe", True, colorsub)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        #Vẽ các nút
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("ROLE X", True, colormain)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, colorsub, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("ROLE O", True, colormain)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, colorsub, playOButton)
        screen.blit(playO, playORect)

        #Kiểm tra nút đã bấm chưa
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        #Vẽ trên bảng
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, colorsub, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, colorsub)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        #Hiển thị
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"RESULT: Draw."
            else:
                title = f"RESULT: {winner} Win."
        elif user == player:
            title = f"Turn {user}"
        else:
            title = f"Computer ..."
        title = largeFont.render(title, True, colorsub)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        #Kiểm tra di chuyển của máy
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board) #Sử dụng thuật toán
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        #Kiểm tra lượt đi
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, colormain)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, colorsub, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    
                    ai_turn = False

    pygame.display.flip()
