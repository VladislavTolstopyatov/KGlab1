from tkinter import *

INSIDE = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 8  # 1000
TOP = 4   # 0100

x_max = 450
y_max = 450
x_min = 50
y_min = 50


def computeCode(x, y):
    code = INSIDE
    if x < x_min:  # слева от прямоугольника
        code |= LEFT
    elif x > x_max:  # справа от прямоугольника
        code |= RIGHT
    if y < y_min:  # снизу прямоугольника
        code |= BOTTOM
    elif y > y_max:  # сверху прямоугольника
        code |= TOP
    return code


def task():
    x1 = float(entry_x1.get())
    y1 = float(entry_y1.get())
    x2 = float(entry_x2.get())
    y2 = float(entry_y2.get())

    my_canvas.create_line(x1, y1, x2, y2, fill='red')
    my_canvas.grid(row=6, column=0)

    code1 = computeCode(x1, y1)
    code2 = computeCode(x2, y2)
    accept = False

    while True:

        # если обе конечные точки лежат внутри прямоугольника, ничего не делаем
        if code1 == 0 and code2 == 0:
            accept = True
            break

        # проверка что линия лежит ли вообще в прямоугольнике
        # ничего не делаем
        elif (code1 & code2) != 0:
            break

        # Некоторый сегмент находится внутри прямоугольника
        else:

            # Линию необходимо обрезать
            # По крайней мере, одна из точек находится снаружи
            x = 1.0
            y = 1.0
            # поиск точки которая за прямоугольником
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

                # поиск точки пересечения
            # по формуле y = y1 + наклон * (x - x1),
            # x = x1 + (1 / наклон) * (y - y1)
            if code_out & TOP:

                # точка находится над прямоугольником
                x = x1 + ((x2 - x1) / (y2 - y1)) * (y_max - y1)
                y = y_max

            elif code_out & BOTTOM:

                # точка находится под прямоугольником
                x = x1 + ((x2 - x1) / (y2 - y1)) * (y_min - y1)
                y = y_min

            elif code_out & RIGHT:

                # точка находится справа от прямоугольника
                y = y1 + ((y2 - y1) / (x2 - x1)) * (x_max - x1)
                x = x_max

            elif code_out & LEFT:

                # точка находится слева от прямоугольника
                y = y1 + ((y2 - y1) / (x2 - x1)) * (x_min - x1)
                x = x_min

                # Теперь найдена точка пересечения x, y
                # Заменяем точку за пределами  прямоугольника
                # на точку пересечения
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = computeCode(x1, y1)

            else:
                x2 = x
                y2 = y
                code2 = computeCode(x2, y2)

    if accept:
        print("Линия отрисована с %.2f, %.2f на %.2f, %.2f" % (x1, y1, x2, y2))
        my_canvas.create_line(x1, y1, x2, y2, fill='blue', width=1)
        my_canvas.grid(row=6, column=0)

    else:
        print("Линия вне прямоугольника")


my_window = Tk()
my_window.title("KG LAB1 TASK 21")

Label(my_window, text="Enter P1 x1 : ", fg="black", font="none 12").grid(row=1, column=0, sticky=W)
entry_x1 = Entry(my_window, width=20, bg="white")
entry_x1.grid(row=1, column=0)
Label(my_window, text="Enter P1 y1 : ", fg="black", font="none 12").grid(row=2, column=0, sticky=W)
entry_y1 = Entry(my_window, width=20, bg="white")
entry_y1.grid(row=2, column=0)
Label(my_window, text="Enter P2 x2 : ", fg="black", font="none 12").grid(row=3, column=0, sticky=W)
entry_x2 = Entry(my_window, width=20, bg="white")
entry_x2.grid(row=3, column=0)
Label(my_window, text="Enter P2 y2 : ", fg="black", font="none 12").grid(row=4, column=0, sticky=W)
entry_y2 = Entry(my_window, width=20, bg="white")
entry_y2.grid(row=4, column=0)

#   button
Button(my_window, text="Отсечь", width=6, command=task).grid(row=5, column=0)

#   canvas
my_canvas = Canvas(my_window, width=500, height=500)
my_canvas.grid(row=6, column=0)
my_canvas.create_line(x_min, x_max, x_max, x_max, fill='black')
my_canvas.create_line(x_max, x_min, x_max, x_max, fill='black')
my_canvas.create_line(x_min, x_min, x_min, x_max, fill='black')
my_canvas.create_line(x_min, x_min, x_max, x_min, fill='black')

my_window.mainloop()
