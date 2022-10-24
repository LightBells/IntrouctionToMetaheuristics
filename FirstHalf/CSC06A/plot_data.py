# アニーリング
import urllib.request
url = 'https://raw.githubusercontent.com/maskot1977/ipython_notebook/master/toydata/location.txt'
urllib.request.urlretrieve(url, 'location.txt') # データのダウンロード

import pandas as pd
japan = pd.read_csv('location.txt')

print(japan)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10, 8))
plt.scatter(japan['Latitude'], japan['Longitude'])
for city, x, y in zip(japan['Town'], japan['Latitude'], japan['Longitude']):
    plt.text(x, y, city, alpha=0.5, size=12)
plt.grid()
plt.show()
fig.savefig("img.png")