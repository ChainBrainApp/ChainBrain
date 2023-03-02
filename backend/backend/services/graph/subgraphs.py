"""
instructions:
$ git clone git@github.com:messari/subgraphs.git in the project's root dir

scan the messari subgraphs repository and build an overview of production ready
subgraphs with:
- filename to their graphql schema
- subgraph type (lending, dex-amm, generic, governance, bridge, yield-aggregator, nft-marketplace)
- network(s)
- their subgraph id, both for hosted and/or decentralised subgraphs
"""
import glob
import json
import os

import yaml


class SubgraphService:
    def __init__(self, protocol, chain):
        self.protocol = protocol
        self.chain = chain
        self.deployments = json.load(
            open(os.getcwdb().decode("utf-8") + "/subgraphs/deployment/deployment.json")
        )[protocol]
        if (
            "decentralized-network"
            in self.deployments["deployments"][f"{protocol}-{chain}"]["services"]
        ):
            self.service_type = "decentralized-network"
        elif (
            "hosted-service"
            in self.deployments["deployments"][f"{protocol}-{chain}"]["services"]
        ):
            self.service_type = "hosted-service"
        try:
            self.query_id = self.deployments["deployments"][f"{protocol}-{chain}"][
                "services"
            ][self.service_type]["query-id"]
        except AttributeError:
            # protocol does not have any deployments
            self.query_id = None
            raise NotImplementedError
        try:
            self.template_file_location = f"subgraphs/subgraphs/{self.deployments['base']}/protocols/{self.protocol}/config/templates/{self.deployments['deployments'][f'{protocol}-{chain}']['files']['template']}"
        except:
            self.template_file_location = None
            pass
        if os.path.isfile(
            f"subgraphs/subgraphs/{self.deployments['base']}/schema.graphql"
        ):
            self.schema_file_location = (
                f"subgraphs/subgraphs/{self.deployments['base']}/schema.graphql"
            )
        else:
            self.schema_file_location = None
        self.mappers = self.read_mappings_dir(
            f"subgraphs/subgraphs/{self.deployments['base']}/src"
        )

    def read_mappings_dir(self, directory):
        return list(glob.iglob(f"{directory}/**/*.ts", recursive=True))

    def parse_template_file(self):
        # TODO: yaml.constructor.ConstructorError: while constructing a mapping
        with open(self.template_file_location, "r") as stream:
            yaml_content = yaml.safe_load(stream)
        print(yaml_content)
