import torch
from tqdm import tqdm
import os
import requests
import numpy as np
from transformers import RobertaTokenizer
from src.model.config import Config
from src.model.greetentity import AbstractGreetEntity

class Classifier:
    """
      Class for text classification using a pre-trained model.
      It utilizes the alBERTo model and the RobertaTokenizer.
    """
  
    __MODEL_URL = "https://huggingface.co/mantra-coding/alBERTo/resolve/main/alBERTo-v1.0.0"
	
    def __init__(self, config: Config = None):
      """
        Constructor for the Classifier class.
        
        Args:
          config (Config, optional): Project configuration (to eventually specify a model version). Default: None.
      """
      self.__tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base', do_lower_case=True)
      self.__device = torch.device('cpu')

      model_path = os.path.join(os.path.expanduser("~"), ".greet", 'greet')
      if os.path.exists(model_path):
          self.__model = torch.load(model_path, map_location=torch.device('cpu'))
      else:
          try: 
            os.mkdir(os.path.join(os.path.expanduser("~"), ".greet"))
          except OSError as error:
            print(error)
          self.__download_model(model_path)
    
    def __download_model(self, model_path):
      """
      Download the model file if it doesn't exist.

      Args:
          model_path (str): Path to save the model file.
      """
      response = requests.get(self.__MODEL_URL, stream=True)
      if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        chunk_size = 1024
        mb_factor = 1024 * 1024  # Conversion factor from bytes to megabytes
        total_size_mb = total_size / mb_factor
        
        print("Model download progress:")
        with open(model_path, 'wb') as file, tqdm(
            desc=f"Downloading model ({total_size_mb:.2f} MB)",
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_bar.update(len(chunk))
        print("Download complete!")
        self.__model = torch.load(model_path, map_location=torch.device('cpu'))
      else:
          raise Exception("Failed to download the model file.")

    def __preprocess_text(self, text: str):
        """
          Returns <class transformers.tokenization_utils_base.BatchEncoding> with the following fields:
          - input_ids: list of token ids
          - token_type_ids: list of token type ids
          - attention_mask: list of indices (0,1) specifying which tokens should considered by the model (return_attention_mask = True).
        """
        return self.__tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=150,
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
    
    def predict(self, entity: AbstractGreetEntity):
      """
        Predicts the class label for the given entity.
        
        Args:
          entity (AbstractGreetEntity): The entity to classify.
        
        Returns:
          int: The predicted class label.
      """
      encoding = self.__preprocess_text(entity.getString())
      predict_ids = []
      predict_attention_mask = []
      # Extract IDs and Attention Mask
      predict_ids.append(encoding['input_ids'])
      predict_attention_mask.append(encoding['attention_mask'])
      predict_ids = torch.cat(predict_ids, dim=0)
      predict_attention_mask = torch.cat(predict_attention_mask, dim=0)
      with torch.no_grad():
          output = self.__model(predict_ids.to(self.__device), token_type_ids=None,
                                attention_mask=predict_attention_mask.to(self.__device))
          prediction = np.argmax(
              output.logits.cpu().numpy()).flatten().item()
      return prediction
    
greetClassifier = Classifier()