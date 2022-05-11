class GiveUp(Exception):
    """Вызывается, когда игрок хочет сдаться"""
    pass

class NotCorrectInput(Exception):
    """Вызывается, когда игрок неверные данные для хода"""
    pass