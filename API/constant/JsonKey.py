
class JsonKey(object):
    ERRORS = "errors"
    COUNTRIES = "countries"
    USERPROFILE_ID = "userprofile_id"

    class UserProfile(object):
        ID = "id"
        LOGIN = "login"
        PASSWORD = "password"
        COUNTRY_ID = "country_id"

        COUNTRY = "country"

    class Countries(object):
        ID = "id"
        TITLE = "title"
        PREFIX = "prefix"

    class Types(object):
        ID = "id"
        TITLE = "title"
        EN_TITLE = "en_title"

    class Histories(object):
        ID = "id"
        USER_ID = "user_id"
        TYPE_ID = "type_id"
        DATE = "date"
        DESCRIPTION = "description"

        USER = "user"
        TYPE = "type"

    class Fact(object):
        NUMBER = "number"
        DESCRIPTION = "description"
        TYPE = "type"