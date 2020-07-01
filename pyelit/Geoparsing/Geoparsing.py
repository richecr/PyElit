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

    def concantenate_address(self, list_address, exclude=False):
        """
        Method that concatenates addresses.

        Params:
        ----------
        list_address: List
            - List containing all addresses found.

        Return:
        ----------
        out : List
            - List of addresses concatenates.
        """
        if exclude:
            out = []
        else:
            out = [e for e in list_address]
        for i in range(len(list_address) - 1):
            for j in range(i+1, len(list_address)):
                temp = str(list_address[i]) + " " + str(list_address[j])
                out.append(temp)
        return out

    def check_reliability_address(self, address):
        """
        Method that check if an address is from Paraíba
        and whether its reliability is greater than or equal to 5.


        Params:
        ----------
        address: Dict
            - Dictionary containing all address information.

        Return:
        ----------
        True: If the address meets the requirements.
        False: otherwise
        """
        if (address['confidence'] >= 5):
            # ", campina grande" in end['address'].lower() and
            # if (", paraíba" in end['address'].lower()):
            return True
        else:
            return False

    def check_address(self, location_entities, limit):
        """
        Method that checks if the addresses are correct.
            - Find the locations of the location entities.
            - Check if is from PB and your reliability(`check_reliability_address`).
            - Concatenates of addresses.
            - Sort addresses by reliability.

        Params:
        ----------
        location_entities : List
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
        addresses = []
        for location in location_entities:
            location = str(location)
            g = geocoder.arcgis(location)
            address = g.json
            if (address is not None):
                addresses.append(address)

        correct_addresses = []
        for addr in addresses:
            if (self.check_reliability_address(addr)):
                correct_addresses.append(addr)

        if (len(correct_addresses)):
            addr_final = correct_addresses[0]
            for addr in correct_addresses:
                if (addr['confidence'] > addr_final['confidence']):
                    addr_final = addr
            addrs_ = sorted(correct_addresses,
                            key=lambda end: end['confidence'])
            return (True, addrs_[0:limit])
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
        for index in range(len(list_best_address)):
            if list_best_address[index]['type_class'] == "geral":
                return index

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

    def choose_best_addresses(self, adresses, text, addresses_concatenated, cities):
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
        addresses_concatenated : List
            - List with all addresses concatenated   with each other.
        cities : List
            - List of city names found.

        Return:
        ----------
        result : List
            - List of best addresses objects.
        """
        result = []
        for location in adresses.keys():
            coord, type_ = adresses[location]
            lat, lon = string_to_list(coord)
            location_ = str(lat[0]) + ", " + str(lon[0])
            addr = geocoder.reverse(location=location_, provider="arcgis")
            addr = addr.json
            if addr is not None:
                addr['occurrences_in_text'] = text.count(location)
                result.append(addr)
                self.insert_ordened_to_priority(result, addr, type_)

        result = sorted(result, key=lambda addr: addr['occurrences_in_text'])

        new_result = []
        for index in range(len(result) - 1, -1, -1):
            location = result[index]
            if location['raw'].__contains__('address'):
                location_district = location['raw']['address']['District'].lower(
                )
                if location_district in adresses.keys():
                    new_result.insert(0, location)
                else:
                    new_result.append(location)
            else:
                if location['raw']['name'].lower() in adresses.keys():
                    new_result.insert(0, location)
                else:
                    new_result.append(location)
        result = new_result

        for location in addresses_concatenated:
            location_ = str(location)
            addr = geocoder.arcgis(location_)
            addr = addr.json
            result.insert(0, addr)

        new_result = []
        for index in range(len(result) - 1, -1, -1):
            if result[index].__contains__('quality'):
                if result[index]['quality'] == "StreetName":
                    new_result.insert(0, result[index])
                else:
                    new_result.append(result[index])
            else:
                new_result.append(result[index])

        result = new_result

        new_result = []
        if (cities != []):
            for index in range(len(result) - 1, -1, -1):
                for city in cities:
                    if result[index].__contains__('quality'):
                        if city in result[index]['address'].lower():
                            new_result.insert(0, result[index])
                    else:
                        loc_city = str(result[index]['raw']
                                       ['address']['City']).lower()
                        if loc_city == city:
                            new_result.insert(0, result[index])
            result = new_result

        return result

    def filter_address_text(self, text):
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
        general_addresses = {}

        text = self.remove_accents(text)

        for osm_id in self.gazetteer.keys():
            address = self.gazetteer.get(osm_id)[2]
            auxiliary_address = address.split()
            if auxiliary_address[0] == "rua":
                auxiliary_address = auxiliary_address[1:]
            if len(auxiliary_address) > 1 or self.gazetteer[osm_id][1] == "suburb":
                address = address.replace("(", "")
                address = address.replace(")", "")
                txt_contains_addr = re.search("\\b" + address + "\\b", text)
                if txt_contains_addr:
                    addr_repeated = self.repeated_address(
                        general_addresses.keys(), address)
                    if not addr_repeated:
                        general_addresses[address] = (
                            self.gazetteer[osm_id][0],
                            self.gazetteer[osm_id][1])

        cities = [str(addr) for addr in general_addresses.keys()
                  if general_addresses[addr][1] == "city"]

        addresses_concatenated = [str(addr)
                                  for addr in general_addresses.keys()]
        addresses_concatenated = self.concantenate_address(
            addresses_concatenated, exclude=True)
        result = self.choose_best_addresses(
            general_addresses, text, addresses_concatenated, cities)
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
        for addr in addresses:
            if address in addr:
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
            result = self.filter_address_text(text.lower())
            if result:
                return result
            else:
                raise Exception(
                    "Text geoparsing could not be performed")
        else:
            if case_correct:
                doc = self.nlp(text)
                ents_loc = list(filter(
                    lambda entity: entity.label_ == "LOC" or
                    entity.label_ == "GPE", doc.ents))
                address_found = self.concantenate_address(ents_loc)
                result = self.check_address(address_found, limit)
                if result[0]:
                    return result[1]
                else:
                    raise Exception(
                        "Text geoparsing could not be performed")
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
