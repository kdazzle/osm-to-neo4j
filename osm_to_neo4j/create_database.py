from os.path import join, dirname
import xml.etree.ElementTree as element_tree

from .models import GeoLocation, Vector, VectorSegment, Street
from .__init__ import db


OSM_FILE_LOCATION = join(dirname(__file__), '..', 'sample_map.osm')


def parse():
    xml_tree = element_tree.parse(OSM_FILE_LOCATION)
    root = xml_tree.getroot()

    nodes = root.findall('node')
    add_geo_locations(nodes)

    ways = root.findall('way')
    add_streets(ways)


def add_geo_locations(nodes):
    for node in nodes:
        is_visible = node.get('visible')
        if is_visible.lower() == 'false':
            continue

        geo_location = GeoLocation(
            node.get('id'),
            node.get('lat'),
            node.get('lon')
        )

        try:
            geo_location.save()
        except Exception as e:
            print 'Exception: {0}'.format(e.message)
            pass


def add_streets(ways):
    for way in ways:
        if not is_street(way):
            continue

        street = Street()
        street.name = get_street_name(way)
        street.save()

        way_id = way.get('id')
        vector = create_vector(way_id)
        create_vector_nodes(vector, way, way_id)

        street.vector = vector
        street.save()

        print('Added street {0}'.format(street.name.encode('utf8')))


def is_street(way):
    tags = way.findall('tag')
    for tag in tags:
        if (tag.get('k').lower() == 'highway' and
                tag.get('v').lower() == 'residential'):
            return True

    return False


def get_street_name(way):
    tags = way.findall('tag')
    for tag in tags:
        if tag.get('k').lower() == 'name':
            return tag.get('v')

    print 'No street name! way #{0} :('.format(way.get('id'))
    return 'Street #{id}'.format(id=way.get('id'))


def create_vector(way_id):
    vector = Vector()
    vector.osm_id = way_id
    vector.save()
    return vector


def create_vector_nodes(vector, way, way_id):
    node_references = way.findall('nd')
    vector_nodes = []
    previous_node = None

    for node_reference in node_references:
        node_id = node_reference.get('ref')
        try:
            location = GeoLocation.get_by_osm_id(node_id)
            vector_node = create_vector_node(location, vector, previous_node)
            vector_nodes.append(vector_node)
            previous_node = vector_node
        except Exception as e:
            print('Error adding way #{0}, node #{1}: {2}'.format(
                way_id, node_id, str(e)))
            continue

    if len(vector_nodes) > 0:
        vector.origin = vector_nodes[0]
        vector.terminus = vector_nodes[-1]
        vector.save()


def create_vector_node(location, vector, previous):
    vector_segment = VectorSegment(
        location=location,
        vector=vector)

    if previous is not None:
        vector_segment.previous = previous

    vector_segment.save()
    return vector_segment


if __name__ == '__main__':
    parse()
