import os
from backend.services.graph.service import GraphService
from backend.services.openAI.service import OpenAIService
import matplotlib.pyplot as plt
import json
import pandas as pd 
import numpy as np
# from AutoClean import AutoClean
from autoviz.AutoViz_Class import AutoViz_Class
import datetime as dt
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

# data = json.load(open('sampledata.json'))
# df = pd.DataFrame(data['data']['voteDailySnapshots'])
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from datetime import datetime

SCHEMA = """
type DelegateChange @entity(immutable: true) {
  "Unique entity used to keep track of delegate changes"
  id: ID!
  "Token addresss"
  tokenAddress: String
  "Token address for delegator"
  delegator: String!
  "Token address for delegate"
  delegate: String!
  "Token address for previous delegate"
  previousDelegate: String!
  "Block time change happened"
  blockTimestamp: BigInt!
  "Transaction hash of the delegate change event"
  txnHash: String!
  "Log index for delegate change"
  logIndex: BigInt!
  "Block number of event"
  blockNumber: BigInt!
}

type DelegateVotingPowerChange @entity(immutable: true) {
  "Unique entity used to keep track of voting power delta"
  id: ID!
  "Token addresss"
  tokenAddress: String
  "Token address for delegate"
  delegate: String!
  "Previous voting power of delegate"
  previousBalance: BigInt!
  "New voting power of delegate"
  newBalance: BigInt!
  "Block time change happened"
  blockTimestamp: BigInt!
  "Transaction hash of the voting power change"
  txnHash: String!
  "Log index for delegate voting power change"
  logIndex: BigInt!
  "Block number of event"
  blockNumber: BigInt!
}

type Governance @entity {
  "Unique entity used to keep track of common aggregated data"
  id: ID!

  "Total Supply of token"
  totalTokenSupply: BigInt!
  "Total number of token holders currently"
  currentTokenHolders: BigInt!
  "Total number of token holders"
  totalTokenHolders: BigInt!
  "Total number of delegates participating on the governance currently"
  currentDelegates: BigInt!
  "Total number of delegates that held delegated votes"
  totalDelegates: BigInt!
  "Total number of votes delegated expressed in the smallest unit of the token"
  delegatedVotesRaw: BigInt!
  "Total number of votes delegated expressed as a BigDecimal normalized value for the token"
  delegatedVotes: BigDecimal!

  "Total number of proposals created"
  proposals: BigInt!
  "Number of proposals currently queued for execution"
  proposalsQueued: BigInt!
  "Number of proposals currently executed"
  proposalsExecuted: BigInt!
  "Number of proposals currently canceled"
  proposalsCanceled: BigInt!
}

type GovernanceFramework @entity {
  "Governance framework contract address"
  id: String!
  "Name of the governance framework"
  name: String!
  "Type of governance framework"
  type: GovernanceFrameworkType!
  "Version of the governance framework"
  version: String!

  "Governance framework contract address"
  contractAddress: String!
  "The contract address associated with the governance token used for voting on the governance framework proposals"
  tokenAddress: String!
  "The contract address associated with the contract that manages the delay of administrative actions for the governance framework"
  timelockAddress: String!

  "The delay before voting on a proposal may take place in blocks"
  votingDelay: BigInt!
  "The duration of voting on a proposal in blocks"
  votingPeriod: BigInt!
  "The number of votes required in order for a voter to become a proposer"
  proposalThreshold: BigInt!

  "The number of votes for a proposal to succeed."
  quorumVotes: BigInt
  "Quorum fraction numerator value. (OZ: quorum = totalSupply * numerator / denominator)"
  quorumNumerator: BigInt
  "Quorum fraction denominator value. (OZ: quorum = totalSupply * numerator / denominator)"
  quorumDenominator: BigInt
}

enum GovernanceFrameworkType {
  GovernorAlpha
  GovernorBravo
  OZGovernor
  AaveGovernanceV2
}

type Proposal @entity {
  "Internal proposal ID, in this implementation it seems to be a autoincremental id"
  id: ID!
  "Transaction hash of the proposal creation"
  txnHash: String!
  "Proposal description in markdown format"
  description: String!
  "Governance Framework that proposal is part of"
  governanceFramework: GovernanceFramework!

  "Delegate that proposed the proposal"
  proposer: Delegate!
  "State of the proposal"
  state: ProposalState!
  "The number of votes for a proposal to succeed."
  quorumVotes: BigInt!
  "Number of tokenholders at start of voting"
  tokenHoldersAtStart: BigInt!
  "Number of delegates at start of voting"
  delegatesAtStart: BigInt!

  "Number of delegates that voted against the proposal"
  againstDelegateVotes: BigInt!
  "Number of delegates that voted for the proposal"
  forDelegateVotes: BigInt!
  "Number of delegates that voted abstain to the proposal"
  abstainDelegateVotes: BigInt!
  "Total number of delegates that voted on the proposal"
  totalDelegateVotes: BigInt!

  "Weighted votes against the proposal"
  againstWeightedVotes: BigInt!
  "Weighted votes for the proposal"
  forWeightedVotes: BigInt!
  "Weighted votes abstaining to the proposal"
  abstainWeightedVotes: BigInt!
  "Total weighted for/against/abstaining votes"
  totalWeightedVotes: BigInt!

  "Votes associated to this proposal"
  votes: [Vote!]! @derivedFrom(field: "proposal")

  "Block number proposal was created in"
  creationBlock: BigInt!
  "Timestamp of block proposal was created in"
  creationTime: BigInt!
  "Block number from where the voting starts"
  startBlock: BigInt!
  "Block number from where the voting ends"
  endBlock: BigInt!
  "Transaction hash of the proposal being queued"
  queueTxnHash: String
  "Block number proposal was queued in"
  queueBlock: BigInt
  "Timestamp of block proposal was queued in"
  queueTime: BigInt
  "Once the proposal is queued for execution it will have an ETA of the execution"
  executionETA: BigInt
  "Transaction hash of the proposal execution"
  executionTxnHash: String
  "Block number proposal was executed in"
  executionBlock: BigInt
  "Timestamp of block proposal was executed in"
  executionTime: BigInt
  "Transaction hash of the proposal cancellation"
  cancellationTxnHash: String
  "Block number proposal was canceled in"
  cancellationBlock: BigInt
  "Timestamp of block proposal was canceled in"
  cancellationTime: BigInt

  "Targets data for the change"
  targets: [String!]
  "Values data for the change"
  values: [BigInt!]
  "Signature data for the change"
  signatures: [String!]
  "Call data for the change"
  calldatas: [Bytes!]
}

enum ProposalState {
  PENDING
  ACTIVE
  CANCELED
  DEFEATED
  SUCCEEDED
  QUEUED
  EXPIRED
  EXECUTED
}

type Vote @entity(immutable: true) {
  "Delegate ID + Proposal ID"
  id: ID!
  "Whether the vote is in favour, against or abstaining to the proposal"
  choice: VoteChoice!
  "Voting weight expressed in the vote"
  weight: BigInt!
  "Reason for voting choice"
  reason: String
  "Delegate that emitted the vote"
  voter: Delegate!
  "Proposal that is being voted on"
  proposal: Proposal!

  "Block number vote is cast in"
  block: BigInt!
  "Timestamp of block vote was cast in"
  blockTime: BigInt!
  "Transaction hash of the vote"
  txnHash: String!
  "Log index for the event"
  logIndex: BigInt!
  "Unique ID based on the blockTime and logIndex"
  blockTimeId: String!
}

enum VoteChoice {
  FOR
  AGAINST
  ABSTAIN
}

type TokenHolder @entity {
  "A TokenHolder is any address that holds any amount of tokens, the id used is the blockchain address."
  id: String!
  "Delegate address of the token holder which will participate in votings. Delegates don't need to hold any tokens and can even be the token holder itself."
  delegate: Delegate

  "Token balance of this address expressed in the smallest unit of the token"
  tokenBalanceRaw: BigInt!
  "Token balance of this address expressed as a BigDecimal normalized value"
  tokenBalance: BigDecimal!
  "Total amount of tokens ever held by this address expressed in the smallest unit of the token"
  totalTokensHeldRaw: BigInt!
  "Total amount of tokens ever held by this address expressed as a BigDecimal normalized value"
  totalTokensHeld: BigDecimal!
}

type Delegate @entity {
  "A Delegate is any address that has been delegated with voting tokens by a token holder, id is the blockchain address of said delegate"
  id: String!

  "Amount of votes delegated to this delegate to be used on proposal votings expressed in the smallest unit of the token"
  delegatedVotesRaw: BigInt!
  "Amount of votes delegated to this delegate to be used on proposal votings expressed as a BigDecimal normalized value"
  delegatedVotes: BigDecimal!

  "Total token holders that this delegate represents"
  tokenHoldersRepresentedAmount: Int!
  "Token holders that this delegate represents"
  tokenHoldersRepresented: [TokenHolder!]! @derivedFrom(field: "delegate")

  "Votes that a delegate has made in different proposals"
  votes: [Vote!]! @derivedFrom(field: "voter")
  "Number of proposals voted on"
  numberVotes: Int!

  "Proposals that the delegate has created"
  proposals: [Proposal!]! @derivedFrom(field: "proposer")
}

# Timeseries Data
type TokenDailySnapshot @entity {
  "Number of days from Unix epoch time"
  id: ID!
  "Total Supply at snapshot"
  totalSupply: BigInt!
  "Number of tokenholders at snapshot"
  tokenHolders: BigInt!
  "Number of delegates at snapshot"
  delegates: BigInt!
  "Block number of last block in snapshot"
  blockNumber: BigInt!
  "Timestamp of snapshot"
  timestamp: BigInt!
}

type VoteDailySnapshot @entity {
  "Number of days from Unix epoch time"
  id: ID!
  "Proposal this snapshot is associated with"
  proposal: Proposal!
  "Weighted votes against the proposal at snapshot"
  forWeightedVotes: BigInt!
  "Weighted votes abstaining to the proposal at snapshot"
  againstWeightedVotes: BigInt!
  "Weighted votes for the proposal at snapshot"
  abstainWeightedVotes: BigInt!
  "Total weighted for/against/abstaining votes at snapshot"
  totalWeightedVotes: BigInt!
  "Block number of last block in snapshot"
  blockNumber: BigInt!
  "Timestamp of snapshot"
  timestamp: BigInt!
}
"""

