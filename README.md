# Geographic Coordinate Conversion

這個專案提供了地理座標轉換和地址查詢的功能，特別針對台灣的 TWD97 座標系統。

## 功能特色

- **TWD97 座標轉換為 WGS84** - 將台灣常用的 TWD97 座標轉換為全球通用的 WGS84 經緯度座標
- **座標轉地址** - 透過反向地理編碼 (Reverse Geocoding) 將座標轉換為實際地址
- **批次處理 CSV 檔案** - 支援處理含有多筆座標的 CSV 檔案，並產生帶有地址資訊的結果檔

## 安裝需求

Python >= 3.12

專案依賴以下 Python 套件：

```bash
pip install -r requirements.txt
```


## 專案結構

```
geographic-coordinate-conversion/
├── requirements.txt       # 專案依賴套件列表
├── README.md              # 專案說明文件
└── src/                   # 主要程式碼
    ├── reverse_geocode.py # 座標轉換與地址查詢功能
    ├── process_csv.py     # CSV 檔案處理工具
    ├── sample.csv         # 範例輸入檔案
    └── result.csv         # 處理結果輸出檔案
```

## 使用方式

### 1. 單一座標轉換為地址

使用 `reverse_geocode.py` 直接在命令列輸入座標：

```bash
cd src
python reverse_geocode.py
```

程式將提示您輸入 TWD97 座標，格式為 `(x, y)`，例如：`(248170.79, 2652129.94)`

### 2. 處理 CSV 檔案

使用 `process_csv.py` 處理含有多筆座標的 CSV 檔案：

```bash
cd src
python process_csv.py
```

此命令會讀取 `sample.csv`，為每個座標查詢地址，並將結果輸出至 `result.csv`。

#### CSV 檔案格式

輸入檔案 (sample.csv) 格式：
```
X, Y
248170.79, 2652129.94
304000.00, 2770000.00
...
```

輸出檔案 (result.csv) 格式：
```
X,Y,Address
248170.79,2652129.94,虎子山步道, 虎仔耳, 大湳里, 埔里鎮, 南投縣, 54560, 臺灣
304000.00,2770000.00,幸安國小, 22, 仁愛路三段, 民炤里, 大安區, 華山, 臺北市, 106, 臺灣
...
```

## 技術細節

- 使用 TWD97 (台灣常用) 轉 WGS84 (全球通用) 的數學轉換公式
- 使用 Nominatim 地理編碼服務進行地址查詢
- 預設輸出地址為繁體中文 (zh-TW)，可以在程式碼中修改語言設定

## 注意事項

- 地址查詢服務需要網路連線
- 大量查詢可能受到服務提供商的速率限制
- 座標越精確，查詢到的地址越準確

## 授權資訊

此專案採用 MIT 授權條款。