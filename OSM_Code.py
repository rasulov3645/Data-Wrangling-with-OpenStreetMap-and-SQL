
# coding: utf-8

# ## P3 Case Study - Open Streetmap Data

# ### Quiz: Iterative Parsing

# In[ ]:

#!/usr/bin/env python

"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags={}
    for event, elem in ET.iterparse(filename):
        if type(elem.tag)=='None':
            pass
        if elem.tag not in tags.keys():
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    print tags
    print elem.tag


def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()


# ### Quiz: Tag Types

# In[1]:

#!/usr/bin/env python

import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into your database, you should check the
"k" value for each "<tag>" and see if there are any potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']
        if re.search(lower, k):
            keys["lower"] += 1
        elif re.search(lower_colon, k):
            keys["lower_colon"] += 1
        elif re.search(problemchars, k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
            
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()


# ### Quiz: Exploring Users

# In[ ]:

#!/usr/bin/env python

import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        tag = element.tag
        if tag in ['node', 'way', 'relation']:
            uniqueu = element.attrib['uid']
            users.add(uniqueu)
    return users

def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()


# ### Quiz: Improving Street Names

# In[2]:

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Ave.": "Avenue"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    # Note: '=' instead of '==', same for 'name' below
    name_upd = street_type_re.search(name)
    # add print statement
    print name_upd
    print name_upd.group()

    if name_upd:
        street_type = name_upd.group()
        if street_type in mapping.keys():
            name = re.sub(name_upd.group(), mapping[name_upd.group()], name)

    return name


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()


# ### Preparing for Database - SQL

# In[ ]:

#!/usr/bin/env python


"""
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so you will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files

We've already provided the code needed to load the data, perform iterative parsing and write the
output to csv files. Your task is to complete the shape_element function that will transform each
element into the correct format. To make this process easier we've already defined a schema (see
the schema.py file in the last code tab) for the .csv files and the eventual tables. Using the 
cerberus library we can validate the output against this schema to ensure it is correct.

## Shape Element Function
The function should take as input an iterparse Element object and return a dictionary.

### If the element top level tag is "node":
The dictionary returned should have the format {"node": .., "node_tags": ...}

The "node" field should hold a dictionary of the following top level node attributes:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset
All other attributes can be ignored

The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
child tags of node which have the tag name/type: "tag". Each dictionary should have the following
fields from the secondary tag attributes:
- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or "regular" if a colon
        is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag should be ignored
- if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key
- if there are additional ":" in the "k" value they and they should be ignored and kept as part of
  the tag key. For example:

  <tag k="addr:street:name" v="Lincoln"/>
  should be turned into
  {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field should just contain an empty list.

The final return value for a "node" element should look something like:

{'node': {'id': 757860928,
          'user': 'uboot',
          'uid': 26299,
       'version': '2',
          'lat': 41.9747374,
          'lon': -87.6920102,
          'timestamp': '2010-07-22T16:16:51Z',
      'changeset': 5288876},
 'node_tags': [{'id': 757860928,
                'key': 'amenity',
                'value': 'fast_food',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'cuisine',
                'value': 'sausage',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'name',
                'value': "Shelly's Tasty Freeze",
                'type': 'regular'}]}

### If the element top level tag is "way":
The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field should hold a dictionary of the following top level way attributes:
- id
-  user
- uid
- version
- timestamp
- changeset

All other attributes can be ignored

The "way_tags" field should again hold a list of dictionaries, following the exact same rules as
for "node_tags".

Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
dictionaries, one for each nd child tag.  Each dictionary should have the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within
            the way element

The final return value for a "way" element should look something like:

{'way': {'id': 209809850,
         'user': 'chicago-buildings',
         'uid': 674454,
         'version': '1',
         'timestamp': '2013-03-13T15:58:04Z',
         'changeset': 15353317},
 'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
               {'id': 209809850, 'node_id': 2199822390, 'position': 1},
               {'id': 209809850, 'node_id': 2199822392, 'position': 2},
               {'id': 209809850, 'node_id': 2199822369, 'position': 3},
               {'id': 209809850, 'node_id': 2199822370, 'position': 4},
               {'id': 209809850, 'node_id': 2199822284, 'position': 5},
               {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
 'way_tags': [{'id': 209809850,
               'key': 'housenumber',
               'type': 'addr',
               'value': '1412'},
              {'id': 209809850,
               'key': 'street',
               'type': 'addr',
               'value': 'West Lexington St.'},
              {'id': 209809850,
               'key': 'street:name',
               'type': 'addr',
               'value': 'Lexington'},
              {'id': '209809850',
               'key': 'street:prefix',
               'type': 'addr',
               'value': 'West'},
              {'id': 209809850,
               'key': 'street:type',
               'type': 'addr',
               'value': 'Street'},
              {'id': 209809850,
               'key': 'building',
               'type': 'regular',
               'value': 'yes'},
              {'id': 209809850,
               'key': 'levels',
               'type': 'building',
               'value': '1'},
              {'id': 209809850,
               'key': 'building_id',
               'type': 'chicago',
               'value': '366409'}]}
"""

import csv
import codecs
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "example.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    poscounter = 0 #for way nodes position
    # YOUR CODE HERE
    if element.tag == 'node':
        for field in NODE_FIELDS:
            node_attribs[field] = element.attrib[field]
        for tag in element.iter('tag'):
            tag_dict = {}
            tag_dict['id'] = element.attrib['id'] #id (NODE_TAGS_FIELDS)
            
            #key and type (NODE_TAGS_FIELDS)
            if PROBLEMCHARS.match(tag.attrib["k"]):
                pass
            elif ':' in tag.attrib['k']:
                tag_dict['type'] = tag.attrib['k'].split(':')[0]
                tag_dict['key'] = tag.attrib["k"].split(':',1)[1]
            else:
                tag_dict['type'] = 'regular'
                tag_dict['key'] = tag.attrib['k']
                
            #value (NODE_TAGS_FIELDS)
            tag_dict['value'] = tag.attrib['v']
            
            tags.append(tag_dict)
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for field in WAY_FIELDS:
            way_attribs[field] = element.attrib[field]
        for nd in element.iter('nd'):
            nd_dict = {}
            nd_dict['id'] = element.attrib['id']
            nd_dict['node_id'] = nd.attrib['ref']
            nd_dict['position'] = poscounter
            poscounter += 1
            way_nodes.append(nd_dict)
        for tag in element.iter('tag'):
            tag_dict = {}
            tag_dict['id'] = element.attrib['id'] #id
            #key and type
            if PROBLEMCHARS.match(tag.attrib["k"]):
                pass
            elif ':' in tag.attrib['k']:
                tag_dict['type'] = tag.attrib['k'].split(':')[0]
                tag_dict['key'] = tag.attrib["k"].split(':',1)[1]
            else:
                tag_dict['type'] = 'regular'
                tag_dict['key'] = tag.attrib['k']
            #value
            tag_dict['value'] = tag.attrib['v']
            
            tags.append(tag_dict)    
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)


