class Field(object):
    pass


class Property(Field):

    @staticmethod
    def save_properties(node, properties):
        """

        :param node: a Neo4j node
        :param properties: a dictionary of properties to values
        :return:
        """
        for property, value in properties.iteritems():
            node[property] = value


class IndexField(Field):
    pass


class RelationshipField(Field):


    def __init__(self, *args, **kwargs):
        """
        :param relationship_type: a pithy string summarizing the relationship
        """
        # self.relationship_type = relationship_type
        pass

class RelationshipTo(RelationshipField):

    def __init__(self, *args, **kwargs):
        pass
