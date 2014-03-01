class Field(object):
    pass


class Property(Field):

    @staticmethod
    def save_properties(node, properties):
        """
        Adds the given properties to the given node

        :param node: a Neo4j node
        :param properties: a dictionary of properties to values
        """
        for property, value in properties.iteritems():
            node[property] = value


class IndexField(Field):
    pass


class RelationshipField(Field):

    def __init__(self, relationship_type, relation, *args, **kwargs):
        """
        :param relationship_type: a pithy string summarizing the relationship
                for example: "Knows"
        :param relation: the Node that has a relationship with this Node
        """
        self.relationship_type = relationship_type
        self.relation = relation

    @staticmethod
    def save_relationships(node, relationships):
        """

        :param node: the start node of a directional relationship
        :param relationships: a dictionary of relationships by relationship
                type to a node: {"Knows": janeNode}

        """
        for relationship_type, relation in relationships.iteritems():
            node.relationships.create(relationship_type, relation)


class RelationshipTo(RelationshipField):

    pass


class RelationshipFrom(RelationshipField):

    @staticmethod
    def save_relationships(node, relationships):
        """
        Saves all of the relationships
        :param node: The end node of the directional relationship
        :param relationships: a dictionary of relationships by relationship
                type to a node: {"Knows": janeNode}
        """
        for relationship_type, relation in relationships.iteritems():
            relation.relationships.create(relationship_type, node)
