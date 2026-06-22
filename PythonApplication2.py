import csv
import re
import os

# 貼上你的 Redis 指令字串
redis_cmd =''
# 1. 使用正規表達式提取所有引號內的內容
matches = re.findall(r'"(.*?)"', redis_cmd)
# 2. 略過前兩個元素 (即 "goldenpiginfo" 這個 key 名稱，不包含在迴圈內)
# matches[0] 會是 你的表名稱，實際資料從 matches[1] 開始
data_elements = matches[1:]

# 3. 將資料兩兩分組組成 list
rows = []
for i in range(0, len(data_elements), 2):
    if i + 1 < len(data_elements):
        key = data_elements[i]
        value = data_elements[i+1]
        rows.append([key, value])

# 4. 寫入 CSV 檔案,以下filename後方請修改成自己要的檔名，後墜需要加上.csv
filename = 'goldenpigpay.csv'
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Key', 'Value'])  # 寫入標題
    writer.writerows(rows)             # 寫入資料

print(f"轉換完成！請使用 Excel 開啟 {filename}")
