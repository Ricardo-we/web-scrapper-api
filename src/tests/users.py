from utils.base.CRUDTest import CRUDTest
from utils.generic.Encrypter import Encrypter

object_schema = {"username": "Ricardo", "email": "totigamer2004@gmail.com", "password": "password"}
crud_test = CRUDTest("/users", object_schema)


def crud_tests():
    encrypted_password_response = {**object_schema, "password": Encrypter.encrypt(object_schema["password"])}
    created_item = crud_test.post(object_schema, encrypted_password_response)

    crud_test.get_one(created_item["id"])
    crud_test.get(created_item["id"])
    crud_test.put(created_item["id"], object_schema, encrypted_password_response)
    crud_test.delete(created_item["id"])


if __name__ == "__main__":
    crud_test()
