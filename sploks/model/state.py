from model import crud

# The State class is a class that represents a state in a state machine
class State:

    def load(self, id):
        """
        This function loads a gear state from the database
        
        :param id: The id of the gear state
        """
        state = crud.selectOneWithParams("*", "gearstates", f"Where id = {id}")

        self.id = state['id']
        self.code = state['code']
        self.description = state['description']

    @staticmethod
    def all():
        """
        It returns all the gearstates in the database
        :return: A list of dictionaries.
        """
        return crud.selectWithParams("id, code, description", "gearstates")