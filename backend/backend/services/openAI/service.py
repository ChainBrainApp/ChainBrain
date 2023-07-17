import openai
import requests

from backend.config import OPENAI_API_KEY
from backend.services.openAI.graph_prompt_factory import GraphPromptFactory
from llama_index import (
    LLMPredictor,
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
    PromptHelper,
)
from llama_index.indices import GPTListIndex
from llama_index import Document
from backend.services.graph.service import GraphService


from langchain import OpenAI
from backend.services.graph import subgraphs
import os

PROTOCOL_TO_PATH = {"opensea-v2": "opensea", "opensea-v1": "opensea"}


def protocol_path_formatter(protocol):
    return PROTOCOL_TO_PATH.get(protocol, protocol)


def mapping_path(protocol):
    path = protocol_path_formatter(protocol)
    return os.getcwdb().decode("utf-8") + "/subgraphs/subgraphs/{}/src/".format(path)


class OpenAIService:

    """
    Service that runs calls to OpenAI to generate the GraphQL
    Printing output to the console for now to get visibility into what is being returned.
    
    """
    def __init__(self, use_prompt=0):
        openai.api_key = OPENAI_API_KEY

    def request_gql_for_graph_llama(self, input_query, subgraph):
        # import regex as re
        if subgraph == 'Solana Blockchain':
            examples = os.getcwdb().decode("utf-8")+ "/backend/services/openAI/prompts/SolanaExamples.py"
            documents = SimpleDirectoryReader(
                input_dir=examples, input_files=[examples], recursive=True
            ).load_data()
        else:
            graph_service = GraphService(protocol=subgraph)
            schema = os.path.join(
                os.getcwdb().decode("utf-8"), graph_service.subgraph.schema_file_location
            )
            mappings = mapping_path(graph_service.subgraph.deployments["base"])
            documents = SimpleDirectoryReader(
                input_dir=mappings, input_files=[schema], recursive=True
            ).load_data()

        # define LLM
        print("==========openai training:==========")
        llm_predictor = LLMPredictor(
            llm=OpenAI(temperature=0, model_name="text-davinci-003")
        )

        # define prompt helper
        # set maximum input size
        max_input_size = 4096
        # set number of output tokens
        num_output = 256
        # set maximum chunk overlap
        max_chunk_overlap = 20
        prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

        index = GPTSimpleVectorIndex(
            documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
        )

        prompt = GraphPromptFactory(subgraph).build_prompt_for_subgraph(input_query)
        response = index.query(prompt)

        openai_result = response.response
        print("==========openai response:==========\n", openai_result)
        # strip any unnecessary text prepended and/or postpended to the gql query
        openai_result = openai_result[
            openai_result.find("{") : openai_result.rfind("}") + 1
        ]
        print("==========openai response (formatted):==========\n", openai_result)
        return openai_result