from model import crud

class Duration:
    @staticmethod
    def all():
        """
        It returns all the rows from the durations table
        :return: A list of dictionaries.
        """
        return crud.selectWithParams("*", "durations")
    
    @staticmethod
    def findId(code):
        """
        It takes a code as a parameter, and returns the id of the duration that has that code
        
        :param code: The code of the duration
        :return: A list of tuples.
        """
        return crud.selectOneWithParams("id","durations",f"WHERE code = '{code}'")