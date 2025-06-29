# graphql_crm/schema.py
import graphene
from crm.schema import Query as CRMQuery
from crm.schema import Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
