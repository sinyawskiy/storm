__author__ = 'azernov'

from pyhessian.parser import cls_factory

# Class definition
SeanceType = cls_factory ( 'com.alee.archive3.api.security.to.SeanceType', [ 'name' ] )

SortingField = cls_factory ( 'com.alee.archive3.api.constants.SortingField', [ 'name' ] )

SearchRequest = cls_factory ( 'com.alee.archive3.api.search.SearchRequest',
                              [ 'id', 'fieldList', 'fileSearch', 'skipMissingAttributes', 'fullTxtSearch', 'sortingFields', 'sortOrder' ] )
AdvSearchableField = cls_factory ( 'com.alee.archive3.api.search.AdvSearchableField',
                                   [ 'id', 'request', 'fieldType', 'fieldName', 'matchType', 'fieldConditions', 'SearchOperator' ] )
FieldType = cls_factory ( 'com.alee.archive3.api.search.FieldType', [ 'name' ] )
MatchType = cls_factory ( 'com.alee.archive3.api.search.MatchType', [ 'name' ] )
SearchOperator = cls_factory ( 'com.alee.archive3.api.search.SearchOperator', [ 'name' ] )

ArchiveObject = cls_factory ( 'com.alee.archive3.api.data.ArchiveObject',
                              [ 'objectId', 'symbolicLink', 'system', 'deleted', 'historical', 'lockingVersion', 'creationDate',
                                'modificationDate', 'oldVerticalIndex', 'verticalIndex', 'versionNumber', 'keywords', 'linkedObject',
                                'name', 'objectPath', 'objectInfo', 'objectModifier', 'objectType', 'ownerUser', 'parentObject', 'vendorId',
                                'objectColorMark', 'userLockStatus', 'userLockDate', 'childsOrder' ] )
DictionaryRecord = cls_factory ( 'com.alee.archive3.api.data.DictionaryRecord', None, ( ArchiveObject, ) )