# # P3 Assignment - Complete Code used 

# ### Auditing the Data

# In[ ]:

# loading modules for python

# ================================================== #
#       P3 Assignment: Complete Code used            #
# ================================================== #


'''
In order to start the data wrangling process, the following modules in python will be essential.
'''

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# opening file in filename
filename = open("phoenix_arizona.osm", "r")


# In[ ]:

# count the number of unique element types

'''
First we will create an empty dictionary and then parse through the tags to count them.
'''

tags = {}

for event, elem in ET.iterparse(filename):
    if elem.tag in tags: 
        tags[elem.tag] += 1
    else:
        tags[elem.tag] = 1
        
pprint.pprint(tags)


# In[ ]:

# lets look at number of unique users having edited the map for Phoenix Arizona

'''
By creating the process_map function, we start by creating an empty set, then parse through elements in the file. 
If the element attribute "uid" is found, it is added to the set. All we have to do then is to call the length of the set in order
to find the number of unique users.
'''

filename = open("phoenix_arizona.osm", "r")

def process_map(filename):
    users = set()
    for i, element in ET.iterparse(filename):
        for elem in element:
            if 'uid' in elem.attrib:
                users.add(elem.attrib['uid'])
    return users

users = process_map(filename)
len(users)


# ### Problem with the Data - Street Name Abbreviations

# In[ ]:

# ================================================== #
#               Street Name Abbreviations           #
# ================================================== #



# looking at streetnames

'''
We create a regex for the street names and store it in street_type_re. 
Furthermore we create a default dictionary that will include sets of different street names.
In a second step, we will audit the datafile and look for street names that have an ending that is different to
the values in the expected list.

'''

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Commons", "Mountain", "Highway", "Horne", "Sycamore", "Way", "Freeway", "Crossing",
            "Mall", "Loop", "Ventura"]


# In[ ]:

