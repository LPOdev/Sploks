from model import crud

class Duration:

    def load(self, id):
        state = crud.selectOneWithParams("*", "gearstates", f"Where id = {id}")

        self.id = state['id']
        self.code = state['code']
        self.description = state['description']

    @staticmethod
    def all():
        return crud.selectWithParams("*", "durations")