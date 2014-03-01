from .fields import Property, RelationshipTo, RelationshipFrom
from .db import Node


class OsmNode(Node):
    """
    The Neo4J representation of an Open Street Map node
    """

    osm_id = Property()
    "The node ID given by Open Street Map"

    def __init__(self, *args, **kwargs):
        for property, value in kwargs.iteritems():
            setattr(self, property, value)


class GeoLocation(OsmNode):

    latitude = Property()
    longitude = Property()

    def __init__(self, osm_id, latitude, longitude, **kwargs):
        self.osm_id = osm_id
        self.latitude = latitude
        self.longitude = longitude
        super(GeoLocation, self).__init__(self, **kwargs)

    @staticmethod
    def get_by_osm_id(osm_id):
        # TODO: should filter on GeoLocation
        nodes = GeoLocation.manager.find_by_property("osm_id", osm_id)
        return nodes[0]


class Vector(OsmNode):

    terminus = RelationshipTo('VectorSegment', 'ends_at')
    origin = RelationshipTo('VectorSegment', 'begins_at')


class VectorSegment(OsmNode):

    location = RelationshipTo('GeoLocation', 'is_located_at')
    next = RelationshipTo('VectorSegment', 'connects_to')
    previous = RelationshipFrom('VectorSegment', 'connects_to')
    vector = RelationshipTo('Vector', 'has_vector')


class Way(OsmNode):

    pass


class Street(Way):

    name = Property()
    vector = RelationshipTo('Vector', 'has_vector')


class Highway(Street):

    pass


class ResidentialStreet(Street):

    pass


class Building(OsmNode):

    location = RelationshipTo('GeoLocation', 'is_located_at')
