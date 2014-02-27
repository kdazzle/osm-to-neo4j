from .fields import Property, RelationshipField, IndexField, RelationshipTo
from .db import Node


class OsmNode(Node):
    """
    An Open Street Map node
    """

    osm_id = Property()
    "The node ID given by Open Street Map"


class GeoLocation(OsmNode):
    latitude = Property()
    longitude = Property()

    def __init__(self, osm_id, latitude, longitude, **kwargs):
        self.osm_id = osm_id
        self.latitude = latitude
        self.longitude = longitude
        super(GeoLocation, self).__init__(self, **kwargs)


class Vector(OsmNode):
    #TODO: Is this class necessary? Are vectors ordered in any way?

    terminus = RelationshipTo('VectorNode', 'ends_at')
    origin = RelationshipTo('VectorNode', 'begins_at')


class VectorNode(OsmNode):
    # TODO: Rename or subclass to StreetSegment?

    location = RelationshipTo('GeoLocation', 'is_located_at')
    next = RelationshipTo('VectorNode', 'goes_to')
    previous = RelationshipTo('VectorNode', 'comes_from')
    vector = RelationshipTo('Vector', 'belongs_to')


class Way(OsmNode):

    def is_street(self):
        pass


class Street(Way):
    # Has a collection of GeographicLocations
    name = Property()
    vector = RelationshipTo('Vector', 'has_vector')


class Building(OsmNode):
    location = RelationshipTo('GeoLocation', 'is_located_at')
