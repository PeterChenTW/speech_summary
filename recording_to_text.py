import os
import time
import openai
# openai.api_key = '-'

# 假設您的 speech_to_text 函數已經被定義或導入
def speech_to_text(audio_file_path):
    audio_file= open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

# 設定文件夾路徑
source_folder = "audio_split"
output_folder = "audio_text"

# 確保輸出文件夾存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 計算總的子錄音檔數量
total_files = sum([len(files) for subdir, dirs, files in os.walk(source_folder)])
processed_files = 0
start_time = time.time()

# 遍歷文件夾中的所有子資料夾
for subdir in os.listdir(source_folder):
    subdir_path = os.path.join(source_folder, subdir)
    print(subdir_path)
    # 確保它是一個資料夾
    if os.path.isdir(subdir_path):
        full_text = ""
        
        # 遍歷子資料夾中的所有錄影檔
        for file_name in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file_name)
            
            # 使用 speech_to_text 函數轉換語音內容
            text_content = speech_to_text(file_path)
            full_text += text_content + "\n\n"
            
            # 更新進度和預估時間
            processed_files += 1
            elapsed_time = time.time() - start_time
            estimated_time = (elapsed_time / processed_files) * (total_files - processed_files)
            print(f"已處理 {processed_files}/{total_files} 檔案，估計剩餘時間：{estimated_time:.2f} 秒")
        
        # 儲存文字內容到 recording_text 文件夾
        output_file_path = os.path.join(output_folder, f"{subdir}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(full_text)

print("處理完成!")