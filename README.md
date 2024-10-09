# gemma_rag
building a RAG locally using timescale db and gemma 2b

### Steps to setup

#### Step 1
Run docker to setup your timescale db
`docker-compose up`

#### Step 2
Install the python dependencies using 
`pip install -r requirements.txt`

#### Step 3
Make sure to install pgai extension if not enabled in timescale db
`CREATE EXTENSION IF NOT EXISTS ai CASCADE;`

to see the list of installed extensions 
`SELECT * FROM pg_extension;`