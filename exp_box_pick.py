import pandas as pd
from google.oauth2.service_account import Credentials
import gspread

class EXPBOX:
    def _get_usedppl_from_googlesheet(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file("googlesheet.json", scopes=scope)
        gs = gspread.authorize(creds)
        sheet = gs.open_by_url("https://docs.google.com/spreadsheets/d/1kXcF0THpVi-FItaYnSVW03C2J3hSZRrvd1kWSayueK4/edit#gid=0")
        worksheet = sheet.get_worksheet(0)
        data = pd.DataFrame(worksheet.get_all_records())
        data["使用者ID"] = data["使用者ID"].astype("str")
        return list(data["使用者ID"])

    def pick(self, used_ppl):
        print("輸入檔案名稱")
        filename = input()
        data = pd.read_excel(f"{filename}.xlsx")
        data = data[data["姓名"].isnull()==False]
        data["電話"] = data["電話"].apply(lambda x:f"0{str(int(x))}")
        data["地址.區碼"] = data["地址.區碼"].apply(lambda x:str(int(x)))
        email_dup = data["信箱"].value_counts()
        data["duplicate"] = data["信箱"].apply(lambda x: True if email_dup[x]>1 else False)
        data = data[data["duplicate"]==False]
        total_data_count = len(data)
        data["used"] = data["會員ID"].apply(lambda x:True if x in used_ppl else False)
        used_count = len(data[data["used"]==True])
        data = data[data["used"]==False]
        data = data.sample(frac=1)
        print(f"要抽幾個人呢 ? 總共有 {len(data)} 人。(總人數 {total_data_count} 人，其中 {used_count} 人近一個月已體驗過予以排除)。")
        ppl = int(input())
        data = data.loc[:, ["會員ID", "姓名", "電話", "地址.區碼", "地址.縣市", "地址.區", "地址.地址"]].head(ppl)
        data.to_excel("result.xlsx", index=False, encoding = "utf-8-sig")
        return "DONE"

if __name__=="__main__":
    expbox = EXPBOX()
    used_ppl = expbox._get_usedppl_from_googlesheet()
    expbox.pick(used_ppl)