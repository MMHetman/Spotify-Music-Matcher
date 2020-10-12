import json
import requests
import numpy as np


class BaseModel:
    def embed(self, input_tensor):
        pass

    def get_embedding_file(self):
        pass


class TensorFlowModelReflection(BaseModel):
    def __init__(self, model_address, embedding_file):
        self.embedding_file = embedding_file
        self.model_address = model_address

    def embed(self, input_tensor):
        data = json.dumps({
            'instances': input_tensor.tolist()
        })

        response = requests.post(self.model_address + ':predict', data=data.encode('utf-8'))
        return np.mean(response.json()['predictions'], axis=0)

    def get_embedding_file(self):
        return self.embedding_file
