NFT_Marketplace = """
# Defines the network the NFT was minted on
enum Network {
  ARBITRUM_ONE
  ARWEAVE_MAINNET
  AURORA
  AVALANCHE
  BOBA
  BSC # aka BNB Chain
  CELO
  COSMOS
  CRONOS
  MAINNET # Ethereum Mainnet
  FANTOM
  FUSE
  HARMONY
  JUNO
  MOONBEAM
  MOONRIVER
  NEAR_MAINNET
  OPTIMISM
  OSMOSIS
  MATIC # aka Polygon
  GNOSIS
}
# defines the standard of the NFT
enum NftStandard {
  ERC721
  ERC1155
  UNKNOWN
}

enum SaleStrategy {
  " Strategy that executes an order at a fixed price that can be taken either by a bid or an ask. "
  FIXED_PRICE

  " Strategy that executes an order at a fixed price that can be matched by any tokenId for the collection. "
  ANY_ITEM_FROM_COLLECTION

  " Strategy that executes an order at a fixed price that can be matched by any tokenId in a set of tokenIds. "
  ANY_ITEM_FROM_SET

  " Strategy to launch a Dutch Auction for a token where the price decreases linearly until a specified timestamp and end price defined by the seller. "
  DUTCH_AUCTION

  " Strategy to set up an order that can only be executed by a specific address. "
  PRIVATE_SALE

  " Other type of sale strategy. "
  UNKNOWN
}

type Marketplace @entity {
  " Smart contract address of the protocol's main contract (Factory, Registry, etc) "
  id: ID!

  " Name of the NFT marketplace, for example OpenSea. "
  name: String!

  " Slug of the NFT marketplace, for example OpenSea. "
  slug: String!

  " The blockchain network this subgraph is indexing on. "
  network: Network!

  " Version of the subgraph schema, in SemVer format (e.g. 1.0.0) "
  schemaVersion: String!

  " Version of the subgraph implementation, in SemVer format (e.g. 1.0.0) "
  subgraphVersion: String!

  " Version of the methodology used to compute metrics, loosely based on SemVer format (e.g. 1.0.0) "
  methodologyVersion: String!

  " Number of collections listed on the marketplace. "
  collectionCount: Int!

  " Trade count of the all collections on the marketplace. "
  tradeCount: Int!

  " Cumulative trade volume (in ETH) "
  cumulativeTradeVolumeETH: BigDecimal!

  " Revenue in ETH that goes to the marketplace protocol, aka protocol fee. "
  marketplaceRevenueETH: BigDecimal!

  " Revenue in ETH that goes to creator, aka royalty fee. "
  creatorRevenueETH: BigDecimal!

  " Sum of marketplaceRevenueETH and creatorRevenueETH. "
  totalRevenueETH: BigDecimal!

  " Cumulative unique traders. "
  cumulativeUniqueTraders: Int!

  " Trades on the marketplace. "
  trades: [Trade!]! @derivedFrom(field: "marketplace")

  " Marketplace collections. "
  collections: [Collection!]! @derivedFrom(field: "marketplace")

  " Marketplace daily snapshots. "
  snapshots: [MarketplaceDailySnapshot!]! @derivedFrom(field: "marketplace")
}

type Collection @entity {
  " Contract address. "
  id: ID!

  " Collection name, mirrored from the smart contract. Leave null if not available. "
  name: String

  " Collection symbol, mirrored from the smart contract. Leave null if not available. "
  symbol: String

  " NFT Standard the collection uses. "
  nftStandard: NftStandard!

  " Marketplace that this collection was traded in. "
  marketplace: Marketplace!

  " Royalty fee rate in percentage. E.g. 2.5% should be 2.5 "
  royaltyFee: BigDecimal!

  " Cumulative trade volume (in ETH) "
  cumulativeTradeVolumeETH: BigDecimal!
  
  " Revenue in ETH that goes to the marketplace protocol, aka protocol fee. "
  marketplaceRevenueETH: BigDecimal!
  
  " Revenue in ETH that goes to creator, aka royalty fee. "
  creatorRevenueETH: BigDecimal!

  " Sum of marketplaceRevenueETH and creatorRevenueETH. "
  totalRevenueETH: BigDecimal!

  " Trade count of the collection on the marketplace. "
  tradeCount: Int!

  " Buyer count. "
  buyerCount: Int!

  " Seller count. "
  sellerCount: Int!

  " Trades of the collection. "
  trades: [Trade!]! @derivedFrom(field: "collection")

  " Collection daily snapshots. "
  snapshots: [CollectionDailySnapshot!]! @derivedFrom(field: "collection")
}

" Trades exist such as a combination of taker/order and bid/ask. "
type Trade @entity {
  " { Transaction hash }-{ Log index }-{ (optional) ID within bundle } "
  id: ID!

  " Event transaction hash. "
  transactionHash: String!

  " Event log index. "
  logIndex: Int!

  " Block timestamp where the trade is executed. "
  timestamp: BigInt!

  " Block number where the trade is executed. "
  blockNumber: BigInt!

  " Whether the trade is in a bundle. "
  isBundle: Boolean!

  " Collection involved. "
  collection: Collection!

  " Marketplace involved. "
  marketplace: Marketplace!

  " Token ID of the traded NFT. "
  tokenId: BigInt!

  " The amount of token to transfer. It is set at 1 except for ERC1155 batch. "
  amount: BigInt!

  " Price (in ETH). If only 1 tokenId is involved, then the price is determined by the token only. If the trade is incurred by a batch purchasing (available in x2y2), then the price is the average price in the batch. "
  priceETH: BigDecimal!
  
  " Stretegy that the trade is executed. "
  strategy: SaleStrategy!

  " Buyer account address. "
  buyer: String!

  " Seller account address. "
  seller: String!
}

type MarketplaceDailySnapshot @entity {
  " { Contract address }-{# of days since Unix epoch time} "
  id: ID!

  " The marketplace that this snapshot belongs to. "
  marketplace: Marketplace!

  " Block number where the snapshot is taken. "
  blockNumber: BigInt!

  " Block timestamp when the snapshot is taken. "
  timestamp: BigInt!

  " Number of collections listed on the marketplace. "
  collectionCount: Int!

  " Cumulative trade volume (in ETH) "
  cumulativeTradeVolumeETH: BigDecimal!
  

  " Revenue in ETH that goes to the marketplace protocol, aka protocol fee. "
  marketplaceRevenueETH: BigDecimal!
  
  " Revenue in ETH that goes to creator, aka royalty fee. "
  creatorRevenueETH: BigDecimal!

  " Sum of marketplaceRevenueETH and creatorRevenueETH. "
  totalRevenueETH: BigDecimal!

  " Trade count of the all collections on the marketplace. "
  tradeCount: Int!

  " Cumulative unique traders. "
  cumulativeUniqueTraders: Int!

  " Daily active traders. "
  dailyActiveTraders: Int!

  " Number of traded collections of the day. "
  dailyTradedCollectionCount: Int!

  " Number of traded items of the day. "
  dailyTradedItemCount: Int!
}

type CollectionDailySnapshot @entity {
  " { Contract address }-{# of days since epoch unix time } "
  id: ID!

  " The collection that this snapshot belongs to. "
  collection: Collection!

  " Block number where the snapshot is taken. "
  blockNumber: BigInt!

  " Block timestamp when the snapshot is taken. "
  timestamp: BigInt!

  " Royalty fee rate in percentage. E.g. 2.5% should be 2.5 "
  royaltyFee: BigDecimal!

  " Minimum sale price of the day (in ETH) "
  dailyMinSalePriceETH: BigDecimal!
  
  " Maximum sale price of the day (in ETH) "
  dailyMaxSalePriceETH: BigDecimal!
  
  " Cumulative trade volume (in ETH) "
  cumulativeTradeVolumeETH: BigDecimal!
  
  " Revenue in ETH that goes to the marketplace protocol, aka protocol fee. "
  marketplaceRevenueETH: BigDecimal!
  
  " Revenue in ETH that goes to creator, aka royalty fee. "
  creatorRevenueETH: BigDecimal!
  
  " Sum of marketplaceRevenueETH and creatorRevenueETH. "
  totalRevenueETH: BigDecimal!
  
  " Trade count of the collection on the marketplace. "
  tradeCount: Int!

  " Number of traded items of the day. "
  dailyTradedItemCount: Int!
}"""