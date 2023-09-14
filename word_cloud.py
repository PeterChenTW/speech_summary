import os
import spacy
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# 載入spaCy的英文模型和stop words
nlp = spacy.load("en_core_web_sm")
stop_words = set(STOPWORDS)

# 增加或調整停用詞
custom_stopwords = {"actually", "lot", "need", "kind", "different", "know", "want", "use", "thing", "look", "go", "think", "time", "right", "way", "come", "start", "new", "good", "help", "people", "let", "basically", "okay", "sure", "maybe", "well", "say", "big", "say", "long", "small", "place", "single", "type", "simple", "day", "especially", "speaker", "Summary", "SUMMARY speaker"}

stop_words.update(custom_stopwords)

# 讀取文檔
docs = []
folder_path = 'audio_summary'
for file_name in os.listdir(folder_path):
    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
        docs.append(file.read())
text = " ".join(docs)

# 使用spaCy進行分詞和前處理
def tokenizer(text):
    return " ".join([token.lemma_ for token in nlp(text) if not token.is_stop and token.is_alpha])

processed_text = tokenizer(text)

# 創建文字雲
wordcloud = WordCloud(stopwords=stop_words, background_color="white", max_words=500, width=800, height=400).generate(processed_text)

# 儲存文字雲中的詞彙及其權重，並且使權重較大的詞彙排在前面
sorted_words = sorted(wordcloud.words_.items(), key=lambda x: x[1], reverse=True)

with open("word_weights_summary.txt", 'w', encoding='utf-8') as file:
    for word, weight in sorted_words:
        file.write(f"{word}\n")

# 顯示文字雲
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# 儲存文字雲到檔案
output_path = "wordcloud_summary.png"
wordcloud.to_file(output_path)

print(f"Word cloud saved to {output_path}.")
print("Words and weights saved to word_weights.txt.")
