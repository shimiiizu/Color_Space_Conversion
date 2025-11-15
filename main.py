import subprocess
import re
import pandas as pd

df = pd.read_csv('./csv/RGB.csv', encoding='utf-8')
# 新しい列を追加
df['C'] = None
df['M'] = None
df['Y'] = None
df['K'] = None
print(df)

subprocess.run(["./bin/csc.exe", "-p", "100, 100, 100", "./cxf/colorT.cxf"]) # RGB値➡CMYK値
# subprocess.run(["./bin/csc.exe", "./tif/10_cube_RGB_Page_0_LTR.tif","./tif/output_file.tif","./cxf/colorT.cxf"]) #
# RGB（tif）➡CMYK(tif)変換

# 出力をキャプチャ
result = subprocess.run(
    ["./bin/csc.exe", "-p", "100,100,100", "./cxf/colorT.cxf"],
    capture_output=True,
    text=True
)

# 出力から数値を抽出
output = result.stdout.strip()
print(f"生の出力: {output}")

# 正規表現でCMYK値を抽出
match = re.search(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', output)
if match:
    c, m, y, k = map(int, match.groups())
    print(f"C: {c}, M: {m}, Y: {y}, K: {k}")