from model import crud


# The Item class is a class that represents an item in the store
class Item:

    def load(self, id):
        """
        It loads the data from the database into the object
        
        :param id: The id of the article
        """
        articleInfos = crud.selectOneWithParams(
            "items.id, itemnb, brand, model, size, gearstate_id, cost, returned, stock, articlenumber, geartype_id, geartypes.id as id_geartypes, name, uniqueitem",
            "items",
            f"INNER JOIN geartypes ON geartype_id = geartypes.id WHERE items.id = {id}")
        self.id = articleInfos['id']
        self.itemnb = articleInfos['itemnb']
        self.brand = articleInfos['brand']
        self.model = articleInfos['model']
        self.size = articleInfos['size']
        self.gear_state_id = articleInfos['gearstate_id']
        self.cost = articleInfos['cost']
        self.returned = articleInfos['returned']
        self.stock = articleInfos['stock']
        self.article_number = articleInfos['articlenumber']
        self.geartype_id = articleInfos['geartype_id']

        self.geartype = articleInfos['name']

    def save(self, values):
        """
        The save() function is used to save the current state of the object to the database
        
        :param values: A tuple of values to be inserted into the database
        """
        if self.id > 0:
            mysql_error = crud.updateOne("items", f"itemnb='{values[0]}',brand='{values[1]}',model='{values[2]}',size={values[3]}, gearstate_id={values[4]},cost={values[5]},returned={values[6]},stock={values[7]},articlenumber='{values[8]}',geartype_id={values[9]}", f"WHERE id = {self.id}")
            return mysql_error

        else:
            columns = "itemnb, brand, model, size, gearstate_id, cost, returned, stock, articlenumber, geartype_id"
            new_id = crud.createOne("items", f"{columns}", f"{values}")
            self.id = new_id

    def delete(self):
        """
        This function is used to delete an item from the items table in the database
        """
        crud.deleteFromTable("items", f"WHERE id = {self.id}")

    def contracts(self):
        """
        This function returns a list of contracts that have the item with the given id
        :return: A rented item.
        """
        return crud.selectDistinct(
            "contracts.id, customers.firstname, customers.lastname, contracts.creationdate, contracts.effectivereturn, CONCAT(helpers.firstname, ' ',helpers.lastname) as helpersFullname, CONCAT(staffs.firstname, ' ',staffs.lastname)",
            "items",
            f"INNER JOIN renteditems ON items.id = item_id INNER JOIN contracts ON contract_id = contracts.id INNER JOIN customers ON customer_id = customers.id INNER JOIN staffs AS helpers ON contracts.help_staff_id = helpers.id INNER JOIN staffs ON contracts.tune_staff_id = staffs.id WHERE items.id = {self.id}")

    def get_location_price(self, state, duration):
        result = crud.selectDistinct("*", "rentprices", 
        f"WHERE gearstate_id = {state} AND duration_id = {duration} AND geartype_id = {self.geartype_id}")
        return result


    @staticmethod
    def all():
        """
        This function returns all the items in the database
        :return: A list of dictionaries.
        """
        return crud.selectWithParams("items.id, articlenumber, brand, model, itemnb, size, name, stock",
                                     "items", "INNER JOIN geartypes ON geartypes.id = items.geartype_id")
    
    @staticmethod
    def allWithColumns(columns, params = ""):
        """
        This function returns all the items in the database
        :return: A list of dictionaries.
        """
        return crud.selectWithParams(columns, "items", f"INNER JOIN geartypes ON geartypes.id = items.geartype_id {params}")

    @staticmethod
    def getIdBySerialNumber(serial):
        """
        This function returns the id of the item with the given serial number
        
        :param serial: the serial number of the item
        :return: A list of dictionaries.
        """
        return crud.selectOneWithParams("id", "items", f"WHERE itemnb = {serial}")

    @staticmethod
    def destroy(id):
        """
        This function deletes an item from the items table
        
        :param id: The id of the item to be deleted
        """
        crud.deleteFromTable("items", f"WHERE id = {id}")

    @staticmethod
    def contratsOf(id):
        """
        This function returns a list of contracts that are associated with the item with the given id
        
        :param id: The id of the item you want to get the contracts of
        :return: A list of dictionaries, each dictionary representing a contract.
        """
        return crud.selectWithParams("*", "items",
                                     f"INNER JOIN renteditems ON items.id = item_id INNER JOIN contracts ON contract_id = contracts.id INNER JOIN customers ON customer_id = customers.id WHERE items.id = {id}")
