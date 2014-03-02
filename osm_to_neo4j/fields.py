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

    def __init__(self, relation, relationship_type, *args, **kwargs):
        """
        :param relation: the Node that has a relationship with this Node
        :param relationship_type: a pithy string summarizing the relationship
                        for example: "Knows"
        """
        self.relationship_type = relationship_type
        self.relation = relation

    @staticmethod
    def save_relationships(instance, node, relationships):
        """
        :param instance: the instance that contains this relationship field
        :param node: the start node of a directional relationship
            :type node: neo4jrestclient.client.Node
        :param relationships: a dictionary of attribute names to their values:
                {"vector": VectorObj}
        """
        calling_class = instance.__class__

        for attribute_name, value in relationships.iteritems():
            relationship_field = getattr(calling_class, attribute_name)
            relationship_type = relationship_field.relationship_type
            node.relationships.create(relationship_type, value)


class RelationshipTo(RelationshipField):

    pass


class RelationshipFrom(RelationshipField):

    @staticmethod
    def save_relationships(instance, node, relationships):
        """
        :param instance: the instance that contains this relationship field
        :param node: The end node of the directional relationship
            :type node: neo4jrestclient.client.Node
        :param relationships: a dictionary of attribute names to their values:
                {"vector": VectorObj}
        """
        calling_class = instance.__class__

        for attribute_name, related_node in relationships.iteritems():
            relationship_field = getattr(calling_class, attribute_name)
            relationship_type = relationship_field.relationship_type
            related_node.neo4j_node.relationships.create(relationship_type, node)
