from model import crud

# Staff is a class that defines the attributes of a staff member
class Staff:

    def load(self, id):
        """
        This function loads a staff member from the database
        
        :param id: The id of the staff member
        """
        staff_member = crud.selectOneWithParams("*", "staffs", f"Where id = {id}")

        self.id = staff_member['id']
        self.firstname = staff_member['firstname']
        self.lastname = staff_member['lastname']
        self.phone = staff_member['phone']

    def save(self, values):
        """
        This function is used to save the staff object to the database
        
        :param values: The values to be inserted into the database
        """
        if self.id > 0:
            crud.updateOne("staffs", f"{values}", f"WHERE id = {self.id}")
        else:
            columns = "firstname, lastname, phone"
            new_id = crud.createOne("staffs", f"{columns}", f"{values}")
            self.id = new_id

    def delete(self):
        """
        This function is used to delete a row from the staffs table
        """
        crud.deleteFromTable("staffs", f"WHERE id = {self.id}")

    @staticmethod
    def all():
        """
        This function returns all the staffs in the staffs table
        :return: A list of dictionaries.
        """
        return crud.selectWithParams("firstname, lastname, phone", "staffs")

    @staticmethod
    def destroy(id):
        """
        This function deletes a row from the staffs table
        
        :param id: The id of the staff you want to delete
        """
        crud.deleteFromTable("staffs", f"WHERE id = {id}")