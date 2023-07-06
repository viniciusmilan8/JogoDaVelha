import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Dimensões da janela
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# Cores
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

# Tamanho da célula do tabuleiro
CELL_SIZE = 200

# Tamanho da fonte
FONT_SIZE = 25
FONT = pygame.font.Font(None, FONT_SIZE)

# Criação da janela
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jogo da Velha")

# Carregamento das imagens
image_x = pygame.image.load("X.png")
image_o = pygame.image.load("O.png")
image_restart = pygame.image.load("restart.png")
image_exit = pygame.image.load("exit.png")

# Carregamento dos sons
sound_win = pygame.mixer.Sound("vitoria.flac")
sound_draw = pygame.mixer.Sound("click.wav")

# Carregamento das imagens com novo tamanho
image_x = pygame.transform.scale(image_x, (int(CELL_SIZE * 0.4), int(CELL_SIZE * 0.4)))
image_o = pygame.transform.scale(image_o, (int(CELL_SIZE * 0.4), int(CELL_SIZE * 0.4)))

# Função para desenhar o tabuleiro na janela
def draw_board(board):
    window.fill(BACKGROUND_COLOR)

    # Desenha as linhas do tabuleiro
    pygame.draw.line(window, LINE_COLOR, (0, CELL_SIZE), (WINDOW_WIDTH, CELL_SIZE), 4)
    pygame.draw.line(window, LINE_COLOR, (0, CELL_SIZE * 2), (WINDOW_WIDTH, CELL_SIZE * 2), 4)
    pygame.draw.line(window, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, WINDOW_HEIGHT - 100), 4)
    pygame.draw.line(window, LINE_COLOR, (CELL_SIZE * 2, 0), (CELL_SIZE * 2, WINDOW_HEIGHT - 100), 4)

    # Desenha os símbolos (X ou O) nas células ocupadas
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                symbol_rect = image_x.get_rect(center=(col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2))
                window.blit(image_x, symbol_rect)
            elif board[row][col] == "O":
                symbol_rect = image_o.get_rect(center=(col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2))
                window.blit(image_o, symbol_rect)

    # Desenha a barra inferior
    pygame.draw.rect(window, BACKGROUND_COLOR, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))
    pygame.draw.line(window, LINE_COLOR, (0, WINDOW_HEIGHT - 100), (WINDOW_WIDTH, WINDOW_HEIGHT - 100), 4)

    # Desenha o botão Restart
    restart_button_rect = image_restart.get_rect()
    restart_button_rect.center = (WINDOW_WIDTH // 4, WINDOW_HEIGHT - 40)
    window.blit(image_restart, restart_button_rect)
    draw_text("F2 para reiniciar", WINDOW_WIDTH // 4, WINDOW_HEIGHT - 80)

    # Desenha o botão Exit
    exit_button_rect = image_exit.get_rect()
    exit_button_rect.center = (WINDOW_WIDTH // 4 * 3, WINDOW_HEIGHT - 40)
    window.blit(image_exit, exit_button_rect)
    draw_text("ESC para sair", WINDOW_WIDTH // 4 * 3, WINDOW_HEIGHT - 80)

    # Desenha as mensagens de vitória ou empate
    if winner == "X":
        draw_text("Jogador X venceu!", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        sound_win.play()
    elif winner == "O":
        draw_text("Jogador O venceu!", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        sound_win.play()
    elif winner == "Draw":
        draw_text("Empate!", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)

    pygame.display.flip()


# Função para desenhar texto na janela
def draw_text(text, x, y):
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)


# Função para verificar se há um vencedor ou empate
def check_winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != None:
            return board[row][0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != None:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]

    if all(cell is not None for row in board for cell in row):
        return "Draw"

    return None


# Função para reiniciar o jogo
def restart_game():
    global board, current_player, winner
    board = [[None] * 3 for _ in range(3)]
    current_player = "X"
    winner = None
    sound_win.stop()
    draw_board(board)


# Variáveis do jogo
board = [[None] * 3 for _ in range(3)]
current_player = "X"
winner = None

# Loop principal do jogo
running = True
draw_board(board)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < WINDOW_HEIGHT - 100:
                col = mouse_pos[0] // CELL_SIZE
                row = mouse_pos[1] // CELL_SIZE
                if board[row][col] == None and winner == None:
                    board[row][col] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                    winner = check_winner()
                    draw_board(board)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F2:
                restart_game()

pygame.quit()
sys.exit()
