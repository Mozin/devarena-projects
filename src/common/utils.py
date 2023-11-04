from passlib.hash import pbkdf2_sha512

class Utils(object):
    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: an encrypted password
        """
        return pbkdf2_sha512.hash(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password user sent matches with that in the DB
        :param password: sha512-based password
        :param hashed_password: encrypted password
        :return: True if password match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)


    @staticmethod
    def check_required_keys_present(request_dict, required_keys):
        request_dict_keys = list(request_dict.keys())
        missing_keys = [x for x in required_keys if not x in request_dict_keys]
        return len(missing_keys) == 0
