from const import con
from model import crud


# The Customer class is a blueprint for a customer object
class Customer:
    def load(self, id):
        """
        The function loads the data of a customer with the given id
        
        :param id: The id of the customer
        """
        data = crud.selectOneWithParams(
            "npas.id as id_npa, npa, town, customers.id, lastname, firstname, address, phone, email, mobile, npa_id",
            "npas", f"INNER JOIN customers ON customers.npa_id = npas.id WHERE customers.id = {id}")
        self.id = data['id']
        self.lastname = data['lastname']
        self.firstname = data['firstname']
        self.address = data['address']
        self.npa = data['npa']
        self.town = data['town']
        self.phone = data['phone']
        self.email = data['email']
        self.mobile = data['mobile']

    def save(self, values):
        """
        If the customer has an id, update the customer's information. If the customer doesn't have an
        id, create a new customer
        
        :param values: The values to be saved
        """
        if self.id > 0:
            crud.updateOne("customers", f"{values}", f"WHERE id = {self.id}")
        else:
            columns = "lastname, firstname, address, phone, email, mobile, npa_id"
            new_id = crud.createOne("customers", f"{columns}", f"{values}")
            self.id = new_id

    def delete(self):
        """
        Delete a row from the customers table in the database
        """
        crud.deleteFromTable("customers", f"WHERE id = {self.id}")

    def contracts(self):
        """
        This function returns a list of contracts that are associated with the customer.
        :return: A list of dictionaries with the following keys:
            id, creationdate, effectivereturn, notes, total, insurance, helpersFullname, staffsFullname
        """
        return crud.selectDistinct(
            "contracts.id, creationdate, effectivereturn, notes, total, insurance, CONCAT(helpers.firstname, ' ',helpers.lastname) as helpersFullname, CONCAT(staffs.firstname, ' ',staffs.lastname)",
            "contracts",
            f"INNER JOIN customers ON customer_id = customers.id INNER JOIN staffs AS helpers ON helpers.id = help_staff_id INNER JOIN staffs ON staffs.id = tune_staff_id WHERE customers.id = {self.id}")

    ### Static methods ###
    @staticmethod
    def all():
        """
        It returns all the customers in the database
        :return: A list of dictionaries.
        """
        return crud.selectWithParams("customers.id, lastname, firstname, address, npa, town, phone, email, mobile",
                                     "customers", "INNER JOIN npas ON npa_id = npas.id")

    @staticmethod
    def destroy(id):
        """
        This function deletes a row from the customers table
        
        :param id: The id of the customer to be deleted
        """
        crud.deleteFromTable("customers", f"WHERE id = {id}")

    @staticmethod
    def contractsOf(id):
        """
        This function returns all contracts of a customer with the given id
        
        :param id: The id of the customer you want to get the contracts of
        :return: A list of dictionaries.
        """
        return crud.selectWithParams("*", "contracts",
                                     f"INNER JOIN customers ON customer_id = customers.id WHERE customers.id = {id}")
