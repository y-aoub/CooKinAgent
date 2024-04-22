# Data Processing

- [ ] Get the data from : [Food.com Recipes and User Interactions Dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?resource=download&select=RAW_recipes.csv)
- [ ] Add reviews to the data (could be a good asset) for our RAG
- [ ] Get rid of unuseful columns
- [ ] Remove rows with missing names
- Format the data:
	- [ ] Format time in a human-readable format
	- [ ] Extract entities relative to countries and regions from tags
	- [ ] Format steps
	- [ ] Format ingredients
	- [ ] Format nutrition
	- [ ] Format reviews
	- [ ] Compute and add a mean rating for each row
- [ ] Format the data into documents (1 row = 1 document, and name as source)
- [ ] Splitting data into documents
- [ ] Perform embedding
- [ ] Storing in ChromaDB data as vectors

# API Calls

- [ ] Test API calls OpenAI
- [ ] Test API calls (see doc: [wttr.in GitHub](https://github.com/chubin/wttr.in))
