import os
from tqdm import tqdm
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
import openai
# openai.api_key = '-'


def text_to_summary(file_path):
    loader = TextLoader(file_path, encoding='utf-8')
    # Define prompt
    prompt_template = """Result format and rule:
    1. Write a summary. If the speaker mentions quantified data, please be sure to write it down.
    2. List the Keywords(top 5)
    The following is the person spoke at the semiconductor conference:
    ```
    "{text}"
    ```
    SUMMARY and KEYWORDS:"""
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-4", openai_api_key=openai.api_key)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )

    docs = loader.load()
    return stuff_chain.run(docs)

# 設定文件夾路徑
source_folder = "audio_text"
output_folder = "audio_summary"

# 確保輸出文件夾存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 獲取所有.txt檔案
text_files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]

# 使用 tqdm 來遍歷文件夾中的所有.txt檔案並顯示進度條
for file_name in tqdm(text_files, desc="處理中", unit="file"):
    file_path = os.path.join(source_folder, file_name)
    
    # 使用 text_to_summary 函數產生摘要
    summary = text_to_summary(file_path)
    
    # 儲存摘要到 recording_summary 文件夾
    output_file_path = os.path.join(output_folder, file_name)
    with open(output_file_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write(summary)

print("處理完成!")
