from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет головы змейки
SNAKE_HEAD_COLOR = (0, 200, 50)

# Цвет глаз змейки
SNAKE_EYES_COLOR = (0, 0, 250)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject служит для описания общих атрибутов и методов объектов,
    которые используются в игре.
    """

    def __init__(self) -> None:
        """Метод инициализирует начальную позицию и цвет объектов."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT) // 2)
        self.body_color = None

    def draw(self):
        """Этот метод определяет, как объект будет отрисовываться на экране.
        Для каждого дочернего класса объектов игры метод переопределяется.
        """
        pass


class Apple(GameObject):
    """Класс Apple описывает объект яблоко."""

    def __init__(self):
        """Метод переинициализирует начальную позицию яблока, с учетом
        стартовой позиции змейки. Задает цвет яблока.
        """
        super().__init__()
        self.position = self.randomize_position(self.position)
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод отрисовывает яблоко в виде окружности."""
        center = (self.position[0] + 10, self.position[1] + 10)
        pygame.draw.circle(screen, self.body_color, center, (GRID_SIZE) // 2)
        pygame.draw.circle(screen, BORDER_COLOR, center, (GRID_SIZE) // 2, 1)

    def randomize_position(self, positions):
        """Метод случайным образом выбирает новую позицию яблока так,чтобы
        она не совпала с текущим положением змейки.
        То есть после выбора нового положения яблока, проверяется, не совпало
        ли оно с какой-либо точкой из тела змейки. Если совпало, то выбирается
        другое случайное значение. И так продолжается, пока новое положение
        яблока не окажется вне тела змейки.
        """
        point = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                 randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        while point in positions:
            point = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                     randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return point


class Snake(GameObject):
    """Класс nake описывает объект змейка."""

    def __init__(self):
        """Метод переинициализирует начальную позицию змейки в центре экрана.
        Задает цвет тела змейки. Дополнительно добавляет цвета головы и глаз
        змейки, начальное направление движения.
        Атрибут next_direction - используется как следующее направление
        движения. В рачалеБ следующее направление движения задается как None,
        в дальнейшем оно определяется в методе handle_keys.
        Атрибут last - используется для хранения позиции последнего сегмента
        змейки перед тем, как он исчезнет (при движении змейки). Это
        необходимо для «стирания» этого сегмента с игрового поля, чтобы змейка
        визуально двигалась.
        """
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.head_color = SNAKE_HEAD_COLOR
        self.eyes_color = SNAKE_EYES_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]

    def update_direction(self):
        """Метод update_direction обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_position):
        """Метод move обновляет позицию змейки. А именно:
        - Добавляется новая голова в начало списка positions.
        - Если змейка не съела яблоко (новая позиция головы не совпала с
          текущим положением яблока), то удаляется последний элемент тела
          змейки.
        Также осуществляется проверка, не наткнулась ли змейка на свое тело
        (новая позиция головы змейки совпала с каким-либо элементом списка
        positions).
        Функция возвращает следующие значения:
        - 'apple', если змейка съела яблоко,
        - 'tail', если змейка наткнулась на свое тело,
        - None, если голова змейки оказалась в свободном поле.
        """
        head = self.get_head_position()
        new_width = (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_height = (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_width, new_height))
        if self.positions[0] == apple_position:
            self.last = None
            return 'apple'
        self.last = self.positions[-1]
        self.positions.pop()
        if self.positions[0] in self.positions[1:]:
            return 'tail'
        else:
            return None

    def get_head_position(self):
        """Метод получает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод запускает игру сначала (возвращает змейку в исходное
        состояние).
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.__init__()

    def draw(self):
        """Метод отрисовывает змейку."""
        # Отрисовка змейки не включая головы
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.head_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        left_eye = (self.positions[0][0] + 5, self.positions[0][1] + 5)
        pygame.draw.circle(screen, self.eyes_color, left_eye, 2)
        right_eye = (self.positions[0][0] + 15, self.positions[0][1] + 5)
        pygame.draw.circle(screen, self.eyes_color, right_eye, 2)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Метод handle_keys определяет дальнейшее направление движения змейки, в
    зависимости от кнопки, которую нажимает игрок.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция используетсяБ чтобы код из нее не запускался из внешних
    модулей.
    """
    # Инициализация PyGame:
    pygame.init()
    # Создаем экземпляры классов.
    snake = Snake()
    apple = Apple()

    # Основная логика игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        apple.draw()
        object = snake.move(apple.position)
        snake.draw()
        if object == 'tail':
            """
            Если змейка наткнулась на свое тело, запускаем игру сначала.
            """
            snake.reset()
        if object:
            """
            Меняем позицию яблока, если оно съедено или происходит перезапуск
            игры (змейка наткнулась на свое тело).
            При перезапуске игры это нужно потому, что текущая позиция яблока
            может совпадать с центром экрана, откуда будет стартовать змейка.
            """
            apple.position = apple.randomize_position(snake.positions)
        pygame.display.update()


if __name__ == '__main__':
    main()
