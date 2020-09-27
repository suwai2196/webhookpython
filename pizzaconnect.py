{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "* Owlready2 * Warning: optimized Cython parser module 'owlready2_optimized' is not available, defaulting to slower Python implementation\n"
     ]
    }
   ],
   "source": [
    "import urllib\n",
    "import json\n",
    "import os\n",
    "\n",
    "import psycopg2\n",
    "from pprint import pprint\n",
    "\n",
    "from flask import Flask\n",
    "from flask import request\n",
    "from flask import make_response\n",
    "from owlready2 import *\n",
    "\n",
    "def ConnectOnto():\n",
    "    my_world = World()\n",
    "    my_world.get_ontology('file://C:/Users/Hp/Documents/a/owl/pizza.owl').load()  # path to the owl file is given here\n",
    "    # reasoner is started and synchronized here\n",
    "    graph = my_world.as_rdflib_graph()\n",
    "    return graph\n",
    "\n",
    "graph = ConnectOnto()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route('/webhook', methods=['POST'])\n",
    "\n",
    "def webhook():\n",
    "    req = request.get_json(silent=True, force=True)\n",
    "\n",
    "    print(\"Request:\")\n",
    "    print(json.dumps(req, indent=4))\n",
    "\n",
    "    res = makeWebhookResult(req)\n",
    "\n",
    "    res = json.dumps(res, indent=4)\n",
    "    print(res)\n",
    "    r = make_response(res)\n",
    "    r.headers['Content-Type'] = 'application/json'\n",
    "    return r\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "def makeWebhookResult(req):\n",
    "    if req.get(\"result\").get(\"action\") == \"listPizza\":\n",
    "        graph = ConnectOnto()\n",
    "        result = req.get(\"result\")\n",
    "        parameters = result.get(\"parameters\")\n",
    "        a = None\n",
    "        \n",
    "\n",
    "\n",
    "\n",
    "        query = (\"PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  \\\n",
    "                                            PREFIX owl: <http://www.w3.org/2002/07/owl#>  \\\n",
    "                                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  \\\n",
    "                                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  \\\n",
    "                                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \\\n",
    "                                            SELECT ?pizza   \\\n",
    "                                            WHERE {?pizza rdfs:subClassOf pz:NamedPizza .}\")\n",
    "        results = graph.query(query)\n",
    "        response = []\n",
    "        for item in results:\n",
    "            pizza = str(item['pizza'].toPython())\n",
    "            pizza = re.sub(r'.*#', \"\", pizza)\n",
    "            response.append('-' + pizza)\n",
    "            a = '\\n'.join(map(str, response))\n",
    "\n",
    "        if a is None:\n",
    "            b = \"Sorry, we don't have offfer for you now.\"\n",
    "        else:\n",
    "            b = \"These are offered pizza for you  \\n\" + a\n",
    "\n",
    "\n",
    "        fulfillmentText = b\n",
    "        print(\"Response:\")\n",
    "        print(fulfillmentText)\n",
    "        return {\n",
    "            # \"data\": {},\n",
    "            # \"contextOut\": [],\n",
    "            \"source\": \"chatbottest\"\n",
    "            \"speech\": fulfillmentText,\n",
    "            \"fulfillmentText\": fulfillmentText,\n",
    "            \"displayText\": 'listPizza',\n",
    "            \"source\": \"webhookdata\"\n",
    "    }"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
