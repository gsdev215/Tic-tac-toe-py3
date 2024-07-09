import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Game variables
board = [['' for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
winner = None
player1_name = "Player 1"
player2_name = "Player 2"
comp_name = "Computer"
player1_score = 0
player2_score = 0
comp_score = 0
leaderboard = []

# Music
pygame.mixer.init()
pygame.mixer.music.load("no_worries.mp3")
pygame.mixer.music.play(-1)
volume = 0.5
pygame.mixer.music.set_volume(volume)

def draw_board(if_comp):
    screen.fill(WHITE)
    for row in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, row * 200), (600, row * 200), 5)
        pygame.draw.line(screen, BLACK, (row * 200, 0), (row * 200, 600), 5)
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * 200 + 50, row * 200 + 50), (col * 200 + 150, row * 200 + 150), 5)
                pygame.draw.line(screen, RED, (col * 200 + 150, row * 200 + 50), (col * 200 + 50, row * 200 + 150), 5)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLUE, (col * 200 + 100, row * 200 + 100), 50, 5)

    # Display player names
    player1_text = font.render(f"X: {player1_name}", True, BLACK)
    player2_text = font.render(f"O: {player2_name}", True, BLACK) if not if_comp else font.render(f"O: {comp_name}", True, BLACK)
    screen.blit(player1_text, (10, SCREEN_HEIGHT - 40))
    screen.blit(player2_text, (SCREEN_WIDTH - player2_text.get_width() - 10, SCREEN_HEIGHT - 40))

def check_winner():
    global game_over, winner

    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '':
            winner = board[i][0]
            game_over = True
            return
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '':
            winner = board[0][i]
            game_over = True
            return
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        winner = board[0][0]
        game_over = True
        return
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        winner = board[0][2]
        game_over = True
        return

    # Check for a draw
    if all(board[row][col] != '' for row in range(3) for col in range(3)):
        game_over = True

def reset_game():
    global board, current_player, game_over, winner
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None

def draw_button(text, position, center=True):
    button_text = font.render(text, True, BLACK)
    button_rect = button_text.get_rect()
    if center:
        button_rect.center = position
    else:
        button_rect.topleft = position
    screen.blit(button_text, button_rect)
    return button_rect