filename = open("phoenix_arizona.osm", "r")

def audit_street_type(street_types, street_name, regex, expected):
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'], regex, expected)
    pprint.pprint(dict(street_types))

audit(filename, street_type_re)


# In[ ]:

# Problematic Street Names - Change them for enhanced data quality

'''
Now we are going to do some data cleaning to enhance the data quality of the street names.
We have identified sets of street name endings that have not been expected. Through a a mapping dictionary we 
indicate the desired changes. We do this for the street name endings (mapping) , as well as the cardinal directions in the
beginning of the street names (mapping2)
'''

filename = open("phoenix_arizona.osm", "r")

mapping = {
            "Boulavard": "Boulevard",
            "D": "Drive",
            "street": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "RD": "Road",
            "Pkwy": "Parkway",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Glen": "Glendale",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "street": "Street",
            "St": "Street",
            "Glen": "Glendale",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ctr": "Centre",
            
            }


# In[ ]:

mapping2 =  {"E"  : "East",
             "E." : "East",
             "N"  : "North",
             "N." : "North",
             "S"  : "South",
             "S." : "South",
             "W"  : "West",
             "W." : "West"}


# In[ ]:

'''
The update name function implements the change. If a street name has the defined string which is defined in the two mapping
dictionaries, then the change is made as defined.
'''


def update_name(name, mapping, regex):
    m = regex.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = re.sub(regex, mapping[street_type], name)
    
    return name


# In[ ]:

street_type_re  = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_pre = re.compile(r'^[NSEW]\b\.?', re.IGNORECASE)


# In[ ]:

'''
We also identified some unique cases that will not be changed by the update name function. We explicitly state the 
change we want individually for each case.
'''


for street_type, ways in street_types.iteritems(): 
        for name in ways:
            if "Suite"  in name:
                name = name.split(", Suite")[0].strip()
            if "#" in name:
                name = name.split(" #")[0].strip()
            if "," in name:
                name = name.split(", ")[0].strip()
            if "Suite" in name:
                name = name.split(" Suite")[0].strip()
            if "Building" in name:
                name = name.split(" Building")[0].strip()
            if "Ste" in name:
                name = name.split(" Ste")[0].strip()
            if "St" in name:
                name = name.split(" St")[0].strip()
            name_improv_first = update_name(name, mapping, street_type_re)
            name_improv_sec = update_name(name_improv_first, mapping2, street_type_pre)
            
            print name, "=>", name_improv_first, "=>", name_improv_sec


# ### Problem with the Data - Postal Codes

# In[ ]:

# ================================================== #
#               Postal Codes                         #
# ================================================== #


'''
In this Section we are going to audit postal codes to check for potential errors. This is a very similar process compared to
to our cleaning street name strategy

'''
filename = open("phoenix_arizona.osm", "r")

zip_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

zip_types = defaultdict(set)

expected_zip = {}

def audit_zip_codes(zip_types, zip_name, regex, expected_zip):
    m = regex.search(zip_name)
    if m:
        zip_type = m.group()
        if zip_type not in expected_zip:
             zip_types[zip_type].add(zip_name)

