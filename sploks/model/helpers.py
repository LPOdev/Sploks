import datetime
import locale
locale.setlocale(locale.LC_TIME, "fr_FR") # Français


# This class contains a set of helper functions that are used by the other classes
class Helpers:
    global date_sql
    date_sql = '%Y-%m-%d %H:%M:%S'

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
            date = datetime.datetime.strptime(str(date), date_sql)
            return date.strftime("%d %B %Y")
    
    @staticmethod
    def removeHours(date):
        """
        It takes a date in the format of 'YYYY-MM-DD HH:MM:SS' and returns it in the format of
        'DD.MM.YYYY'
        
        :param date: the date to be converted
        :return: A string
        """
        if date is None:
            return None
        else:
            date_sql = '%Y-%m-%d %H:%M:%S'
            date = datetime.datetime.strptime(str(date), date_sql)
            return date.strftime("%d.%m.%Y")

    @staticmethod
    def dateToSQL(date):
        """
        It takes a date in the format dd.mm.yyyy and returns it in the format yyyy-mm-dd
        
        :param date: the date in the format dd.mm.yyyy
        :return: The date in the format of the date_sql variable.
        """
        if date is None:
            return None
        else:
            
            date = datetime.datetime.strptime(str(date),"%d.%m.%Y")
            return date.strftime(date_sql)