from transformers import AutoTokenizer, AutoModel
import torch

class CustomEmbedder:
    def __init__(self, model_name):
        """
        Initializes the tokenizer and model based on the specified model name.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
    
    def get_text_embedding_batch(self, texts, **kwargs):
        """
        Generates embeddings for a batch of texts, now accepting arbitrary keyword arguments.

        Args:
        - texts (list of str): The texts to embed.

        Returns:
        - A torch.Tensor of embeddings.
        """
        # Check for 'show_progress' in kwargs and handle it if necessary
        # For now, we'll ignore it since it's not applicable to our embedding method
        show_progress = kwargs.get('show_progress', False)

        # Ensure the model is in evaluation mode
        self.model.eval()

        # Tokenize the texts and move to the correct device
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt').to(self.device)
        
        # Perform the embedding
        with torch.no_grad():
            outputs = self.model(**encoded_input)
            # let's use the mean of the last hidden state as the embedding
            embeddings = outputs.last_hidden_state.mean(dim=1)

        return embeddings
