from model import crud

columns = "itemnb, brand, model, size, gearstate_id, cost, returned, stock, articlenumber, geartype_id"
id = crud.createOne("items", columns, "'test', 'test', 'test', 1, 1, 1, 1, 1, 'test', 1")

if id is not None and id > 0:
    result = "Success"
else:
    result = "Wrong"

print(f"Result:\t\t{result}")