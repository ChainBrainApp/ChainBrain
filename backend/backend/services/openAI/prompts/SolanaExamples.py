from backend.services.openAI.graph_prompt import GraphPromptBase as Prompt


EXAMPLES = [

Prompt(
q="What are the top currencies on Solana?",
o="""{
  solana{
    transfers(
      options: {limit: 10, desc: "count", asc: "currency.symbol"}
      date: {since: "2021-01-01"}
    ){
      count
      currency{
        name
        symbol
      }
      senders: count(uniq: sender_address)
      receivers: count(uniq: receiver_address)
      from_date: minimum(of: date)
      till_date: maximum(of: date)
      amount
    }
  }
}
    """),
Prompt(
q="What is the frequency of token transfers?",
o="""{
  solana(network: solana) {
    transfers(options: {asc: "date.month"}, date: {since: "2021-01-01"}) {
      date {
        month
        year
      }
      count
    }
  }
}
"""),
Prompt(
q="What was the latest block?",
o="""
{
solana{
blocks(date: {since: "2021-08-13"}, options: {asc: "time.iso8601"}){
height
blockHash
transactionCount
time{
iso8601
}}
}}
""")
]