PROMPT="""
You are an AI that helps write GraphQL queries on the Graph Protocol. Generate 10 GraphQL queries that work along with their questions for the following graphql schema. Show only code and do not use sentences. Note that it's important that if you don't have some specific data (like dates or IDs), just add placeholders.

"""

ai = OpenAIService()
subgraph="compound-governance"
# from pathlib import Path
# # contents = Path(SCHEMA).read_text()
# graph_service = GraphService(protocol=subgraph)
# schema = os.path.join(os.getcwdb().decode("utf-8"), graph_service.subgraph.schema_file_location)
ai.request_gql_for_graph_llama(PROMPT+SCHEMA, subgraph=subgraph)

# data = json.load(open('sampledata.json'))
# print(data)
# df = pd.DataFrame(data['data']['voteDailySnapshots'])
# Loop through each column in the DataFrame

# ai = OpenAIService()
# ai.request_gql_for_graph(PROMPT, subgraph='compound-governance')
# print(ai.request_gql_for_graph(PROMPT, subgraph='compound-governance'))



# for col in df.columns:
#     # Convert values to integers if possible
#     if df[col].dtype == 'object' and df[col].str.isnumeric().all():
#         try:
#             df[col] = df[col].astype(np.int64)
#         except:
#             df[col] = df[col].astype(float)

#     # Convert values to datetime objects if possible
#     elif df[col].dtype == 'object':
#         print('in elif')
#         try:
#             print('in try')
#             df[col] = dt.datetime.utcfromtimestamp(int(df[col])).strftime(
#                             "%Y-%m-%d %H:%M:%S"
#                         )
#         except ValueError:
#             pass
# AV = AutoViz_Class()
# # AV.AutoViz(filename = 'data_to_csv_test.csv', sep = ",")
# # sep = ","
# dft = AV.AutoViz(
#     filename = '/Users/marissaposner/ethdenver-buidlathon-2023/backend/backend/services/graph/data_to_csv_test.csv',
#     sep=",",
#     depVar="",
#     dfte=None,
#     header=0,
#     verbose=0,
#     lowess=False,
#     chart_format="svg",
#     max_rows_analyzed=150000,
#     max_cols_analyzed=30,
#     save_plot_dir=None
# )