def main_menu():
    screen.fill(WHITE)
    title = font.render("Tic Tac Toe", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    play_pvp_button = draw_button("1. Player vs Player", (SCREEN_WIDTH // 2, 200))
    play_pvc_button = draw_button("2. Player vs Computer", (SCREEN_WIDTH // 2, 300))
    leaderboard_button = draw_button("3. Leaderboard", (SCREEN_WIDTH // 2, 400))
    settings_button = draw_button("4. Settings", (SCREEN_WIDTH // 2, 500))
    pygame.display.flip()
    return play_pvp_button, play_pvc_button, leaderboard_button, settings_button

def game_over_screen(if_comp:bool):
    global game_over, winner
    while game_over:
        draw_board(if_comp)

        # Draw translucent grey-black background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # Set transparency level (0-255)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))

        # Display winner or draw message
        if winner:
            text = font.render(f"{winner} wins!", True, WHITE)
        else:
            text = font.render("It's a draw!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))

        # Draw buttons
        play_again_button = draw_button("Play Again (R)", (SCREEN_WIDTH // 2, 300))
        main_menu_button = draw_button("Main Menu (M)", (SCREEN_WIDTH // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    reset_game()
                    return
                elif main_menu_button.collidepoint(event.pos):
                    game_over = False
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                elif event.key == pygame.K_m:
                    game_over = False
                    return

def update_leaderboard():
    global leaderboard
    leaderboard_dict = {name: score for name, score in leaderboard}
    leaderboard_dict[player1_name] = player1_score
    leaderboard_dict[player2_name] = player2_score
    leaderboard_dict[comp_name] = comp_score
    leaderboard = sorted(leaderboard_dict.items(), key=lambda x: x[1], reverse=True)

def display_leaderboard():
    screen.fill(WHITE)
    title = font.render("Leaderboard", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    for i, (name, score) in enumerate(leaderboard):
        text = font.render(f"{i + 1}. {name}: {score}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100 + i * 50))
    back_button = draw_button("Press B to go back", (SCREEN_WIDTH // 2, 500))
    pygame.display.flip()
    return back_button

def settings_menu():
    screen.fill(WHITE)
    title = font.render("Settings", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    volume_up_button = draw_button("Volume Up (+)", (SCREEN_WIDTH // 2, 200))
    volume_down_button = draw_button("Volume Down (-)", (SCREEN_WIDTH // 2, 300))
    change_player1_name_button = draw_button(f"Change {player1_name} Name", (SCREEN_WIDTH // 2, 400))
    change_player2_name_button = draw_button(f"Change {player2_name} Name", (SCREEN_WIDTH // 2, 500))
    back_button = draw_button("Press B to go back", (SCREEN_WIDTH // 2, 600))
    pygame.display.flip()
    return volume_up_button, volume_down_button, change_player1_name_button, change_player2_name_button, back_button

def player_vs_player():
    global current_player, game_over, winner, player1_score, player2_score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row, col = y // 200, x // 200
                if board[row][col] == '':
                    board[row][col] = current_player
                    check_winner()
                    if game_over:
                        if winner == "X":
                            player1_score += 1
                        elif winner == "O":
                            player2_score += 1
                    current_player = "O" if current_player == "X" else "X"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        draw_board(False)
        pygame.display.flip()

        if game_over:
            game_over_screen(False)
            update_leaderboard()
            if not game_over:
                reset_game()
                return 

def player_vs_computer():
    global current_player, game_over, winner, player1_score, comp_score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == "X":
                x, y = event.pos
                row, col = y // 200, x // 200
                if board[row][col] == '':
                    board[row][col] = current_player
                    check_winner()
                    if game_over:
                        if winner == "X":
                            player1_score += 1
                        elif winner == "O":
                            comp_score += 1
                    current_player = "O" if current_player == "X" else "X"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Computer's turn
        if not game_over and current_player == "O":
            pygame.time.wait(500)  # Delay for realism
            empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']
            if empty_cells:
                row, col = random.choice(empty_cells)
                board[row][col] = current_player
                check_winner()
                if game_over:
                    if winner == "X":
                        player1_score += 1
                    elif winner == "O":
                        comp_score += 1
                current_player = "O" if current_player == "X" else "X"

        draw_board(True)
        pygame.display.flip()

        if game_over:
            game_over_screen(True)
            update_leaderboard()
            if not game_over:
                reset_game()
                return 

def change_player_name(player_num):
    global player1_name, player2_name
    running = True
    input_text = ""
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_num == 1:
                        player1_name = input_text
                    elif player_num == 2:
                        player2_name = input_text
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill(WHITE)
        prompt = font.render(f"Enter new name for Player {player_num}:", True, BLACK)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (SCREEN_WIDTH // 2 - input_surface.get_width() // 2, 300))
        pygame.display.flip()

def settings():
    global volume
    volume_up_button, volume_down_button, change_player1_name_button, change_player2_name_button, back_button = settings_menu()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if volume_up_button.collidepoint(event.pos):
                    volume = min(volume + 0.1, 1.0)
                    pygame.mixer.music.set_volume(volume)
                elif volume_down_button.collidepoint(event.pos):
                    volume = max(volume - 0.1, 0.0)
                    pygame.mixer.music.set_volume(volume)
                elif change_player1_name_button.collidepoint(event.pos):
                    change_player_name(1)
                    settings_menu()
                elif change_player2_name_button.collidepoint(event.pos):
                    change_player_name(2)
                    settings_menu()
                elif back_button.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    running = False

play_pvp_button, play_pvc_button, leaderboard_button, settings_button = main_menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_pvp_button.collidepoint(event.pos):
                player_vs_player()
                play_pvp_button, play_pvc_button, leaderboard_button, settings_button = main_menu()
            elif play_pvc_button.collidepoint(event.pos):
                player_vs_computer()
                play_pvp_button, play_pvc_button, leaderboard_button, settings_button = main_menu()
            elif leaderboard_button.collidepoint(event.pos):
                back_button = display_leaderboard()
                leaderboard_menu = True
                while leaderboard_menu:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            leaderboard_menu = False
                            running = False
                        elif ev.type == pygame.MOUSEBUTTONDOWN:
                            if back_button.collidepoint(ev.pos):
                                leaderboard_menu = False
                        elif ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_b:
                                leaderboard_menu = False
                play_pvp_button, play_pvc_button, leaderboard_button, settings_button = main_menu()
            elif settings_button.collidepoint(event.pos):
                settings()
                play_pvp_button, play_pvc_button, leaderboard_button, settings_button = main_menu()

    pygame.display.flip()

pygame.quit()
