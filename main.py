import pygame
import sys
import time

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
CELL_SIZE = WIDTH // BOARD_COLS
PION_RADIUS = CELL_SIZE // 3

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (220, 220, 220)
LINE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Men's Morris - Fixed Start")
screen.fill(BG_COLOR)


class Game:
    def __init__(self):
        # Plateau de jeu: 0 = vide, 1 = joueur 1, 2 = joueur 2
        self.board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

        # Initialisation des positions de départ
        # Joueur 1 (rouge) en haut
        self.board[0][0] = 1
        self.board[0][1] = 1
        self.board[0][2] = 1

        # Joueur 2 (bleu) en bas
        self.board[2][0] = 2
        self.board[2][1] = 2
        self.board[2][2] = 2

        self.player = 1  # Joueur 1 commence
        self.game_over = False
        self.winner = None
        self.selected_piece = None
        self.valid_moves = []

        # Définition des mouvements valides pour chaque position
        # Format: {(row, col): [(row_destination, col_destination), ...], ...}
        self.valid_connections = self.create_valid_connections()

        # Liste des connexions pour le rendu visuel
        self.visual_connections = [
            # Connexions horizontales
            ((0, 0), (0, 1)), ((0, 1), (0, 2)),
            ((1, 0), (1, 1)), ((1, 1), (1, 2)),
            ((2, 0), (2, 1)), ((2, 1), (2, 2)),

            # Connexions verticales
            ((0, 0), (1, 0)), ((1, 0), (2, 0)),
            ((0, 1), (1, 1)), ((1, 1), (2, 1)),
            ((0, 2), (1, 2)), ((1, 2), (2, 2)),

            # Connexions diagonales en X
            ((0, 0), (1, 1)), ((1, 1), (2, 2)),
            ((0, 2), (1, 1)), ((1, 1), (2, 0))
        ]

    def create_valid_connections(self):
        # Création d'un dictionnaire avec tous les mouvements valides pour chaque position
        connections = {}

        # Pour chaque case du plateau
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                connections[(row, col)] = []

                # Mouvements horizontaux et verticaux (toujours permis vers des cases adjacentes)
                # Haut
                if row > 0:
                    connections[(row, col)].append((row - 1, col))
                # Bas
                if row < BOARD_ROWS - 1:
                    connections[(row, col)].append((row + 1, col))
                # Gauche
                if col > 0:
                    connections[(row, col)].append((row, col - 1))
                # Droite
                if col < BOARD_COLS - 1:
                    connections[(row, col)].append((row, col + 1))

                # Mouvements diagonaux (seulement les diagonales principales "en X")
                # Coin haut-gauche vers coin bas-droite
                if (row == 0 and col == 0) or (row == 2 and col == 2):
                    if (row == 0 and col == 0):
                        connections[(row, col)].append((1, 1))  # vers le centre
                    if (row == 2 and col == 2):
                        connections[(row, col)].append((1, 1))  # vers le centre

                # Coin haut-droite vers coin bas-gauche
                if (row == 0 and col == 2) or (row == 2 and col == 0):
                    if (row == 0 and col == 2):
                        connections[(row, col)].append((1, 1))  # vers le centre
                    if (row == 2 and col == 0):
                        connections[(row, col)].append((1, 1))  # vers le centre

                # Centre vers les quatre coins
                if row == 1 and col == 1:
                    connections[(row, col)].append((0, 0))  # haut-gauche
                    connections[(row, col)].append((0, 2))  # haut-droite
                    connections[(row, col)].append((2, 0))  # bas-gauche
                    connections[(row, col)].append((2, 2))  # bas-droite

        return connections

    def draw_board(self):
        # Fond
        screen.fill(BG_COLOR)

        # Dessiner les points (intersections) où les pions peuvent être placés
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = row * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, BLACK, (center_x, center_y), 8)

        # Dessiner les lignes de connexion
        for start, end in self.visual_connections:
            start_row, start_col = start
            end_row, end_col = end

            start_x = start_col * CELL_SIZE + CELL_SIZE // 2
            start_y = start_row * CELL_SIZE + CELL_SIZE // 2
            end_x = end_col * CELL_SIZE + CELL_SIZE // 2
            end_y = end_row * CELL_SIZE + CELL_SIZE // 2

            pygame.draw.line(
                screen,
                LINE_COLOR,
                (start_x, start_y),
                (end_x, end_y),
                LINE_WIDTH // 2
            )

        # Dessiner les pions
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = row * CELL_SIZE + CELL_SIZE // 2

                if self.board[row][col] == 1:
                    color = RED
                    pygame.draw.circle(screen, color, (center_x, center_y), PION_RADIUS)
                elif self.board[row][col] == 2:
                    color = BLUE
                    pygame.draw.circle(screen, color, (center_x, center_y), PION_RADIUS)

        # Surbrillance de la pièce sélectionnée
        if self.selected_piece:
            row, col = self.selected_piece
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (center_x, center_y), PION_RADIUS + 5, 5)

        # Afficher les mouvements valides
        for row, col in self.valid_moves:
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (center_x, center_y), 10)

        # Afficher le tour du joueur actuel
        font = pygame.font.SysFont(None, 30)
        if not self.game_over:
            text = f"Tour du Joueur {self.player} ({'Rouge' if self.player == 1 else 'Bleu'})"
            text_surface = font.render(text, True, BLACK)
            screen.blit(text_surface, (20, 20))
        else:
            if self.winner:
                text = f"Joueur {self.winner} ({'Rouge' if self.winner == 1 else 'Bleu'}) a gagné!"
            else:
                text = "Match nul!"
            text_surface = font.render(text, True, BLACK)
            screen.blit(text_surface, (20, 20))

            # Instructions pour recommencer
            restart_text = "Appuyez sur R pour recommencer"
            restart_surface = font.render(restart_text, True, BLACK)
            screen.blit(restart_surface, (20, 50))

    def get_row_col_from_mouse(self, mouse_pos):
        x, y = mouse_pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return row, col

    def get_valid_moves(self, row, col):
        # Retourne les mouvements valides pour une pièce à la position (row, col)
        valid = []

        # Obtenir tous les mouvements possibles pour cette position selon la structure du jeu
        possible_moves = self.valid_connections.get((row, col), [])

        # Filtrer pour ne garder que les cases vides
        for new_row, new_col in possible_moves:
            if self.board[new_row][new_col] == 0:
                valid.append((new_row, new_col))

        return valid

    def check_win(self):
        # Vérifier si tous les pions du joueur 1 sont sur la première ligne (bord initial)
        player1_on_start_row = True
        for col in range(BOARD_COLS):
            if self.board[0][col] != 1:
                player1_on_start_row = False
                break

        # Si tous les pions du joueur 1 sont sur sa ligne de départ, il ne peut pas gagner
        if player1_on_start_row:
            return None

        # Vérifier si tous les pions du joueur 2 sont sur la dernière ligne (bord initial)
        player2_on_start_row = True
        for col in range(BOARD_COLS):
            if self.board[2][col] != 2:
                player2_on_start_row = False
                break

        # Si tous les pions du joueur 2 sont sur sa ligne de départ, il ne peut pas gagner
        if player2_on_start_row:
            return None

        # Vérifier les lignes
        for row in range(BOARD_ROWS):
            if self.board[row][0] != 0 and self.board[row][0] == self.board[row][1] == self.board[row][2]:
                # Vérifier que le joueur 1 n'est pas sur sa ligne de départ (ligne 0)
                if self.board[row][0] == 1 and row == 0:
                    continue
                # Vérifier que le joueur 2 n'est pas sur sa ligne de départ (ligne 2)
                if self.board[row][0] == 2 and row == 2:
                    continue
                return self.board[row][0]

        # Vérifier les colonnes
        for col in range(BOARD_COLS):
            if self.board[0][col] != 0 and self.board[0][col] == self.board[1][col] == self.board[2][col]:
                return self.board[0][col]

        # Vérifier les diagonales
        if self.board[0][0] != 0 and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] != 0 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]

        return None

    def handle_click(self, mouse_pos):
        if self.game_over:
            return

        row, col = self.get_row_col_from_mouse(mouse_pos)

        # Si aucune pièce n'est sélectionnée
        if self.selected_piece is None:
            # Si la case cliquée contient une pièce du joueur actuel
            if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and self.board[row][col] == self.player:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)

        # Si une pièce est déjà sélectionnée
        else:
            # Si le joueur clique sur un mouvement valide
            if (row, col) in self.valid_moves:
                # Déplacer la pièce
                old_row, old_col = self.selected_piece
                self.board[old_row][old_col] = 0
                self.board[row][col] = self.player

                # Vérifier s'il y a un gagnant
                winner = self.check_win()
                if winner:
                    self.game_over = True
                    self.winner = winner
                else:
                    # Passer au joueur suivant
                    self.player = 3 - self.player  # Alternance entre 1 et 2

                # Réinitialiser la sélection
                self.selected_piece = None
                self.valid_moves = []

            # Si le joueur clique sur une autre de ses pièces
            elif 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and self.board[row][col] == self.player:
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)

            # Si le joueur clique ailleurs, annuler la sélection
            else:
                self.selected_piece = None
                self.valid_moves = []

    def reset(self):
        # Réinitialiser le jeu
        self.__init__()


# Création du jeu
game = Game()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Touche R pour recommencer
                game.reset()

    # Dessiner le plateau
    game.draw_board()

    # Mettre à jour l'affichage
    pygame.display.update()

    # Limiter la fréquence d'images
    pygame.time.Clock().tick(60)