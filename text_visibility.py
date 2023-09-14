import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# 載入spaCy的英文模型
nlp = spacy.load("en_core_web_sm")

# 讀取文件
docs = []
folder_path = 'audio_text'
for file_name in os.listdir(folder_path):
    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
        content = file.read()
        docs.append(content)

# 使用spaCy進行分詞和前處理
def tokenizer(text):
    return [token.lemma_ for token in nlp(text) if not token.is_stop and token.is_alpha]

vectorizer = TfidfVectorizer(tokenizer=tokenizer, max_df=0.85, min_df=2, max_features=1000)
tfidf_matrix = vectorizer.fit_transform(docs)

# 使用NMF (Non-negative Matrix Factorization) 進行主題建模
num_topics = 10  # 改成十個主題
nmf_model = NMF(n_components=num_topics)
nmf_topic_matrix = nmf_model.fit_transform(tfidf_matrix)

# 儲存結果到txt檔案
output_file = "topics_output.txt"
with open(output_file, 'w', encoding='utf-8') as file:
    for topic_idx, topic in enumerate(nmf_model.components_):
        topic_words = " ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:][::-1]])
        file.write(f"Topic {topic_idx + 1}: {topic_words}\n")

print(f"Topics have been saved to {output_file}.")
