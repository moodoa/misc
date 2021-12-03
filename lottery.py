import re
import pandas as pd
import xlsxwriter
import urllib.request
from PIL import Image
from tqdm import tqdm
from datetime import datetime


print("輸入 EXCEL 檔名")
filename = input()
data = pd.read_excel(f"{filename}.xlsx")
data.dropna(inplace=True)
print("留言次數限制，超過即刪除資格。")
limit = int(input())
id_count = data["member_id"].value_counts()
data["limit_reached"] = data["member_id"].apply(lambda x: True if id_count[x] > 100 else False)
data = data[data["limit_reached"] == False]
print("最終留言時間，超過即刪除資格。格式 : 2021-11-22/17:18:19")
time_limit = datetime.strptime(input(), "%Y-%m-%d/%H:%M:%S")
data["time_limit"] = data["time"].apply(lambda x:True if datetime.strptime(x, "%Y-%m-%dT%H:%M:%S") > time_limit else False)
data = data[data["time_limit"]==False]
image_pattern = r"(https?:\/\/.*\.(?:png|jpg|jpeg))"
print("輸入關鍵字，可替換字用 @& 取代。如無關鍵字則直接輸入 ENTER。")
keyword = input()
keyword_pattern = "(.+)".join(keyword.split("@&"))
data["image_url"] = data["content"].apply(lambda x:re.findall(image_pattern, x)[0] if re.findall(image_pattern, x) else "")
data["keyword_check"] = data["content"].apply(lambda x:True if (re.findall(keyword_pattern, x)) else False)
data[data["keyword_check"]==True]
data = data.sample(frac = 1).reset_index(drop=True)
print("是否是圖片抽獎? Y/N")
judge = input()
print(f"符合資格的留言數 : {len(data)}")
workbook = xlsxwriter.Workbook("image.xlsx")        
worksheet = workbook.add_worksheet()
ppl = int(input("你想抽幾個人?"))
for r in range(ppl+100):
    worksheet.set_row(r, 600 if judge.lower()=="y" else 20)
box = 0
idx = 1
used_id = ["a"]
worksheet.write("A1", "floor")
worksheet.write("B1", "image")
worksheet.write("C1", "content")
worksheet.write("D1", "member_id")
worksheet.write("E1", "time")
worksheet.write("F1", "school")
worksheet.write("G1", "department")
while box <= ppl:
    if data["member_id"][idx] not in used_id:
        try:
            if judge.lower() == "y":
                urllib.request.urlretrieve(data["image_url"][idx],f"{idx}.png")
                worksheet.write(f"A{len(used_id)+1}", f"{data['floor'][idx]}")
                worksheet.insert_image(f"B{len(used_id)+1}", f"{idx}.png", {'x_scale': 0.35, 'y_scale': 0.35})
                worksheet.write(f"C{len(used_id)+1}", f"{data['content'][idx]}")
                worksheet.write(f"D{len(used_id)+1}", f"{data['member_id'][idx]}")
                worksheet.write(f"E{len(used_id)+1}", f"{data['time'][idx]}")
                worksheet.write(f"F{len(used_id)+1}", f"{data['school'][idx]}")
                worksheet.write(f"G{len(used_id)+1}", f"{data['department'][idx]}")
            else:
                worksheet.write(f"A{len(used_id)+1}", f"{data['floor'][idx]}")
                worksheet.write(f"B{len(used_id)+1}", f"")
                worksheet.write(f"C{len(used_id)+1}", f"{data['content'][idx]}")
                worksheet.write(f"D{len(used_id)+1}", f"{data['member_id'][idx]}")
                worksheet.write(f"E{len(used_id)+1}", f"{data['time'][idx]}")
                worksheet.write(f"F{len(used_id)+1}", f"{data['school'][idx]}")
                worksheet.write(f"G{len(used_id)+1}", f"{data['department'][idx]}")
            used_id.append(data["member_id"][idx])
            box += 1
            idx += 1
        except:
            pass
    else:
        idx += 1

workbook.close()