import os
import platform
from colorama import init, Style, Fore, Back
from random import randint

init()

COLUMNS = 'АБВГДЕЖЗИК'

EMPTY = Fore.YELLOW + "■" + Style.RESET_ALL
SHIP  = Fore.BLUE + "■" + Style.RESET_ALL
HIT   = Fore.RED + "■" + Style.RESET_ALL
MISS  = Fore.LIGHTBLACK_EX + "■" + Style.RESET_ALL
DEAD  = Fore.BLACK + "■" + Style.RESET_ALL

MESSAGEBOX = ["" for _ in range(10)]

def cls():
    if str(platform.system()) == "Windows" :
        os.system('CLS')
    else:
        os.system('clear')


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class ChordsException(BoardException):
    def __str__(self):
        return " Координаты не верны! "


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=10):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [[EMPTY] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    @property
    def shipslist(self):
        return self.ships

    @property
    def boardfield(self):
        return self.field

    @property
    def ishidden(self):
        return self.hid

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = SHIP
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = MISS
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += Fore.MAGENTA + "  А Б В Г Д Е Ж З И К" + Style.RESET_ALL
        for i, row in enumerate(self.field):
            if i + 1 > 9:
                res += Fore.MAGENTA +f"\n{i + 1}"+ Style.RESET_ALL + " ".join(row)
            else:
                res += Fore.MAGENTA +f"\n{i + 1} "+ Style.RESET_ALL + " ".join(row)

        if self.hid:
            res = res.replace(SHIP, EMPTY)
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = HIT
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    MESSAGEBOX.append("Корабль уничтожен!")
                    return False
                else:
                    MESSAGEBOX.append("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = MISS
        MESSAGEBOX.append("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as error:
                MESSAGEBOX.append(Fore.RED + str(error))
                return True

class AI(Player):
    def ask(self):
        seed = randint(0, 100)
        if seed < 70:
            d = Dot(randint(0, 5), randint(0, 5))
            MESSAGEBOX.append(f"Ход компьютера: {COLUMNS[d.y]} {d.x + 1}")
        else: # Make AI Great Agan!
            cheatdots = []
            for sh in self.enemy.shipslist:
                for dot in sh.dots:
                    cheatdots.append(dot)
            d = cheatdots[randint(0,len(cheatdots)-1)]
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").upper()
            for i, col in enumerate(COLUMNS):
                cords = cords.replace(col, str(i+1)+" ")
            cords = cords.split()

            if len(cords) != 2:
                raise ChordsException()

            y, x = cords

            if not (x.isdigit()) or not (y.isdigit()):
                raise ChordsException()

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=10):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.message = ""

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [4, 3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def printboards(self):
        enum1 = list(enumerate(self.us.board.boardfield))
        enum2 = list(enumerate(self.ai.board.boardfield))
        res = ""
        res += Fore.CYAN + "  Доска пользователя:     Доска компьютера:  " + Style.RESET_ALL
        res += Fore.MAGENTA + "\n  А Б В Г Д Е Ж З И К     А Б В Г Д Е Ж З И К" + Style.RESET_ALL
        for i in range(0,self.size):
            if i + 1 > 9:
                numstr = f"\n{i + 1}"
                numstr2 = f"{i + 1}"
            else:
                numstr = f"\n{i + 1} "
                numstr2 = f"{i + 1} "
            ( num1 ,row1)  = enum1[i]
            ( num2 ,row2)  = enum2[i]
            str1 = Fore.MAGENTA + numstr + Style.RESET_ALL + " ".join(row1)
            if self.us.board.ishidden:
                str1 = str1.replace(SHIP, EMPTY)
            str2 = Fore.MAGENTA + numstr2 + Style.RESET_ALL + " ".join(row2)
            if self.ai.board.ishidden:
                str2 = str2.replace(SHIP, EMPTY)
            res += str1 + "   " + str2 + "   " + Fore.GREEN + MESSAGEBOX[len(MESSAGEBOX)-self.size+i] + Style.RESET_ALL
        return res

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print("  формат ввода: А1 ")
        input("Нажмите 'Enter' ")
    def loop(self):
        num = 0
        while True:
            cls()
            print(self.printboards())
            if num % 2 == 0:
                MESSAGEBOX.append("Ходит пользователь!")
                repeat = self.us.move()
            else:
                MESSAGEBOX.append("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break
            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()



