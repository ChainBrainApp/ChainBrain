## Cmds to Spin up Sutime Docker with Open Jupyter Notebook

`docker build -t sutime .`
`docker run -it -p 8888:8888 --ip=0.0.0.0 sutime`

Once inside the docker container run
`jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root`
and click the link to the jupyter notebook url

Cmds for jupyter notebook 

```
import json
from sutime import SUTime
import os

test_case = 'I need a desk for tomorrow from 2pm to 3pm'

jar_files = "./jars/"
sutime = SUTime(jars=jar_files, mark_time_ranges=True, include_range=True)
print(json.dumps(sutime.parse(test_case), sort_keys=True, indent=4))

cb_q1 = "What was the most expensive NFT sold last week?"
cb_q1a = "What was the highest price of Bitcoin sold last week?"
cb_q2 = "On what date were the most NFTs in the Bored Ape NFT collection traded?"
cb_q3 = "What was the most expensive NFT sold May 3 - May 11?"
cb_q4 = "What was the most expensive NFT sold may 3 - may 11?"
cb_q5 = "What was the most expensive NFT sold yesterday?"
cb_q6 = "What was the most expensive NFT sold in the last 3 hours?"
cb_q6b = "What was the most expensive NFT sold from 05:00 to 14:00 today?"
cb_q6c = "What was the most expensive NFT sold after 08:00:00 EST on 1 January 1970?"
cb_q6d = "What was the most expensive NFT sold in the last 3 hours today?"

query = cb_q1
print(query)
print(json.dumps(sutime.parse(query), sort_keys=True, indent=4))
```