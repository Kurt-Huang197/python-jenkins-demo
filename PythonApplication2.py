import os
import re
import csv
import sys

# 1. 接收 Jenkins 參數 (自動轉為環境變數)
# 注意：此處的鍵值必須與 Jenkins 設定的參數名稱完全一致
redis_cmd = os.environ.get('REDIS_INPUT', '')
custom_name = os.environ.get('FILE_NAME', 'output').strip()

# 防呆機制
if not custom_name:
    custom_name = 'output'

if not redis_cmd.strip():
    print("【錯誤】未偵測到輸入內容，請確認是否已貼上 Redis 程式碼。")
    sys.exit(1)

# 2. 處理副檔名
if custom_name.lower().endswith('.csv'):
    filename = custom_name
else:
    filename = f"{custom_name}.csv"

# 3. 執行資料轉換邏輯
# 抓取所有引號內的字串
matches = re.findall(r'"(.*?)"', redis_cmd)

if len(matches) < 2:
    print("【錯誤】解析失敗，請確認 Redis 程式碼格式是否包含引號。")
    sys.exit(1)

# 忽略第一個元素 (HSET 的主鍵，例如 "goldenpigpay")
data_elements = matches[1:]

rows = []
# 兩個兩個一組抓取 Key 與 Value
for i in range(0, len(data_elements), 2):
    if i + 1 < len(data_elements):
        key = data_elements[i]
        value = data_elements[i+1]
        rows.append([key, value])

# 4. 寫入 CSV 檔案
# 使用 'w' 模式會直接覆蓋同名檔案，不需在腳本中執行 rm 指令
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Key', 'Value'])
    writer.writerows(rows)

print(f"轉換成功！檔案已產生：{filename}")
