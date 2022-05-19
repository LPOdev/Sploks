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
        list_c = crud.selectWithParams("contracts.id, CONCAT(customers.firstname, ' ', customers.lastname) as client, creationdate, plannedreturn, IF (effectivereturn is null, 0, 1) as returned",
            "contracts",
            "INNER JOIN customers ON customer_id = customers.id")
        
        contracts_list = list(list_c)

        contracts_list[0][0] = 456

        list_c = tuple(contracts_list)
        

        print(list_c)

        '''for c in list_c:
            contracts_list.append([c[0], c[1], Helpers.formatDate(c[2]), Helpers.formatDate(c[3]), c[4]])
            '''

        #print(contracts_list)