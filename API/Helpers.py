from translate import Translator

class Helpers(object):

    def translate_language(to_language, source, from_lnaguage = "en", status_translate=True):
        translator = Translator(from_lnag=from_lnaguage, to_lang=to_language)
        if (status_translate == False):
            return source
        translate = translator.translate(source)
        print("source = {0}".format(source))
        print("translate = {0}".format(translate))
        return translate
