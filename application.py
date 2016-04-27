# -*- coding: utf-8 -*-
from service import *
from data import *
from flask import Flask, jsonify, render_template


class StormConnect():
    def __init__(self, *args, **kwargs):
        self.storm_is_load = False
        self.serverUrl = 'http://192.168.168.33:8080'
        self.login = 'portal'
        self.password = 'portal123'
        self.session = None
        seanceType = SeanceType()
        seanceType.__setstate__({'name': u'EDITOR'})
        self.requisite = {u'crypt.key.id': u'', u'user.name': u'administrator', u'connection.type': seanceType}
        self.services = {
            'auth': AuthenticationService(self.serverUrl),
            'data': None,
            'dictionary': None,
            'search': None,
            'attribute': None
        }
        self.authenticate()

        self.attributes = {}
        for attr in self.getService('attribute').getAvailableAttributes():
            self.attributes[attr.objectId] = attr.name
        self.dictionaries = {}

        dataService = self.getService('data')
        dictionaryRoot = dataService.getDictionaryStorageRoot()
        childrenTypes =['com.alee.archive3.api.data.Dictionary']
        sort = SortingField()
        sort.__setstate__({'name': u'NONE'})
        dictionaries = dataService.getTypedObjectChilds(dictionaryRoot.objectId, childrenTypes, 0, 65535, sort)
        for dictionary in dictionaries:
            self.dictionaries[dictionary.objectId] = dictionary.name
        self.storm_is_load = True

    def authenticate(self):
        self.session = self.services['auth'].login(self.login, self.password, self.requisite)
        self.services['data'] = DataService(self.serverUrl, (self.session.id, self.session.id))
        self.services['dictionary'] = DictionaryService(self.serverUrl, (self.session.id, self.session.id))
        self.services['search'] = SearchService(self.serverUrl, (self.session.id, self.session.id))
        self.services['attribute'] = AttributeService(self.serverUrl, (self.session.id, self.session.id))
        print 'Connect to STOR-M3 - session:', self.session.id

    def getService(self, service_name):
        if self.session and not self.services['auth'].checkUserSessionAvailable(self.login, self.password, self.requisite):
            try:
                print 'STOR-M3 disconnected.'
                self.authenticate()
            except ProtocolError, error:
                print error
        try:
            return self.services[service_name]
        except KeyError:
            return None

    def get_dict_value(self, dict, key):
        try:
            return dict[key]
        except KeyError:
            return None

    def get_dict_key(self, dict, value):
        for attrId, attrName in dict.iteritems():
            if attrName == value:
                return attrId
        return None

    def get_attribute(self, attr_id):
        return self.get_dict_value(self.attributes, attr_id)

    def get_attribute_id(self, value):
        return self.get_dict_key(self.attributes, value)

    def get_attribute_ids(self, attribute_names):
        result = []
        for attribute_name in attribute_names:
            attributeId = app.storm.get_attribute_id(attribute_name)
            if attributeId:
                result.append(attributeId)
        return result

    def get_dictionary(self, attr_id):
        return self.get_dict_value(self.dictionaries, attr_id)

    def get_dictionary_id(self, value):
        return self.get_dict_key(self.dictionaries, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session:
            self.getService('auth').logoff(self.session.id)


class CustomFlask(Flask):
    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False):
        stormConnect = StormConnect()
        self.storm = stormConnect.__enter__()
        super(CustomFlask, self).__init__(import_name, static_path, static_url_path, static_folder, template_folder, instance_path, instance_relative_config)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.storm:
            self.storm.__exit__(exc_type, exc_val, exc_tb)

app = CustomFlask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template('test.html')

