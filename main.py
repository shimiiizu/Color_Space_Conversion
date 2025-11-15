import subprocess
import re
import pandas as pd


def rgb_to_cmyk(r, g, b, cxf_file):
    """RGB値をCMYK値に変換"""
    result = subprocess.run(
        ["./bin/csc.exe", "-p", f"{r},{g},{b}", cxf_file],
        capture_output=True,
        text=True
    )

    match = re.search(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', result.stdout)
    if match:
        return tuple(map(int, match.groups()))
    return (None, None, None, None)


def convert_dataframe(input_csv, output_csv, cxf_file):
    """CSVのRGB値をCMYKに変換"""
    # CSVを読み込む
    df = pd.read_csv(input_csv, encoding='utf-8')

    # CMYK列を追加
    df[['C', 'M', 'Y', 'K']] = None
    print(df)

    # 各行を処理
    for index, row in df.iterrows():
        print(f"行番号: {index}")
        print(f"R: {row['R']}, G: {row['G']}, B: {row['B']}")

        # 変換
        c, m, y, k = rgb_to_cmyk(row['R'], row['G'], row['B'], cxf_file)

        # 結果を格納
        df.at[index, 'C'] = c
        df.at[index, 'M'] = m
        df.at[index, 'Y'] = y
        df.at[index, 'K'] = k

        print(f"C: {c}, M: {m}, Y: {y}, K: {k}\n")

    # 結果を保存
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"完了！結果を {output_csv} に保存しました。")
    return df


# 実行
df_result = convert_dataframe(
    input_csv='./csv/RGB.csv',
    output_csv='./csv/CMYK.csv',
    cxf_file='./cxf/colorT.cxf'
)