def is_zip_name(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_zip_name(tag):
                    audit_zip_codes(zip_types, tag.attrib['v'], regex, expected_zip)
    pprint.pprint(dict(zip_types))

audit(filename, zip_type_re)


# In[ ]:

'''
We want to have all postal codes in the standard 5 digit display. This means we have to change the postal codes that have more
than 5 digits, the ones that beginn with "AZ" and any other ones that differ from the the plain 5 digit display.
'''

for zip_type, ways in zip_types.iteritems(): 
        for name in ways:
            if "-" in name:
                name = name.split("-")[0].strip()
            if "AZ" in name:
                name = name.split("AZ")[1].strip('AZ ')
            print name


# ### Problem with the Data - Phone Numbers

# In[ ]:

# ================================================== #
#               Phone Numbers                        #
# ================================================== #


'''
In this Section we are going to audit phone numbers. This is a similar process compared to auditing and cleaning street name 
abbreviations as well as postal codes

'''
filename = open("phoenix_arizona.osm", "r")

phone_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

phone_types = defaultdict(set)

expected_zip = {}

def audit_phone_num(phone_types, phone_num, regex, expected_phone):
    m = regex.search(phone_num)
    if m:
        phone_type = m.group()
        if phone_type not in expected_zip:
             phone_types[phone_type].add(phone_num)

def is_phone_num(elem):
    return (elem.attrib['k'] == "phone")


def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_phone_num(tag):
                    audit_phone_num(phone_types, tag.attrib['v'], regex, expected_zip)
    pprint.pprint(dict(phone_types))

audit(filename, phone_type_re)


# In[ ]:

'''
The goal is to have all phone numbers in a similar way: "XXX XXX XXXX". The phone numbers as we found out during the audit are
quite messy. We are using an approach were we explicitly state the required change for each set of cases.

'''

for phone_type, ways in phone_types.iteritems():
    for name in ways:
        if "+1 " in name:
            name = name.split("+1 ")[1].strip('+1 ')
        if "+" in name:
            name = name.split("+")[1].strip('+')
        if ";" in name:
            name = name.split(";")[0].strip()
        if name.startswith ("1-"): 
            name = name.strip("1-")
        if name.startswith ("1 "):
            name = name.strip("1 ")
        if "-" in name:
            name = name.replace("-", " ")
        if "(" in name:
            name = name.replace("(", "")
        if ")" in name:
            name = name.replace(")", "")
        if "." in name:
            name = name.replace(".", " ")
        if name.startswith("01"):
            name = name.strip("01")
        if name.startswith("Phone number "):
            name = name.strip("Phone number")
        if name.startswith("1 "):
            name = name.strip("1 ")
        if len(name) < 12:
            only_numbers = re.sub(r'\D', "", name)
            name = only_numbers[0:3] + " " + only_numbers[3:6] + " " + only_numbers[6:]
        if name.startswith(" "):
            name = name.replace(" ", "")
        if "x1" in name:
            name = name.strip("x1")
    
        print name


# ### Problematic Tags

# In[ ]:

# Look for problematic tag names

filename = open("phoenix_arizona.osm", "r")

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']
        if re.search(lower, k):
            keys["lower"] += 1
        elif re.search(lower_colon, k):
            keys["lower_colon"] += 1
        elif re.search(problemchars, k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
            
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

process_map(filename)


# ### Create csv Files and prepare Database

# In[ ]:

# import xml data into a csv file for later integration into sql database

# first load necessary packages

import csv
import codecs
import cerberus
import schema


# In[ ]:

# create the csv files to which specific data should be drawn


OSM_PATH = "phoenix_arizona.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"


# In[ ]:

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# In[ ]:

# Look for problematic tag names

filename = open("phoenix_arizona.osm", "r")

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']
        if re.search(lower, k):
            keys["lower"] += 1
        elif re.search(lower_colon, k):
            keys["lower_colon"] += 1
        elif re.search(problemchars, k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
            
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

process_map(filename)


# In[ ]:

process_map(OSM_PATH, validate=True)

# ALL DONE. NOW LETS LOAD THE CSV FILES INTO SQL AND START PERFORMING QUERIES


# In[ ]:

# Note: The schema is stored in a .py file in order to take advantage of the
# int() and float() type coercion functions. Otherwise it could easily stored as
# as JSON or another serialized format.

SCHEMA = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}


# In[ ]:

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    poscounter = 0 #for way nodes position
    
    if element.tag == 'node':
        for field in NODE_FIELDS:
            node_attribs[field] = element.attrib[field]
        for tag in element.iter('tag'):
            tag_dict = {}
            tag_dict['id'] = element.attrib['id'] #id (NODE_TAGS_FIELDS)
            
            #key and type (NODE_TAGS_FIELDS)
            if PROBLEMCHARS.match(tag.attrib["k"]):
                pass
            elif ':' in tag.attrib['k']:
                tag_dict['type'] = tag.attrib['k'].split(':')[0]
                tag_dict['key'] = tag.attrib["k"].split(':',1)[1]
            else:
                tag_dict['type'] = 'regular'
                tag_dict['key'] = tag.attrib['k']
                
            #value (NODE_TAGS_FIELDS)
            tag_dict['value'] = tag.attrib['v']
            
            tags.append(tag_dict)
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for field in WAY_FIELDS:
            way_attribs[field] = element.attrib[field]
        for nd in element.iter('nd'):
            nd_dict = {}
            nd_dict['id'] = element.attrib['id']
            nd_dict['node_id'] = nd.attrib['ref']
            nd_dict['position'] = poscounter
            poscounter += 1
            way_nodes.append(nd_dict)
        for tag in element.iter('tag'):
            tag_dict = {}
            tag_dict['id'] = element.attrib['id'] #id
            #key and type
            if PROBLEMCHARS.match(tag.attrib["k"]):
                pass
            elif ':' in tag.attrib['k']:
                tag_dict['type'] = tag.attrib['k'].split(':')[0]
                tag_dict['key'] = tag.attrib["k"].split(':',1)[1]
            else:
                tag_dict['type'] = 'regular'
                tag_dict['key'] = tag.attrib['k']
            #value
            tag_dict['value'] = tag.attrib['v']
            
            tags.append(tag_dict)    
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
    
# HELPER FUNCTIONS    
    
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# MAIN FUNCTION

def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


# In[ ]:

process_map(OSM_PATH, validate=False)

# ALL DONE. NOW LETS LOAD THE CSV FILES INTO SQL AND START PERFORMING QUERIES


# ### Preparing for SQL

# In[ ]:

### import sqlite3

import sqlite3
import csv
from pprint import pprint

sqlite_file = 'OpenStreetMap2.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        
def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
cur.execute('''
    CREATE TABLE nodes(id INTEGER, lat REAL, lon REAL, user TEXT, uid INTEGER, 
    version INTEGER, changeset INTEGER, timestamp TIMESTAMP)
''')
cur.execute('''
    CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, changeset INTEGER, timestamp TIMESTAMP)
''')
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT, type TEXT) 
''')
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')

# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('nodes_tags.csv','rb') as fin:
    dr = UnicodeDictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'], i['type']) for i in dr]

with open('nodes.csv', 'rb') as fin2:
    dr2 = UnicodeDictReader(fin2)
    to_db2 = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr2]
    
with open('ways.csv', 'rb') as fin3:
    dr3 = UnicodeDictReader(fin3)
    to_db3 = [(i['id'], i['user'], i['uid'], i['changeset'], i['timestamp']) for i in dr3]
    
with open('ways_tags.csv', 'rb') as fin4:
    dr4 = UnicodeDictReader(fin4)
    to_db4 = [(i['id'], i['key'], i['value'], i['type']) for i in dr4]  
    
with open('ways_nodes.csv', 'rb') as fin5:
    dr5 = UnicodeDictReader(fin5)
    to_db5 = [(i['id'], i['node_id'], i['position']) for i in dr5]  
    
    # insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db2)
cur.executemany("INSERT INTO ways(id, user, uid, changeset, timestamp) VALUES (?, ?, ?, ?, ?);", to_db3)
cur.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_db4)
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db5)

# commit the changes
conn.commit()

cur.execute('SELECT * FROM nodes_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)

conn.close()


# In[ ]:

# WHAT WE DID SO FAR: 

# ANALYSE XML FILE FROM OPEN STREET MAP
# LOOK FOR FAULTY STREET NAMES
# CHANGE STREET NAMES ACCORDINGLY
# CREATE CSV FILES
# CREATE DATABASE AND INSERT CSV FILES INTO DATABASE

# READY FOR THE NEXT STEP


# ### SQL Queries

# In[ ]:

# Counting number of nodes

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
    SELECT COUNT(*) FROM nodes;
''')
all_rows = cur.fetchall()

