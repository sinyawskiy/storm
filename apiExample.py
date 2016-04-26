__author__ = 'azernov'

from service import *
from data import *

if __name__ == "__main__":
    try:
        serverUrl = "http://localhost:8080"
        serverUrl = 'http://192.168.168.33:8080'
        authService = AuthenticationService(serverUrl)

        # Login
        # login = 'admin'
        # password = 'manager'
        
        login = 'portal'
        password = 'portal123'

        seanceType = SeanceType()
        seanceType.__setstate__({'name': u'EDITOR'})
        requisite = {u'crypt.key.id': u'', u'user.name': u'administrator', u'connection.type': seanceType}

        seance = authService.login(login, password, requisite)

        check = authService.checkUserSessionAvailable(login, password, requisite)
        print check
        authService.logoff(seance.id)
        check = authService.checkUserSessionAvailable(login, password, requisite)
        print check, '****************'

        dataService = DataService(serverUrl, (seance.id, seance.id))
        dictionaryService = DictionaryService(serverUrl, (seance.id, seance.id))

        # Retrieving structures
        structures = dataService.getStructures()

        if len(structures)> 0:
            first = structures[0]

            # Retrieving children
            sort = SortingField()
            sort.__setstate__({'name': u'NONE'})
            childrenTypes =['com.alee.archive3.api.data.Card']
            children = dataService.getTypedObjectChilds(first.objectId, childrenTypes, 0, 65535, sort)

            if len(children):
                firstCard = children[0]

                # Retrieving complete card
                complete = dataService.getCompleteCard(firstCard.objectId, True, None)

        # Performing attributive search
        searchService = SearchService(serverUrl, (seance.id, seance.id))

        matchType = MatchType()
        matchType.__setstate__({'name': u'CONTAINS'})

        fieldType = FieldType()
        fieldType.__setstate__({'name': u'ATTRIBUTE'})

        condition1 = AdvSearchableField()
        attributeId = 'ALSFR-dd118c3d-979d-48bc-97d2-ebcbb757f1a2'
        dictionaryRecordId = 'ALSFR-83e4152d-e951-4f0e-8d1b-9a014dfb5e0a'
        condition1.__setstate__(
            {'fieldType': fieldType, 'fieldName': attributeId, 'matchType': matchType, 'fieldConditions':[]}) #dictionaryRecordId

        request = SearchRequest()
        full_text_search = u'419703'
        request.__setstate__({'id': 'some_random_id', 'fieldList': [condition1], 'fileSearch': False, 'skipMissingAttributes': False,
                                'fullTxtSearch': full_text_search, 'sortingFields': None, 'sortOrder': 'asc'})

        # result = searchService.performSearch(request)

        # for item in result:
        #     print item.objectId
        #
        # sort = SortingField()
        # sort.__setstate__({'name': u'NONE'})
        #
        # childrenTypes = ['com.alee.archive3.api.data.Attribute']
        # attributes = dataService.getTypedObjectChilds(first.objectId, childrenTypes, 0, 65535, sort)

        dictionaryId = 'ALSFR-59dd86c7-3c08-4f4f-af03-ac9ff74c57e5'
        query = '195492295'
        result = dictionaryService.searchDictionaryChildrenByLikeName(dictionaryId, query)

        print result

        # Logging out
        authService.logoff(seance.id)

    except ProtocolError, v:
        print "ERROR", v