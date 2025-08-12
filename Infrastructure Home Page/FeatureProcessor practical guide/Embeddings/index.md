# Embeddings
The Embeddings tool set is designed to allow generation of strong features embedding a very large feature space into a much smaller dimension, and giving the tools to train these Embeddings, and to use them as a feature generator within the InfraStructure.
The general plan is the following:

1. Define the (large) feature set (use the embed_params many options for that, see below)
2. Create x,y matrices to train the embedding : this will also create the .scheme file which is the recipe file of how to create a line in the x matrix - this will be needed later.
3. Train the embedding using Keras (Embedder.py script) : this will also set the dimension of the embedding.
4. Use the .scheme file and the keras layers file to define embedded features to be generated on your prediction problem - the new embedded features will be added to your train/test matrices, the .scheme and layers information will be serialized into your trained model.
 
We will cover the technical details of how to perform each of the steps above, and also take a look at the Embedding WalkThrough Example page to see an actual example.
 
