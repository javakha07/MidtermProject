import pygame
from game_logic import start_game
from data_handler import view_logs, save_logs
from api_handler import fetch_leaderboard, add_score

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SPACE INVADERS")

# Main Menu
def main_menu():
    running = True
    clock = pygame.time.Clock()
    retro_font = pygame.font.Font("assets/fonts/ARCADECLASSIC.ttf", 24)
    selected_option = 0
    options = ["Start Game", "View Logs", "Leaderboard", "Exit"]

    while running:
        screen.fill((0, 0, 0))
        title_text = retro_font.render("SPACE INVADERS", True, (0, 255, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150))
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            option_text = retro_font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + i * 40))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        score = start_game(screen, clock)
                        if score is not None:
                            name = input_name(screen, retro_font)
                            if name.strip():
                                add_score(name, score)
                    elif selected_option == 1:
                        show_logs(screen, retro_font)
                    elif selected_option == 2:
                        show_leaderboard(screen, retro_font)
                    elif selected_option == 3:
                        running = False

        pygame.display.flip()
        clock.tick(FPS)

def input_name(screen, font):
    name = ""
    input_active = True
    while input_active:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return ""
                else:
                    if len(name) < 10 and event.unicode.isalnum():
                        name += event.unicode
        
        title = font.render("Enter your name:", True, (255, 255, 255))
        name_text = font.render(name, True, (255, 255, 0))
        instruction = font.render("Press ENTER to confirm or ESC to cancel", True, (255, 255, 255))
        
        screen.blit(title, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(name_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()
    return name

def show_leaderboard(screen, font):
    scores = fetch_leaderboard()
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        title = font.render("LEADERBOARD", True, (255, 255, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - 100, 50))
        
        if not scores:
            text = font.render("No scores yet!", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, 150))
        else:
            for i, score in enumerate(scores):
                text = font.render(f"{i+1}. {score['name']}: {score['score']}", True, (255, 255, 255))
                screen.blit(text, (SCREEN_WIDTH // 2 - 150, 150 + i * 40))
        
        exit_text = font.render("Press any key to return", True, (255, 255, 0))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                return
        
        pygame.display.flip()

def show_logs(screen, font):
    logs = view_logs()
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        title = font.render("GAME LOGS", True, (255, 255, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - 100, 50))
        
        for i, log in enumerate(logs):
            text = font.render(log.strip(), True, (255, 255, 255))
            screen.blit(text, (50, 150 + i * 40))
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
        
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
