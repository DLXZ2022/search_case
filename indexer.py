import faiss
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch
from transformers import BertTokenizer, BertModel


class Indexer:
    def __init__(self, model_name='uer/roberta-base-finetuned-chinanews-chinese', batch_size=8):
        # 检查是否可以使用CUDA
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name).to(self.device)
        self.index = faiss.IndexFlatL2(768)  # BERT的向量大小为768
        self.batch_size = batch_size
        self.url_mapping = []  # 存储每个向量对应的URL

    def texts_to_vectors(self, texts):
        vectors = []
        for i in tqdm(range(0, len(texts), self.batch_size)):
            batch_texts = texts[i:i + self.batch_size].tolist()
            inputs = self.tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.model(**inputs)
            batch_vectors = outputs.pooler_output.detach().cpu().numpy()
            vectors.extend(batch_vectors)
        return np.array(vectors)

    def add_to_index(self, texts, urls):
        vectors = self.texts_to_vectors(texts)
        self.index.add(vectors)
        self.url_mapping.extend(urls)

    def save_index_and_mapping(self, index_path, mapping_path):
        faiss.write_index(self.index, index_path)
        with open(mapping_path, 'w', encoding='utf-8') as f:
            for url in self.url_mapping:
                f.write(url + '\n')

    def build_index_from_csv(self, csv_file_path):
        df = pd.read_csv(csv_file_path)[:1000] # 为了演示这里只选取了1000条数据
        self.add_to_index(df['content'], df['url'])

if __name__=="__main__":
    # 示例用法
    indexer = Indexer()
    indexer.build_index_from_csv('./data/wiki_zh.csv')  # 假设CSV文件路径
    indexer.save_index_and_mapping('./data/wiki_zh.index', './data/wiki_map.txt')
