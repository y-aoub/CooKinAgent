# Data Processing

- [x] Get the data from : [Food.com Recipes and User Interactions Dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?resource=download&select=RAW_recipes.csv)
- [x] Set a script to download data (with dynamic paths)
- [x] Add reviews to the data (could be a good asset) for our RAG
- [x] Get rid of unuseful columns
- [x] Remove rows with missing names
- [x] Format the data:
	- [x] Format time in a human-readable format
	- [x] Extract entities relative to countries and regions from tags
	- [x] Format steps
	- [x] Format ingredients
	- [x] Format nutrition
	- [x] Format reviews
	- [x] Compute and add a mean rating for each row
- [ ] Format the data into documents (1 row = 1 document, and name as source)
- [ ] Splitting data into documents
- [ ] Perform embedding
- [ ] Storing in ChromaDB data as vectors

# API Calls

- [ ] Test API calls OpenAI
- [ ] Test API calls (see doc: [wttr.in GitHub](https://github.com/chubin/wttr.in))
