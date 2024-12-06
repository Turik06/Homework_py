from abc import ABC, abstractmethod


class ChessPiece(ABC):
    def __init__(self, horizontal, vertical, board=8):
        if horizontal not in 'abcdefgh':
            raise ValueError("Неверная координата по горизонтали")
        if vertical < 1 or vertical > 8:
            raise ValueError("Неверная координата по вертикали")
        self.horizontal = horizontal
        self.vertical = vertical
        self.board = board

    @abstractmethod
    def can_move(self, horizontal, vertical):
        pass


class King(ChessPiece):
    def __init__(self, horizontal, vertical, board=8):
        super().__init__(horizontal, vertical, board)

    def can_move(self, horizontal, vertical):
        horizontal_step = abs(ord(self.horizontal) - ord(horizontal))
        vertical_step = abs(self.vertical - vertical)
        return horizontal_step <= 1 and vertical_step <= 1


class Knight(ChessPiece):
    def __init__(self, horizontal, vertical, board=8):
        super().__init__(horizontal, vertical, board)

    def can_move(self, horizontal, vertical):
        horizontal_step = abs(ord(self.horizontal) - ord(horizontal))
        vertical_step = abs(self.vertical - vertical)
        return (horizontal_step == 2 and vertical_step == 1) or (horizontal_step == 1 and vertical_step == 2)


def print_board(king, knight):
    print("  a b c d e f g h")
    print("  ---------------")
    for i in range(8, 0, -1):
        row = f"{i} |"
        for j in 'abcdefgh':
            if king.horizontal == j and king.vertical == i:
                row += " K"
            elif knight.horizontal == j and knight.vertical == i:
                row += " N"
            else:
                row += " ."
        print(row)
    print()


def user_move(piece):
    move = input(f"Введите координаты для перемещения {piece.__class__.__name__} (например, 'f5'): ")
    if len(move) == 2 and move[0] in 'abcdefgh' and move[1] in '12345678':
        new_horizontal, new_vertical = move[0], int(move[1])
        if piece.can_move(new_horizontal, new_vertical):
            print(
                f"Фигура {piece.__class__.__name__} перемещена с {piece.horizontal}{piece.vertical} на {new_horizontal}{new_vertical}.")
            piece.horizontal, piece.vertical = new_horizontal, new_vertical
            return True
        else:
            print("Невозможный ход для данной фигуры. Попробуйте снова.")
            return False
    else:
        print("Неверный формат координат. Попробуйте снова.")
        return False


def make_move(king, knight):
    print_board(king, knight)
    piece_choice = input("Выберите фигуру (king/knight) или 'exit' для выхода: ").lower()
    if piece_choice == 'exit':
        print("Выход из игры.")
        return False
    elif piece_choice == 'king':
        if user_move(king):
            return True
    elif piece_choice == 'knight':
        if user_move(knight):
            return True
    else:
        print("Неверный выбор фигуры. Попробуйте снова.")
        return True

    return True


def main():
    print("Добро пожаловать в шахматную игру!")

    king = King('e', 4)  # Король на позиции e4
    knight = Knight('g', 6)  # Конь на позиции g6

    continue_game = True
    while continue_game:
        continue_game = make_move(king, knight)


main()
