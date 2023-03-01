import requests
import datetime as dt

from backend.config import THEGRAPH_API_KEY
from backend.services.graph.subgraphs import SubgraphService
# from helpers.thegraph import query_thegraph

DEFAULT_PROTOCOL = "makerdao"
DEFAULT_CHAIN = "ethereum"


def query_thegraph(subgraph_id, query, hosted=True):
    if hosted:
        base_url = "https://api.thegraph.com/subgraphs/name/"
    else:
        base_url = f"https://gateway.thegraph.com/api/{THEGRAPH_API_KEY}/subgraphs/id/"
    query_url = f"{base_url}{subgraph_id}"
    r = requests.post(query_url, json={"query": query})
    r.raise_for_status()
    try:
        # assumes only one table is being queried
        first_table_name = list(r.json()["data"].keys())[0]
        return r.json()["data"][first_table_name]
    except KeyError:
        print(r.json())


class GraphService:
    def __init__(self, protocol=DEFAULT_PROTOCOL, chain=DEFAULT_CHAIN):
        self.protocol = protocol
        self.chain = chain
        self.subgraph_service = SubgraphService()
        self.protocols = self.subgraph_service.get_prod_subgraphs()
        if "decentralized-network" in self.protocols[protocol]["deployments"][chain]:
            service_type = "decentralized-network"
        else:
            service_type = "hosted-service"
        self.query_id = self.protocols[protocol]["deployments"][chain][service_type]["query-id"]

    def query_thegraph(self, gql, service_type=True):
        data = query_thegraph(
            self.query_id,
            gql,
            hosted=(service_type == "hosted-service"),
        )
        print("==========the graph response:==========\n", data)
        for dict_item in data:
            for key, val in dict_item.items():
                if key == 'timestamp':
                    # print(dt.datetime.utcfromtimestamp(int(val)).strftime('%Y-%m-%d %H:%M:%S'))
                    dict_item[key]= dt.datetime.utcfromtimestamp(int(val)).strftime('%Y-%m-%d %H:%M:%S')
        print("end data", data)
        return data
