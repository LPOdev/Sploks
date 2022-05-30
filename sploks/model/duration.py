from model import crud

class Duration:
    @staticmethod
    def all():
        return crud.selectWithParams("*", "durations")
    
    @staticmethod
    def findId(code):
        return crud.selectOneWithParams("id","durations",f"WHERE code = '{code}'")