from model import crud
from model.helpers import Helpers

# This class is used to load a contract from the database
class Contract:
    def load(self, id):
        """
        It takes an id as an argument, and returns a contract object
        
        :param id: The id of the contract
        """
        contract_infos = crud.selectOneById("*", "contracts", id)

        creation_date = Helpers.formatDate(contract_infos['creationdate'])
        return_date = Helpers.formatDate(contract_infos['effectivereturn'])
        planned_return = Helpers.formatDate(contract_infos['plannedreturn'])

        self.id = contract_infos['id']
        self.creation_date = creation_date
        self.effective_return = return_date
        self.planned_return = planned_return
        self.customer_id = contract_infos['customer_id']
        self.notes = contract_infos['notes']
        self.total = contract_infos['total']
        self.takenon = Helpers.formatDate(contract_infos['takenon'])
        self.paidon = Helpers.formatDate(contract_infos['paidon'])
        self.help_staff = contract_infos['help_staff_id']
        self.tune_staff = contract_infos['tune_staff_id']

    
    def create(self, values):
        """
        It creates a new contract in the database and then loads it into the program
        
        :param values: ('2020-01-01', '2020-01-02', '1', '', '0', '2020-01-01', '2020-01-01', '1', '1')
        """
        columns = "creationdate, plannedreturn, customer_id, notes, total, takenon, paidon, help_staff_id, tune_staff_id"

        new_id = crud.createOne("contracts", columns, values)
        #print(new_id)
        self.load(new_id)

    @staticmethod
    def all():
        """
        It returns all the rows from the contracts table
        :return: A list of dictionaries.
        """
        return crud.selectAll("contracts")

    @staticmethod
    def allWithParams():
        """
        It takes a query, executes it, and then returns a list of lists
        :return: A list of lists.
        """
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