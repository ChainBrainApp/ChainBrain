## Cmds to Spin up Sutime Docker for API Request

cd into sutime-time-ner folder in `models`
`docker build -t sutime-flask .`
`docker run -d -p 5001:5001 sutime-flask`

To make a request:
```
curl -X POST http://0.0.0.0:5001/time -H 'Content-Type: application/json' -d '{"query": "What was the most expensive NFT sold tive weeks ago?"}'
```
Note -- the content-type as well as the structure for the data is required

To confirm container is up:
Navigate to http://127.0.0.1:5001/ in a browser