from random import randint
'''В текущем модуле реализована основная логика игры.'''

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
    """Класс GameObject - игровые объекты

    Служит для описания общих атрибутов и методов объектов,
    которые используются в игре.
    """

    def __init__(self) -> None:
        """Метод инициализирует начальную позицию и цвет объектов."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT) // 2)
        self.body_color = None

    def draw(self):
        """Метод отрисовки объектов

        Этот метод определяет, как объект будет отрисовываться на экране.
        Для каждого дочернего класса объектов игры метод переопределяется.
        """


class Apple(GameObject):
    """Класс Apple описывает объект яблоко."""

    def __init__(self):
        """Метод инициализации яблока

        Переинициализирует начальную позицию яблока, с учетом
        стартовой позиции змейки. Задает цвет яблока.
        """
        super().__init__()
        self.randomize_position(self.position)
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод отрисовывает яблоко в виде окружности."""
        center = (self.position[0] + 10, self.position[1] + 10)
        pygame.draw.circle(screen, self.body_color, center, (GRID_SIZE) // 2)
        pygame.draw.circle(screen, BORDER_COLOR, center, (GRID_SIZE) // 2, 1)

    def randomize_position(self, positions):
        """Метод определяет положение яблока.

        Метод случайным образом выбирает новую позицию яблока так,чтобы
        она не совпала с текущим положением змейки.
        То есть после выбора нового положения яблока, проверяется, не совпало
        ли оно с какой-либо точкой из тела змейки. Если совпало, то выбирается
        другое случайное значение. И так продолжается, пока новое положение
        яблока не окажется вне тела змейки.
        """
        while True:
            point = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                     randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if point not in positions:
                self.position = point
                break


class Snake(GameObject):
    """Класс nake описывает объект змейка."""

    def __init__(self):
        """Метод инициализации змейки.

        Метод переинициализирует начальную позицию змейки в центре экрана.
        Задает цвет тела змейки. Дополнительно добавляет цвета головы и глаз
        змейки, начальное направление движения.
        Атрибут next_direction - используется как следующее направление
        движения. В начале, следующее направление движения задается как None,
        в дальнейшем оно определяется в методе handle_keys.
        Атрибут last - используется для хранения позиции последнего сегмента
        змейки перед тем, как он исчезнет (при движении змейки). Это
        необходимо для «стирания» этого сегмента с игрового поля, чтобы змейка
        визуально двигалась.
        Атрибут lenghth хранит длину змейки. Начальное значение 1.
        """
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.head_color = SNAKE_HEAD_COLOR
        self.eyes_color = SNAKE_EYES_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.lenghth = 1
        self.positions = [self.position]

    def update_direction(self):
        """Метод update_direction обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод move обновляет позицию змейки.

        А именно:
        - Добавляется новая голова в начало списка positions.
        - Если змейка не съела яблоко (длина змейки не превышает значения
           атрибута length), то удаляется последний элемент тела
          змейки.
        """
        head_x, head_y = self.get_head_position()
        direct_x, direct_y = self.direction
        new_width = (head_x + direct_x * GRID_SIZE) % SCREEN_WIDTH
        new_height = (head_y + direct_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_width, new_height))
        if len(self.positions) > self.lenghth:
            self.last = self.positions[-1]
            self.positions.pop()

    def get_head_position(self):
        """Метод получает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод запускает игру сначала

        Змейка возвращается в исходное состояние.
        """
        self.__init__()

    def draw(self):
        """Метод отрисовывает змейку."""
        # Отрисовка змейки не включая головы
        # Поскольку изображение головы отличается от остального
        # туловища, при смещении змейки, нужно затереть исходную
        # голову (после смещения, она будет на позиции 1 списка)
        for position in self.positions[1:2]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_x, head_y = self.positions[0]
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.head_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        left_eye = (head_x + 5, head_y + 5)
        pygame.draw.circle(screen, self.eyes_color, left_eye, 2)
        right_eye = (head_x + 15, head_y + 5)
        pygame.draw.circle(screen, self.eyes_color, right_eye, 2)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Метод handle_keys определяет дальнейшее направление движения змейки.

    Направление определяется в зависимости от кнопки, которую нажимает игрок.
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
    """В теле функции записан основной исполняющий модуль

    Используется, чтобы код из нее не запускался из внешних
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
        snake.move()
        # Если змейка наткнулась на свое тело, запускаем игру сначала.
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
        # Меняем позицию яблока, если оно съедено
        # и увеличиваем длину змейки
        elif head == apple.position:
            apple.randomize_position(snake.positions)
            snake.lenghth += 1
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
