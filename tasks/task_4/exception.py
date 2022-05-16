class GiveUp(Exception):
    """Вызывается, когда игрок хочет сдаться"""
    pass

class NotCorrectInput(Exception):
    """Вызывается, когда игрок неверные данные для хода"""
    pass

class FigureOnWay(Exception):
    """Вызывается, когда на пути стоит препятствие в виде союзной фигуры"""
    pass