@app.route("/search/<query>")
def search(query):
    dictionaryId = app.storm.get_dictionary_id(u'Площадки')
    cardAttributes = []
    buildAttributeId = app.storm.get_attribute_id(u'Площадка')
    if buildAttributeId:
        cardAttributes.append(buildAttributeId)
    yearAttributeId = app.storm.get_attribute_id(u'Год')
    if yearAttributeId:
        cardAttributes.append(yearAttributeId)
    typeAttributeId = app.storm.get_attribute_id(u'Тип документа')
    if typeAttributeId:
        cardAttributes.append(typeAttributeId)
    titleAttributeId = app.storm.get_attribute_id(u'Название проекта')
    if titleAttributeId:
        cardAttributes.append(titleAttributeId)

    result = {}
    if dictionaryId and buildAttributeId:
        try:
            dictionaryRecords = app.storm.getService('dictionary').searchDictionaryChildrenByLikeName(dictionaryId, query)

            for dictionaryRecord in dictionaryRecords:
                matchType = MatchType()
                matchType.__setstate__({'name': u'CONTAINS'})

                fieldType = FieldType()
                fieldType.__setstate__({'name': u'ATTRIBUTE'})

                condition1 = AdvSearchableField()

                condition1.__setstate__({
                    'fieldType': fieldType,
                    'fieldName': buildAttributeId,
                    'matchType': matchType,
                    'fieldConditions': [dictionaryRecord.objectId],
                })

                request = SearchRequest()
                request.__setstate__({
                    'id': 'some_random_id',
                    'fieldList': [condition1],
                    'fileSearch': False,
                    'skipMissingAttributes': False,
                    'fullTxtSearch': u'',
                    'sortingFields': None,
                    'sortOrder': 'asc'
                })

                search_result = app.storm.getService('search').performSearch(request)

                if len(search_result):
                    cards = []
                    for search_card in search_result:
                        card = app.storm.getService('data').getCompleteCard(search_card.objectId, True, cardAttributes)
                        cards.append({'id': search_card.objectId, 'card': card, 'name': search_card.name})

                    card_result = {}
                    for card_item in cards:
                        card = card_item['card']
                        card_id = card_item['id']
                        # build=None
                        # build_id=None
                        year=None
                        year_id=None
                        doc_type=None
                        doc_type_id=None
                        title=None

                        for attr in card.attributes:
                            # if attr.attributeId == buildAttributeId:
                            #     build = attr.doubleValue or attr.integerValue or attr.stringValue
                            #     build_id = attr.value
                            if attr.attributeId == yearAttributeId:
                                year = attr.doubleValue or attr.integerValue or attr.stringValue
                                year_id = attr.value
                            if attr.attributeId == typeAttributeId:
                                doc_type = attr.doubleValue or attr.integerValue or attr.stringValue
                                doc_type_id = attr.value
                            if attr.attributeId == titleAttributeId:
                                title = card_item['name']#, attr.doubleValue or attr.integerValue or attr.stringValue)

                        # try:
                        #     card_result[build_id]['count'] += 1
                        # except KeyError:
                        #     card_result[build_id] = {
                        #         'title': build,
                        #         'count': 1
                        #     }

                        try:
                            card_result[doc_type_id]['count'] += 1
                        except KeyError:
                            card_result[doc_type_id] = {
                                'title': doc_type,
                                'count': 1
                            }

                        try:
                            card_result[doc_type_id][year_id]['count'] += 1
                        except KeyError:
                            card_result[doc_type_id][year_id] = {
                                'title': year,
                                'count': 1
                            }

                        try:
                            card_result[doc_type_id][year_id][card_id]['count'] += 1
                        except KeyError:
                            card_result[doc_type_id][year_id][card_id] = {
                                'title': title,
                                'count': 1,
                            }

                        try:
                            card_result[doc_type_id][year_id][card_id]['files'].extend([{
                                'name': doc.name,
                                'url': doc.documentURL,
                                'id': doc.objectId
                            } for doc in card.documents])
                        except KeyError:
                            card_result[doc_type_id][year_id][card_id]['files'] = [{
                                'name': doc.name,
                                'url': doc.documentURL,
                                'id': doc.objectId
                            } for doc in card.documents]

                    result[dictionaryRecord.objectId] = {
                        'title': u'%s' % dictionaryRecord.name,
                        'cards': card_result
                    }

        except Exception, err:
            print err

    finish_result = []
    for build_item in result:
        card_types = []
        finish_result.append({
            'data': {
                'title': result[build_item]['title'],
                'icon': '/static/img/icons.png',
                'attributes': {}
            },
            'children': card_types
        })
        for item_type in result[build_item]['cards']:
            card_years = []
            if item_type not in ['count', 'title']:
                card_types.append({
                    'data': {
                        'title': result[build_item]['cards'][item_type]['title'],
                        'icon': '/static/img/icons.png',
                        'attributes': {}
                    },
                    'children': card_years
                })
                for item_year in result[build_item]['cards'][item_type]:
                    card_documents = []
                    if item_year not in ['count', 'title']:
                        card_years.append({
                            'data': {
                                'title': result[build_item]['cards'][item_type][item_year]['title'],
                                'icon': '/static/img/icons.png',
                                'attributes': {}
                            },
                            'children': card_documents
                        })
                        for item_document in result[build_item]['cards'][item_type][item_year]:
                            if item_document not in ['count', 'title']:
                                card_documents.append({
                                    'data': {
                                        'title': result[build_item]['cards'][item_type][item_year][item_document]['title'],
                                        'icon': '/static/img/icons.png',
                                        'attributes': {
                                            'href': '#',
                                            'onclick': "apex.StromTree.click_document('%s'); return false;" % item_document,
                                            'data-files': len(result[build_item]['cards'][item_type][item_year][item_document]['files'])
                                        }
                                    }
                                })

    return jsonify({'data': finish_result})


# @app.route("/root/")
# def root():
#     structures = app.storm.getService('data').getStructures()
#     result = ''
#     if len(structures) > 0:
#         first = structures[0]
#
#         # Retrieving children
#         sort = SortingField()
#         sort.__setstate__({'name': u'NONE'})
#         childrenTypes = ['com.alee.archive3.api.data.Card']
#         children = app.storm.getService('data').getTypedObjectChilds(first.objectId, childrenTypes, 0, 65535, sort)
#         # print children
#         if len(children)> 0:
#             firstCard = children[0]
#
#             # Retrieving complete card
#             card = app.storm.getService('data').getCompleteCard(firstCard.objectId, True, None)
#             print card
#             result += u'%s' % card
#     return result

# if __name__ == '__main__':
#app.run(host='127.0.0.1', port=5000, debug=True)
app.run(host='127.0.0.1', port=5000)
