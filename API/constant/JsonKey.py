
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

    class Language(object):
        ID = "id"
        TITLE = "title"
        PREFIX = "prefix"

    class Cities(object):
        ID = "id"
        TITLE = "title"
        COUNTRY_CODE = "country_code"

    class Histories(object):
        ID = "id"
        USER_ID = "user_id"
        TYPE_ID = "type_id"
        DATE = "date"
        DESCRIPTION = "description"

        USER = "user"
        TYPE = "type"

    class Weather(object):
        ID = "id"
        TEMP = "description"
        CITY_NAME = "number"
        DESCRIPTION = "description"
        DATE = "date"