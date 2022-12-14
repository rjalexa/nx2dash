""" from networkx
    to Dash cytoscape
    """
import dash_cytoscape as cyto
from dash import Dash, html
import networkx as nx

SCALING_FACTOR = 5000  # try using to scatter nodes

app = Dash(__name__)

# 1) generate a networkx graph
G = nx.les_miserables_graph()

# 2) apply a netowrkx layouting algorithm
pos = nx.fruchterman_reingold_layout(G, k=0.1, iterations=2000, threshold=1e-10)

# 3) convert networkx graph to cytoscape format
cy = nx.cytoscape_data(G)

# 4.) Add the dictionary key label to the nodes list of cy
for n in cy["elements"]["nodes"]:
    for k, v in n.items():
        v["label"] = v.pop("value")

# 5.) Add the coords you got from (2) as coordinates of nodes in cy
for n, p in zip(cy["elements"]["nodes"], pos.values()):
    n["position"] = {"x": int(p[0] * SCALING_FACTOR), "y": int(p[1] * SCALING_FACTOR)}

# 6.) Take the results of (3)-(5) and write them to a list
elements = cy["elements"]["nodes"] + cy["elements"]["edges"]

app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape-layout-6",
            elements=elements,
            style={"width": "100%", "height": "800px"},
            layout={"name": "preset"},  # "preset" to use the pos coords
        )
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
