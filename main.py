import os
import platform
import blessings


MAX_SHIP_SIZE = 4
NROWS = 10
COLUMNS = 'АБВГДЕЖЗИК'
EMPTY, SHIP, HIT, MISS, DEAD, CONTUR = ' SX/D0'
term = blessings.Terminal()
class TPoint:
    x = 0
    y = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, point):
        return self.x == point.x and self.x == point.x

    def incx(self,a = 1):
        return  TPoint(self.x + a,self.y)

    def incy(self,a = 1):
        return  TPoint(self.x ,self.y + a)
#****************************************************************************************************

class TShip:
    length = 0
    direction = ''
    hp = 0

    def __init__(self, plen, px, py, pdir):
        if plen > 4 :
            self.length = 4
        else:
            self.length = plen
        self.startpoint = TPoint(px,py)
        if pdir != 'V' and pdir != 'G' :
            self.direction = 'G'
        else:
            self.direction = pdir
        self.hp = self.length

    @property
    def points(self):
        result = [self.startpoint]
        for p in range(1, self.length):
            if self.direction == 'V':
                result.append(self.startpoint.incx(p))
            else:
                result.append(self.startpoint.incy(p))
        return result

    def match(self, shot):
        return shot in self.points
#****************************************************************************************************
    # И имеет методы:

   #     Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения).
   #     Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может).
   #     Метод, который выводит доску в консоль в зависимости от параметра hid.
   #     Метод out, который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False, если не выходит.
   #     Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения).
   #  raise ValueError("Тебе не может быть столько лет")
class TBoard:
    hidden = False
    ships_alive = 0
    cells = []
    def __init__(self):
                     # АБВГДЕЖЗИК
        self.cells = ['          ',  # 1
                      '          ',  # 2
                      '          ',  # 3
                      '          ',  # 4
                      '          ',  # 5
                      '          ',  # 6
                      '          ',  # 7
                      '          ',  # 8
                      '          ',  # 9
                      '          ']  # 10
        self.ships = []
        self.objects = []

    def add_ship(self, ship):
        for point in ship.points:
           if point.x > 10 or point.y > 10:
               print("Out of field!")
           elif point in self.objects:
               print("Out of field!")
           else:
               self.cells[point.x][point.y] = SHIP
               self.objects.append(point)
               self.ships.append(ship)

    @property
    def fieldcells(self):
        return self.cells

    def testf1(self):
        # АБВГДЕЖЗИК
        self.cells =   ['S         ',  # 1
                        '          ',  # 2
                        '   S    S ',  # 3
                        '          ',  # 4
                        '  S       ',  # 5
                        '        SS',  # 6
                        '          ',  # 7
                        'SS SS SSS ',  # 8
                        '          ',  # 9
                        '  SSS SSSS']  # 10

    def testf2(self):

        # АБВГДЕЖЗИК
        self.cells =   ['S  S      ',  # 1
                        '          ',  # 2
                        '   S    S ',  # 3
                        '   S  S   ',  # 4
                        '          ',  # 5
                        '  SSSS  SS',  # 6
                        '          ',  # 7
                        '      S   ',  # 8
                        '      S   ',  # 9
                        '  SSS S SS']  # 10

    def print(self):
        print('  '+COLUMNS)
        for i, row in enumerate(self.cells, start=1):
           print("{:2d}{}".format(i, ''.join(map(str, row))))





def board_display1(board, name):
    x = 0
    with term.location(x, 0):
        print(name + ':')
    with term.location(x, 1):
        print('  ' + COLUMNS)
        for i, row in enumerate(board, start=1):
            with term.location(x, i + 1):
                print("{:2d}{}".format(i, ''.join(map(str, row))))

def board_display2(board,  name):
    x =  20
    with term.location(x, 0):
        print(name + ':')
    with term.location(x, 1):
        print('  ' + COLUMNS)
        for i, row in enumerate(board, start=1):
            with term.location(x, i + 1):
                print("{:2d}{}".format(i, ''.join(map(str, row))))

if __name__ == '__main__':
    field = TBoard()
    field.testf1()
    board_display1(field.fieldcells,  'al')
    field.testf2()
    board_display2(field.fieldcells,  'al1')
