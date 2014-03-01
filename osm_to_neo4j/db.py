from .__init__ import db
from .fields import Property, RelationshipFrom, RelationshipTo

from neo4jrestclient.query import Q


class NodeManager(object):

    @staticmethod
    def find_by_property(property, value):
        """
        Performs a case-sensitive query on the database and returns
        matching nodes

        :param property: string - the property being queried
        :param value: the value that the property should be (case-sensitive)
        :return: list of nodes
        """
        lookup = Q(property, exact=value)
        return db.nodes.filter(lookup)


class Node(object):
    """
    A Neo4j Node
    """

    manager = NodeManager()

    def __init__(self, *args, **kwargs):
        pass

    def save(self):
        """
        Save properties, relationships, and labels to the database.
        """

        #TODO: This should be in a transaction
        node = db.nodes.create()
        node.labels.add(self.__class__.__name__)

        fields_by_field_type = self.get_fields_by_field_type()

        Property.save_properties(node, fields_by_field_type.get('Property', {}))
        RelationshipTo.save_relationships(
            node, fields_by_field_type.get('RelationshipTo', {}))
        RelationshipFrom.save_relationships(
            node, fields_by_field_type.get('RelationshipFrom', {}))

    def get_fields_by_field_type(self):
        """
        Sorts attributes by their field type.

        :return dict 2-dimensional dictionary mapped like:
            {'FieldType': {attribute_name: attribute_value} }
        """

        fields_by_field_type = {}

        for attribute_key, value in self.__dict__.iteritems():
            attribute = getattr(self.__class__, attribute_key)
            field_type = attribute.__class__.__name__

            fields_by_field_type.setdefault(field_type, {}).update({
                attribute_key: value
            })

        return fields_by_field_type
