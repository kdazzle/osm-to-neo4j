import xml.etree.ElementTree as element_tree
import os

from models import GeoLocation, Vector, VectorNode, Way, Street, Building


OSM_FILE_LOCATION = '../smaller_map.osm'


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

        street.vector.connect(vector)
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
    vector.id = way_id
    vector.save()
    return vector


def create_vector_nodes(vector, way, way_id):
    node_references = way.findall('nd')
    vector_nodes = []
    previous_node = None

    for node_reference in node_references:
        node_id = node_reference.get('ref')
        try:
            location = GeoLocation.index.search("id:{0}".format(node_id))[0]
            vector_node = create_vector_node(location, vector, previous_node)
            vector_nodes.append(vector_node)
            previous_node = vector_node
        except Exception as e:
            print('Error adding way #{0}, node #{1}: {2}'.format(
                way_id, node_id, str(e)
            ))
            continue

    if len(vector_nodes) > 0:
        vector.origin.connect(vector_nodes[0])
        vector.terminus.connect(vector_nodes[-1])
        vector.save()


def create_vector_node(location, vector, previous):
    vector_node = VectorNode()
    vector_node.save()
    vector_node.location.connect(location)
    vector_node.vector.connect(vector)

    if previous is not None:
        vector_node.previous.connect(previous)

    vector_node.save()
    return vector_node


def delete_everything():
    from py2neo import neo4j

    graph_db = neo4j.GraphDatabaseService(neo4j.DEFAULT_URI)
    graph_db.clear()


if __name__ == '__main__':
    os.environ['NEO4J_REST_URL'] = NEO4J_REST_URL
    delete_everything()
    print('everything deleted')
    parse()
