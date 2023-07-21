import datetime as dt
import json
import os

import pandas as pd
import requests

from backend.config import THEGRAPH_API_KEY
from backend.services.graph.subgraphs import SubgraphService
from backend.services.graph import *
DEFAULT_PROTOCOL = "aave-governance"
DEFAULT_CHAIN = "ethereum"

CHAINS = [
    "arbitrum",
    "aurora",
    "avalanche",
    "boba",
    "bsc",
    "celo",
    "clover",
    "ethereum",
    "fantom",
    "fuse",
    "gnosis",
    "harmony",
    "optimism",
    "polygon",
    "moonbeam",
    "moonriver",
]

subgraph_id = 'ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7'
query = '''{
  liquidityPools(first: 5, orderBy: cumulativeVolumeUSD, orderDirection: desc, where: {inputTokens_: {symbol: "USDC"}}) {
    name
    cumulativeVolumeUSD
    totalValueLockedUSD
  }
}'''
hosted = True

def execute_query_thegraph(subgraph_id, query, hosted=True):
    namespace = "marissaposner" if subgraph_id == "sporkdao-token" else "messari"
    if hosted:
        base_url = f"https://api.thegraph.com/subgraphs/name/{namespace}/"
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
        # TODO: error handling
        print(r.json())


class GraphService:
    def __init__(self, protocol=DEFAULT_PROTOCOL, chain=DEFAULT_CHAIN):
        self.build_subgraphs_json()
        self.subgraph = SubgraphService(protocol, chain)

    def ensure_enumerable(self, data):
        if not isinstance(data, list):
            return [data]
        return data

    def query_thegraph(self, gql):
        data = execute_query_thegraph(
            self.subgraph.query_id,
            gql,
            hosted=(self.subgraph.service_type == "hosted-service"),
        )

        print("==========the graph response:==========\n", data)
        if data == None:
            raise ValueError()
        data = self.ensure_enumerable(data)
        for dict_item in data:
            for key, val in dict_item.items():
                if key == "timestamp":
                    # print(dt.datetime.utcfromtimestamp(int(val)).strftime('%Y-%m-%d %H:%M:%S'))
                    dict_item[key] = dt.datetime.utcfromtimestamp(int(val)).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
        print("==========the graph response (formatted):==========\n", data)
        return data

    def build_subgraphs_json(self):
        print("in build subgraphs")
        deployments = json.load(
            open(os.getcwdb().decode("utf-8") + "/backend/subgraphs/deployment/deployment.json")
        )
        print('after deployments in build subgraphs')
        li = []
        for protocol in deployments:
            for chain in CHAINS:
                try:
                    df = pd.DataFrame([SubgraphService(protocol, chain).__dict__])
                    df.pop("protocol")
                    df = df.join(df["deployments"].apply(pd.Series), lsuffix="_")
                    df.pop("deployments_")
                    df["deployments"].iloc[0] = (
                        df["deployments"]
                        .apply(pd.Series)[f"{protocol}-{chain}"]
                        .iloc[0]
                    )
                    li.append(df)
                except NotImplementedError:
                    pass
        df = pd.concat(li)
        df = df.set_index(["protocol", "chain"])
        json_dump = df.to_json(
            indent=2,
            orient="index",
        ).replace("\\/", "/")
        print(
            json_dump,
            file=open(
                os.path.join(
                    os.getcwdb().decode("utf-8"),
                    "backend/backend/services/graph/",
                    "subgraphs.json",
                ),
                "w",
            ),
        )
        return df
def QUERY_API_RESPONSE_FORMATTER(id, gql, output):
    return {"id": id, "gql": gql, "output": output}


gql = execute_query_thegraph(subgraph_id, query, hosted=True)
print(gql)
graph_service = GraphService(protocol=subgraph_id)
print('after graph service')
try:
    result = graph_service.query_thegraph(gql)
except ValueError:
    # import pdb;pdb.set_trace()
    QUERY_API_RESPONSE_FORMATTER("-1", gql, [])


