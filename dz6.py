from random import randint, choice, sample
from sympy import Symbol, simplify, SympifyError, solve, Function


class Specimen:
    '''
    Отдельная особь из 0 и 1 типа str
    '''

    def __init__(self, number: str | int, lenght=8) -> None:
        # Длина приводится к четному виду
        self.__lenght = lenght + 1 if lenght % 2 else lenght
        self.__pol_lenght = self.__lenght // 2
        # Бинарный вид либо передается явно, строкой, либо преобразуется из int
        if isinstance(number, int):
            self.__sample = f'{number:0{self.__lenght}b}'
        elif isinstance(number, str):
            self.__sample = number
        else:
            raise TypeError('Incorrect data type')

    def get_exemp(self):
        return self.__sample

    # Используем + для создания потомков
    def __add__(self, other):
        return (Specimen(self.__sample[:self.__pol_lenght] + other.__sample[self.__pol_lenght:], self.__lenght),
                Specimen(other.__sample[:self.__pol_lenght] + self.__sample[self.__pol_lenght:], self.__lenght))

    __str__ = get_exemp

    # Сравнение для sort
    def __lt__(self, other):
        return int(self.__sample, 2) < int(other.__sample, 2)

    def __eq__(self, other):
        return int(self.__sample, 2) == int(other.__sample, 2)


class Population:
    '''
    Список особей.\n
    Победитель в 0м слоте\n
    func иследуемая функция\n
    minimum=0, maximum=255 отрезок исследования\n
    metod='max' поиск максимума или минимума\n
    '''

    def __init__(self, func, minimum=0, maximum=255, size=12, metod='max') -> None:
        self.x = Symbol('x')
        self.__func = simplify(func)
        self.__minimum, self.__maximum = (
            minimum, maximum) if minimum < maximum else (maximum, minimum)
        self.__size = size
        self.__size_gen = int((size - 1) / 4 * 3)
        if self.__size_gen % 2:
           self.__size_gen += 1
        self.__metod = True if metod == 'max' else False
        self.__population = [self.__new_specimen() for _ in range(self.__size)]
        self.__population.sort(reverse=self.__metod, key=self.__func_from_bin)
    
    # Значение функции y по x(особи)
    def __func_from_bin(self, elem: Specimen):
        return self.__func.subs(self.x, self.__bin_to_int(str(elem)))

    # Новая популяция и определение победителя сортировкой по y
    def next_population(self):
        self.__population = self.__generation()
        self.__population.sort(reverse=self.__metod, key=self.__func_from_bin)

    # Создание новой популяции
    def __generation(self):
        new_population = []
        # Забираем предыдушего победителя
        new_population.append(self.__population.pop(0))
        # Создаем потомков из случайных 3/4 популяции
        new_population.extend(self.__birth(
            sample(self.__population, self.__size_gen)))
        # Добивем популяцию до нужного размера новосгенерированными особями
        new_population.extend([self.__new_specimen()
                              for _ in range(self.__size - len(new_population))])
        return new_population

    # Создание потомков
    def __birth(self, parents: list[Specimen]) -> list[Specimen]:
        children = []
        # Попарно создаем потомков
        for i in range(0, len(parents), 2):
            children.extend(parents[i] + parents[i + 1])
        # Оставляем особей входящих в заданный отрезок иследования
        sps = []
        for i in range(len(children)):
            if self.__minimum <= self.__bin_to_int(children[i].get_exemp()) <= self.__maximum:
                sps.append(children[i])
        return sps

    def get_winner(self):
        return self.__bin_to_int(str(self.__population[0]))

    def get_popul(self):
        return self.__population

    def __new_specimen(self):
        return Specimen(randint(self.__minimum, self.__maximum), len(self.__int_to_bin(self.__maximum)))

    def __int_to_bin(self, number):
        return f'{number:0b}'

    def __bin_to_int(self, bins: str):
        return int(bins, 2)

    def __repr__(self) -> str:
        out = ''
        for num, pop in enumerate(map(str, self.__population)):
            out += f"{num} bin: {pop} int: {self.__bin_to_int(pop)}\n"
        return f'{self.__func=}\n{self.__minimum=} {self.__maximum=}\n{self.__size=}\n{self.__size_gen=}\nself.__population\n{self.__metod=}\n{out}'
    
    def __str__(self) -> str:
        out = ''
        for num, pop in enumerate(map(str, self.__population)):
            out += f"Specimen {num} bin: {pop} int: {self.__bin_to_int(pop)}\n"
        return f'Function: {self.__func}\nRange: {self.__minimum} : {self.__maximum}\nSize population: {self.__size}\nPopulation:\n{out}'