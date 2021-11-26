import re

class NameConverter:

    # converts to the format stored on database
    def convert_country_name(countryName):

        countryName = countryName.lower()
        countryName = countryName.strip()
        countryName = re.sub("dem[.]", "democratic", countryName)
        countryName = re.sub("repub[.]", "republic", countryName)
        countryName = re.sub("rep[.]", "republic", countryName)
        countryName = re.sub(r"\bthe\b", "", countryName)
        countryName = re.sub("of", "", countryName)
        countryName = re.sub("^dr ", "democratic republic ", countryName)
        countryName = re.sub("^st[.]? ", "saint ", countryName)
        countryName = re.sub("&", "and", countryName)
        countryName = re.sub("-", "_", countryName)
        countryName = re.sub("^u[.]?s[.]?a[.]?$", "united states", countryName)
        countryName = re.sub("^u.a.e[.]?$", "united arab emirates", countryName)
        countryName = re.sub("^u.k[.]?$", "united kingdom", countryName)
        countryName = re.sub("^congo$", "republic congo", countryName)
        countryName = re.sub("^sao tome$", "sao tome and principe", countryName)
        countryName = re.sub("^principe$", "sao tome and principe", countryName)
        countryName = re.sub("^tobago$", "trinidad and tobago", countryName)
        countryName = re.sub("^trinidad$", "trinidad and tobago", countryName)
        countryName = re.sub("^ivory coast$", "cote d'ivoire", countryName)

        output = ""
        components = re.split(",", countryName)
        if len(components) == 2:
            output = components[1].strip() + ' ' + components[0]
        else:
            output = components[0]
            
        output = re.sub("[\s]+", '_', output.strip())
        return output

    # conerts to the format presented to the user
    def convert_to_display_name(country_name):

        output = ""
        components = re.split("_", country_name)
        for component in components:
            output += component.capitalize() + " "
        
        #remove last whitespace introduced
        return output[:-1]
