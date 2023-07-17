from backend.services.openAI.graph_prompt import GraphPromptBase as Prompt


EXAMPLES = [
    Prompt(
        q="What date were the most NFTs in the Bored Ape NFT collection traded (collection id = '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d')?",
        o="""query {
          collectionDailySnapshots(
              where: {collection: "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"}
              first: 1
              orderBy: dailyTradeVolumeETH
              orderDirection: desc
          ) {
              blockNumber
              dailyTradeVolumeETH
              timestamp
          }
        }""",
    ),
    Prompt(
        q="Queries the Bored Ape NFT collection and finds the date with the highest daily trade volume in ETH. \n\nThe timestamp is the number of days since the Unix epoch (basically the Unix timestamp, divided by 86400).",
        o="""query {
          marketplaceDailySnapshots(orderBy: timestamp, orderDirection: desc) {
            cumulativeTradeVolumeETH
            dailyTradedItemCount
            dailyTradedCollectionCount
            timestamp
          }
        }""",
    ),
    Prompt(
        q="How many NFT collections have a volume above 100000 eth?",
        o="""query {
          collections(where: {cumulativeTradeVolumeETH_gt: 100000}) {
            id
            cumulativeTradeVolumeETH
          }
        }""",
    ),
    Prompt(
    q="show the volume of all trades by day",
    o="""query {
      marketplaceDailySnapshots {
        cumulativeTradeVolumeETH
        dailyTradedItemCount
        dailyTradedCollectionCount
        timestamp
      }
    }"""),
    Prompt(
        q="What date were the most NFTs in the Degods NFT collection traded (collection id = '0xa45D808eAFDe8B8E6B6B078fd246e28AD13030E8')?",
        o="""query {
          collectionDailySnapshots(
              where: {collection: "0xa45D808eAFDe8B8E6B6B078fd246e28AD13030E8"}
              first: 1
              orderBy: dailyTradeVolumeETH
              orderDirection: desc
          ) {
              blockNumber
              dailyTradeVolumeETH
              timestamp
          }
        }""",
    ),
]
