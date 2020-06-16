import pandas as pd
import json

COLUMN_NAME='department'
FILE = "../data/graph_general.json"

with open(FILE, 'r') as f:
    graph = json.load(f)

data = pd.DataFrame.from_records(graph['nodes'])

colors = data['color'].astype('category')
attributes = pd.DataFrame.from_records(data['attributes'])

for column in attributes.columns:
    if attributes[column].apply(lambda x: str(x).isnumeric()).all():
        attributes[column] = attributes[column].astype('float')
    else:
        attributes[column] = attributes[column].astype('category')

attrib_color = attributes.copy()
attrib_color['color'] = colors

result = {}

if attributes[COLUMN_NAME].dtype == 'category':
    mapping = {}
    for item in attributes[COLUMN_NAME].unique():
        mode = attrib_color[attrib_color[COLUMN_NAME] == item]['color'].mode()[0]
        mapping[item] = mode

    result['type'] = 'categorical'
    result['mapping'] = mapping

    print(json.dumps(result))
else:
    id_min = attrib_color[COLUMN_NAME].argmin()
    id_max = attrib_color[COLUMN_NAME].argmax()

    #col_min = attrib_color['color'][id_min] = 