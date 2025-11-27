import pandas as pd
import numpy as np
from datetime import datetime, timedelta

n = 5000  # 数据量
dates = [datetime(2024,1,1) + timedelta(days=np.random.randint(0, 365)) for _ in range(n)]
stores = np.random.choice(["华东店","华北店","华南店"], n)
categories = np.random.choice(["饮料","食品","生活用品"], n)
products = {
    "饮料": ["可乐","雪碧","矿泉水"],
    "食品": ["面包","薯片","巧克力"],
    "生活用品": ["牙膏","洗发水","洗衣液"]
}
items = [np.random.choice(products[c]) for c in categories]
prices = np.round(np.random.uniform(3,60,n),2)
qty = np.random.randint(1,15,n)
amount = np.round(prices*qty,2)

df = pd.DataFrame({
    "日期": dates,
    "门店": stores,
    "类别": categories,
    "商品": items,
    "单价": prices,
    "数量": qty,
    "总金额": amount
})

df.to_excel("超市销量_5000条.xlsx", index=False)
