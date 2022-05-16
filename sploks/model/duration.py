from model import crud

class Duration:
    @staticmethod
    def all():
        return crud.selectWithParams("*", "durations")