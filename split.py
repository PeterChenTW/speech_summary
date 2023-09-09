import os
import time
from pydub import AudioSegment
from pydub.utils import make_chunks

# 設定文件夾路徑
source_folder = "audio"
output_folder = "audio_split"

# 確保輸出文件夾存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

file_list = os.listdir(source_folder)
total_files = len(file_list)

start_time = time.time()

# 遍歷文件夾中的所有檔案
for idx, file_name in enumerate(file_list, 1):
    file_path = os.path.join(source_folder, file_name)
    
    # 為每個錄音檔案建立一個子資料夾
    individual_folder = os.path.join(output_folder, file_name.rsplit('.', 1)[0])
    if not os.path.exists(individual_folder):
        os.makedirs(individual_folder)

    # 載入音訊檔案
    audio = AudioSegment.from_file(file_path)
    
    # 以一分鐘為區間分割檔案
    chunk_length = 60 * 1000  # 60 seconds * 1000 ms/s
    chunks = make_chunks(audio, chunk_length)
    
    # 儲存每個分割後的檔案
    for i, chunk in enumerate(chunks):
        chunk_name = f"{file_name.rsplit('.', 1)[0]}_chunk_{i}.mp3"
        chunk_path = os.path.join(individual_folder, chunk_name)
        chunk.export(chunk_path, format="mp3")

    elapsed_time = time.time() - start_time
    estimated_time = (elapsed_time / idx) * (total_files - idx)
    print(f"已處理 {idx}/{total_files} 檔案，估計剩餘時間：{estimated_time:.2f} 秒")

print("處理完成!")
