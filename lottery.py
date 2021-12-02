import random
import pandas as pd
import xlsxwriter
import urllib.request
from PIL import Image
from tqdm import tqdm

data = pd.read_excel("lottery.xlsx")
data = data.sample(frac = 1).reset_index(drop=True)
workbook = xlsxwriter.Workbook(".\image.xlsx")        
worksheet = workbook.add_worksheet()
ppl = int(input("你想抽幾個人?"))
for r in range(ppl):
    worksheet.set_row(r, 1000)
for idx in tqdm(range(ppl)):
    try:
        urllib.request.urlretrieve(data["content"][idx],f"{idx}.png")
        worksheet.write(f"A{idx+1}", f"{data['floor'][idx]}")
        worksheet.write(f"B{idx+1}", f"{data['member_id'][idx]}")
        worksheet.insert_image(f"C{idx+1}", f"{idx}.png", {'x_scale': 0.5, 'y_scale': 0.5})
    except:
        print(data["content"][idx])
workbook.close()