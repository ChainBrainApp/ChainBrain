from backend.services.openAI.graph_prompt import GraphPromptBase as Prompt


EXAMPLES = [

Prompt(
q="Who are the top delegates by voting power?",
o="""query{
  votes(orderBy: voter__tokenHoldersRepresentedAmount, orderDirection: desc) {
    voter {
      tokenHoldersRepresentedAmount
      id
    }}}
    """),
Prompt(
q="How many votes did proposal 11 have?",
o="""query{
  proposals(where: {id: "11"}) {
    abstainWeightedVotes
    againstWeightedVotes
    forWeightedVotes
  }
}"""),
Prompt(
q="Query: What was the voting timeline for Against, For, and Abstain votes for proposal 11?",
o="""query {
  voteDailySnapshots(
    where: {proposal_: {id: "11"}
    }
    orderBy: timestamp
    orderDirection: desc
  ) {
    blockNumber
    abstainWeightedVotes
    againstWeightedVotes
    forWeightedVotes
    timestamp
    proposal {
      id
    }
  }
}"""),

Prompt(
q="What were the results for Proposal 86?",
o="""query{
  proposals(where: {id: "86"}) {
    abstainWeightedVotes
    againstWeightedVotes
    forWeightedVotes
  }
}"""),

Prompt(
q="Summarize Proposal with ID = 86?",
o="""query {
  proposal(id: "86") {
    description
    state
    quorumVotes
    tokenHoldersAtStart
    delegatesAtStart
    againstDelegateVotes
    forDelegateVotes
    abstainDelegateVotes
    totalDelegateVotes
    againstWeightedVotes
    forWeightedVotes
    abstainWeightedVotes
    totalWeightedVotes
    governanceFramework {
      id
      name
      type
      version
    }
  }
}
""")
]
