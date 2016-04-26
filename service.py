__author__ = 'azernov'

from pyhessian.client import *
from pyDes import *


class AuthenticationService(object):
    key = [0x55, 0x01, 0x43, 0x3E, 0x1C, 0x7A, 0x72]

    def __init__(self, serverUrl):
        self.proxy = HessianProxy(serverUrl + "/ArchiveServer/transport/AuthenticationService", version=1)

    def checkUserSessionAvailable(self, login, password, requisite):
        return self.proxy.checkUserSessionAvailable_string_string_Requisite(login, self.encrypt(password), requisite)

    def login(self, login, password, requisite):
        return self.proxy.login_string_string_Requisite(login, self.encrypt(password), requisite)

    def logoff(self, seanceId):
        return self.proxy.logoff_string(seanceId)

    def encrypt(self, data):
        return '***' + base64.b64encode(des(self.test(self.key), padmode=PAD_PKCS5).encrypt(data))

    def test(self, sp):
        result = [0, 0, 0, 0, 0, 0, 0, 0]

        # Keeps track of the bit position in the result
        resultIx = 1

        # Used to keep track of the number of 1 bits in each 7-bit chunk
        bitCount = 0

        # Process each of the 56 bits
        i = 0
        while i < 56:
            # Get the bit at bit position i
            bit = ( sp[6 - i / 8] & ( 1 << ( i % 8 ) ) ) > 0

            # If set, set the corresponding bit in the result
            if bit:
                result[7 - resultIx / 8] |= ( 1 << ( resultIx % 8 ) ) & 0xFF
                bitCount += 1

            # Set the parity bit after every 7 bits
            if ( i + 1 ) % 7 == 0:
                if bitCount % 2 == 0:
                    # Set low-order bit (parity bit) if bit count is even
                    result[7 - resultIx / 8] |= 1
                resultIx += 1
                bitCount = 0
            resultIx += 1
            i += 1
        return bytearray(result).__str__()


class DataService(object):
    def __init__(self, serverUrl, credentials):
        self.proxy = HessianProxy(serverUrl + "/ArchiveServer/transport/DataService", credentials, version=1)

    def getStructures(self):
        return self.proxy.getStructures()

    def getTypedObjectChilds(self, parent, types, first, count, sortBy):
        return self.proxy.getTypedObjectChilds_string_List_int_int_SortingField(parent, types, first, count, sortBy)

    def getCompleteCard(self, cardId, isLoadFiles, attributeIds):
        return self.proxy.getCompleteCard_string_boolean_Collection(cardId, isLoadFiles, attributeIds)

    # def getCompleteCards(self, isLoadFiles, mergeAttributes, attributeIds, cardIds):
    #     return self.proxy.getCompleteCards_boolean_boolean_Collection_Collection(isLoadFiles, mergeAttributes, attributeIds, cardIds)

    def getDictionaryStorageRoot(self):
        return self.proxy.getDictionaryStorageRoot()

class SearchService(object):
    def __init__(self, serverUrl, credentials):
        self.proxy = HessianProxy(serverUrl + "/ArchiveServer/transport/SearchService", credentials, version=1)

    def performSearch(self, request):
        return self.proxy.performSearch_SearchRequest(request)


class AttributeService(object):
    def __init__(self, serverUrl, credentials):
        self.proxy = HessianProxy(serverUrl + "/ArchiveServer/transport/AttributeService", credentials, version=1)

    def getAttributeValuesForAnObject(self, cardId, aggregateAttributes=False, attributesIds=[]):
        return self.proxy.getAttributeValuesForAnObject(cardId, aggregateAttributes, attributesIds)

    def getAvailableAttributes(self):
        return self.proxy.getAvailableAttributes()


class DictionaryService(object):
    def __init__(self, serverUrl, credentials):
        self.proxy = HessianProxy(serverUrl + "/ArchiveServer/transport/DictionaryService", credentials, version=1)

    def searchDictionaryChildrenByLikeName(self, dictionaryId, likeName):
        return self.proxy.searchDictionaryChildrenByLikeName_string_string(dictionaryId, likeName)