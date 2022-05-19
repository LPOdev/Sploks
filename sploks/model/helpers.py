import datetime


# This class contains a set of helper functions that are used by the other classes
class Helpers:

    @staticmethod
    def formatDate(date):
        """
        Converts a date from the sqlite database into a string that can be used in the html template
        
        :param date: The date you want to convert
        :return: A list of dictionaries. Each dictionary contains the information for a single question.
        """
        if date is None:
            return None
        else:
            date_sql = '%Y-%m-%d %H:%M:%S'
            date = datetime.datetime.strptime(str(date), date_sql)
            return date.strftime("%d %B %Y")
