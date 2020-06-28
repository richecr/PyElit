import os
import csv
import unicodedata

import truecase
from googletrans import Translator

import spacy
import geocoder

import nltk
from nltk.stem.porter import *

from .utils.utils import string_to_list


class Geoparsing:
    """
    Class responsible for performing Geoparsing.
    """

    def __init__(self):
        """
        Class constructor. Where all attributes are started
        and undergo pre-processing.
        """
        self.translator = Translator()
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp.Defaults.stop_words |= {
            "vamos", "olha", "pois", "tudo",
            "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui",
            "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá",
            "hoje", "aí", "ainda", "então", "vai", "porque", "moradores",
            "fazer", "prefeitura", "todo", "vamos", "problema", "fica", "ver",
            "tô"
        }
        self.stop_words_spacy = self.nlp.Defaults.stop_words
        self.residential = {}
        self.gazetteer = {}
        ROOT = os.path.abspath(os.path.dirname(__file__))
        fname = ROOT + "/gazetteer/processados"
        self.gazetteer_ln = csv.DictReader(
            open(fname + "/gazetteerpb.csv", "r", encoding='utf-8'))
        self.pre_process(self.gazetteer_ln)

    def pre_process(self, gazetteer):
        """
        Method that performs the pre-processing of the gazetteer.
        Loads the information fron the gazetteer into a dictionary.

        Params:
        ----------
        gazetteer: dict
            - Python native library object: `CSV`.
        """
        for row in gazetteer:
            self.gazetteer[self.remove_accents(row['osm_id'])] = (
                row['coordenates'],
                row['fclass'],
                self.remove_accents(row['name'].lower()),
                row['type']
            )

    def remove_accents(self, input_str):
        """
        Method that removes accents from words.

        Params:
        ----------
        input_str: String
            - Input to be removed the accents
        """
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode('utf-8')

    def concatena_end(self, list_end, exclude=False):
        """
        Method that concatenates addresses.

        Params:
        ----------
        list_end: List
            - List containing all addresses found.

        Return:
        ----------
        out : List
            - List of addresses concatenates.
        """
        if exclude:
            out = []
        else:
            out = [e for e in list_end]
        for i in range(len(list_end) - 1):
            for j in range(i+1, len(list_end)):
                temp = str(list_end[i]) + " " + str(list_end[j])
                out.append(temp)
        return out

    def verifica_endereco(self, end):
        """
        Method that check if an address is from Paraíba
        and whether its reliability is greater than or equal to 5.


        Params:
        ----------
        end: Dict
            - Dictionary containing all address information.

        Return:
        ----------
        True: If the address meets the requirements.
        False: otherwise
        """
        if (end['confidence'] >= 5):
            # ", campina grande" in end['address'].lower() and
            # if (", paraíba" in end['address'].lower()):
            return True
        else:
            return False

    def verfica(self, ents_loc, limit):
        """
        Method that checks if the addresses are correct.
            - Find the locations of the location entities.
            - Check if is from PB and your reliability(`verifica_endereco`).
            - Concatenates of addresses.
            - Sort addresses by reliability.

        Params:
        ----------
        ents_loc : List
             - List of locations entities.
        limit : Integer
            - Number of addresses you want to return.

        Return:
        ----------
        out : Tuple
            - One tuple of type (Boolean - List).
            If you have found at least one address in these requirements.
            List of addresses(len = limit))
        """
        ends = []
        for loc in ents_loc:
            loc = str(loc)
            g = geocoder.arcgis(loc)
            end = g.json
            if (end is not None):
                ends.append(end)

        ends_corretos = []
        for e in ends:
            if (self.verifica_endereco(e)):
                ends_corretos.append(e)

        if (len(ends_corretos)):
            end_final = ends_corretos[0]
            for ed in ends_corretos:
                if (ed['confidence'] > end_final['confidence']):
                    end_final = ed
            end_ = sorted(ends_corretos, key=lambda end: end['confidence'])
            return (True, end_[0:limit])
        else:
            return (False, [])

    def search_next_index(self, list_best_address):
        """
        Method that search a new position to be added
        in list of best addresses


        Params:
        ----------
        list_best_address : List
            - List containing all addresses found.

        Return:
        ----------
        out : Integer
            - Position where the new address must be added.
        """
        for i in range(len(list_best_address)):
            if list_best_address[i]['type_class'] == "geral":
                return i

        return len(list_best_address) - 1

    def insert_ordened_to_priority(self, result, address, type_):
        """
        Methodo that insert in list of best addresses order by priority.

        Params:
        ----------
        result : List
            - List of best addresses.
        address : Dict
            - Address to be insert in list.
        type_ : String
            - Type of address.
        """
        if address not in result:
            if type_ == "school":
                address['type_class'] = "school"
                result.insert(0, address)
            elif type_ == "residential":
                address['type_class'] = "residential"
                result.insert(self.search_next_index(result), address)
            else:
                address['type_class'] = "geral"
                result.append(address)

    def choose_best_addresses(self, adresses, text, addresses_, cities):
        """
        Method that performs the chose of the best addresses found.

        Algorithms implemented:
            - Sort by priority levels.
            - Filter by addresses that are in a certain neighborhood that is
            also in these filtered addresses.
            - Addresses that are more repeated in the text.
            - Addresses that are StreatName.
            - Addresses that are contained in the cities found in the text.

        Params:
        ----------
        adresses : Dict
            - Adddresses dictionary and its cordinates .
        text : String
            - Text that is going through geoparsing..
        addresses_ : List
            - List with all addresses concantenates with each other.
        cities : List
            - List of city names found.

        Return:
        ----------
        result : List
            - List of best addresses objects.
        """
        result = []
        for loc in adresses.keys():
            coord, type_ = adresses[loc]
            lat, lon = string_to_list(coord)
            loc_ = str(lat[0]) + ", " + str(lon[0])
            g = geocoder.reverse(location=loc_, provider="arcgis")
            g = g.json
            if g is not None:
                g['occurrences_in_text'] = text.count(loc)
                result.append(g)
                self.insert_ordened_to_priority(result, g, type_)

        result = sorted(result, key=lambda e: e['occurrences_in_text'])

        new_result = []
        for i in range(len(result) - 1, -1, -1):
            loc = result[i]
            if loc['raw'].__contains__('address'):
                loc_district = loc['raw']['address']['District'].lower()
                if loc_district in adresses.keys():
                    new_result.insert(0, loc)
                else:
                    new_result.append(loc)
            else:
                if loc['raw']['name'].lower() in adresses.keys():
                    new_result.insert(0, loc)
                else:
                    new_result.append(loc)
        result = new_result

        for loc in addresses_:
            loc_ = str(loc)
            g = geocoder.arcgis(loc_)
            end = g.json
            result.insert(0, end)

        new_result = []
        for i in range(len(result) - 1, -1, -1):
            if result[i].__contains__('quality'):
                if result[i]['quality'] == "StreetName":
                    new_result.insert(0, result[i])
                else:
                    new_result.append(result[i])
            else:
                new_result.append(result[i])

        result = new_result

        new_result = []
        if (cities != []):
            for i in range(len(result) - 1, -1, -1):
                for city in cities:
                    if result[i].__contains__('quality'):
                        if city in result[i]['address'].lower():
                            new_result.insert(0, result[i])
                    else:
                        loc_city = str(result[i]['raw']
                                       ['address']['City']).lower()
                        if loc_city == city:
                            new_result.insert(0, result[i])
            result = new_result

        return result

    def filterAddressCGText(self, text):
        """
        Method that performs the filtering of the text addresses
        that are in the gazetteer.

        Params:
        ----------
        text : String
            - Text that to performs the geoparsing..

        Return:
        ----------
        result : Dict
            - Addresses dictionary and its cordinates.
        """
        addresses_geral = {}

        text = self.remove_accents(text)

        for osm_id in self.gazetteer.keys():
            address = self.gazetteer.get(osm_id)[2]
            address_aux = address.split()
            if address_aux[0] == "rua":
                address_aux = address_aux[1:]
            if len(address_aux) > 1 or self.gazetteer[osm_id][1] == "suburb":
                address = address.replace("(", "")
                address = address.replace(")", "")
                txt_contains_addr = re.search("\\b" + address + "\\b", text)
                if txt_contains_addr:
                    addr_repeated = self.repeated_address(
                        addresses_geral.keys(), address)
                    if not addr_repeated:
                        addresses_geral[address] = (
                            self.gazetteer[osm_id][0],
                            self.gazetteer[osm_id][1])

        cities = [str(a) for a in addresses_geral.keys()
                  if addresses_geral[a][1] == "city"]

        addresses_ = [str(a) for a in addresses_geral.keys()]
        addresses_ = self.concatena_end(addresses_, exclude=True)
        result = self.choose_best_addresses(
            addresses_geral, text, addresses_, cities)
        return result

    def repeated_address(self, addresses, address):
        """
        Method that checks whether an address is repeated.

        Params:
        ----------
        addresses: List
            - List of addresses
        address: String
            - Address

        Return:
        ----------
        True: if the address is repeated.
        False: Otherwise.
        """
        for a in addresses:
            if address in a:
                return True
        return False

    def geoparsing(self, text, case_correct=False, limit=5,
                   gazetteer_cg=False):
        """
        Method that performs the geoparsing of text,

        NOTE: use the geoparsing without the correct case and withour
        the gazetteer will give you poor results.

        Params:
        ----------
        text : String
            - Text that to performs the geoparsing.
        case_correct: Bool
            - If the text is with correct case.
        limit: Int
            - Maximum limit of returned addresses.
        gazetteer_cg: Bool
            - If you want to use the gazetteer with locations in
            the state of Paraíba.

        Return:
        ----------
        result : List
            - List of addresses.
        """
        if gazetteer_cg:
            result = self.filterAddressCGText(text.lower())
            if result:
                return result
            else:
                raise Exception(
                    "Não foi possível realizar o geoparsing do texto")
        else:
            if case_correct:
                doc = self.nlp(text)
                ents_loc = list(filter(
                    lambda entity: entity.label_ == "LOC" or
                    entity.label_ == "GPE", doc.ents))
                address_found = self.concatena_end(ents_loc)
                result = self.verfica(address_found, limit)
                if result[0]:
                    return result[1]
                else:
                    raise Exception(
                        "Não foi possivel realizar o geoparsing do texto")
            else:
                text = truecase.get_true_case(text)

                text_en = self.translator.translate(text, dest="en")
                text_en = text_en.text
                text_true_case = truecase.get_true_case(text_en)

                text_pt = self.translator.translate(
                    text_true_case, src="en", dest="pt")
                text = text_pt.text

                doc = self.nlp(text)
                return self.geoparsing(text, case_correct=True)
