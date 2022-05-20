from model import crud
from model.helpers import Helpers

# This class is used to load a contract from the database
class Contract:
    def load(self, id):
        """
        It takes an id as an argument, and returns a contract object
        
        :param id: The id of the contract
        """
        contract_infos = crud.selectOneWithParams(
            "contracts.id, creationdate, effectivereturn, lastname, firstname, address, npa, town, mobile, phone, email",
            "contracts",
            f"INNER JOIN customers ON customer_id = customers.id INNER JOIN npas ON npa_id = npas.id WHERE contracts.id = {id}")

        creation_date = Helpers.formatDate(contract_infos['creationdate'])
        return_date = Helpers.formatDate(contract_infos['effectivereturn'])

        self.id = contract_infos['id']
        self.creation_date = creation_date
        self.effective_return = return_date
        self.lastname = contract_infos['lastname']
        self.firstname = contract_infos['firstname']
        self.address = contract_infos['address']
        self.town = f"{contract_infos['npa']}, {contract_infos['town']}"
        self.mobile = contract_infos['mobile']
        self.phone = contract_infos['phone']
        self.email = contract_infos['email']

    @staticmethod
    def all():
        return crud.selectAll("contracts")

    @staticmethod
    def allWithParams():
        result = crud.selectWithParams("contracts.id, CONCAT(customers.firstname, ' ', customers.lastname) as client, creationdate, plannedreturn, effectivereturn",
            "contracts",
            "INNER JOIN customers ON customer_id = customers.id")

        
        contracts_list = []
        for r in result:
            created_on = r[2]
            planned_return = r[3]
            return_Date = r[4]

            if r[2] is not None:
                created_on = Helpers.removeHours(r[2])
            
            if r[3] is not None:
                planned_return = Helpers.removeHours(r[3])
            
            if r[4] is not None:
                return_Date = Helpers.removeHours(r[4])

            contracts_list.append([r[0], r[1], created_on, planned_return, return_Date])

        return contracts_list
        #return result