print('Number of nodes are:{}').format(all_rows)

conn.commit()


# In[ ]:

# Counting number of nodes

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
    SELECT COUNT(*) FROM ways;
''')
all_rows = cur.fetchall()

print('Number of ways are:{}').format(all_rows)

conn.commit()


# In[ ]:

# Counting number of unique users

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
''')

all_rows = cur.fetchall()

print('Number of unique users are:{}').format(all_rows)

conn.commit()


# In[ ]:

# TOP 10 contributing users

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
''')

all_rows = cur.fetchall()

print('Number of unique users are:')
pprint(all_rows)

conn.commit()


# In[ ]:

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1)  u;
''')

all_rows = cur.fetchall()

print('Number of unique users only appearing once are:')
pprint(all_rows)

conn.commit()


# In[ ]:

# Sorts Parts of the metropolitan area of Phoenix

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC;

''')

all_rows = cur.fetchall()

print('1):')
pprint(all_rows)

conn.commit()


# In[3]:

# TOP 10 appearing amenities

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 5;

''')

all_rows = cur.fetchall()

print('1):')
pprint(all_rows)

conn.commit()


# In[ ]:

# Most popular Cusines

# TOP 10 appearing amenities

conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

cur.execute('''
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC;

''')

all_rows = cur.fetchall()

print('1):')
pprint(all_rows)

conn.commit()


# In[ ]:




# In[ ]:




# In[ ]:



