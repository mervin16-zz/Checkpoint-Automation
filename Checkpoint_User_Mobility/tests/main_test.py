import unittest
from models.user import User


class TestMain(unittest.TestCase):

    ##################################
    ###### password_generator() ######
    ##################################
    def test_password_generator(self):
        email = "jdoe@auchan.com"
        user = User(email, None, None)
        result = user.password
        print("*" * 50)
        print(result)
        print("*" * 50)

    ##################################
    ###### generate_user_name() ######
    ##################################
    def test_generate_username_veryShort(self):
        email = "jdo@auchan.com"
        user = User(email, None, None)
        expected_result = "jdo"
        result = user.name
        self.assertEqual(result, expected_result)

    def test_generate_username_short(self):
        email = "jdoel@auchan.com"
        user = User(email, None, None)
        expected_result = "jdoel"
        result = user.name
        self.assertEqual(result, expected_result)

    def test_generate_username_long(self):
        email = "nfullrick@auchan.com"
        user = User(email, None, None)
        expected_result = "nfullrick"
        result = user.name
        self.assertEqual(result, expected_result)

    def test_generate_username_veryLong(self):
        email = "clockerheartingale@auchan.com"
        user = User(email, None, None)
        expected_result = "clockerheartingale"
        result = user.name
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
