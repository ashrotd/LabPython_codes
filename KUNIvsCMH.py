import requests
import re
from bs4 import BeautifulSoup

cloud_base_height_kuni = []
cloud_base_height_CMH = []
page = requests.get(
    "https://aviationweather.gov/metar/data?ids=KUNI&format=raw&hours=120&taf=off&layout=on"
)
soup = BeautifulSoup(page.content, "html.parser")
datas = soup.select("code")

for data in datas:
    text = data.get_text()

    lowest_sct = float("inf")
    lowest_bkn = float("inf")
    lowest_ovc = float("inf")

    sct_matches = re.finditer(r"SCT(\d+)", text)
    bkn_matches = re.finditer(r"BKN(\d+)", text)
    ovc_matches = re.finditer(r"OVC(\d+)", text)

    for match in sct_matches:
        sct_value = int(match.group(1))
        if sct_value < lowest_sct:
            lowest_sct = sct_value
            cloud_base_height_kuni.append(lowest_sct)

    for match in bkn_matches:
        bkn_value = int(match.group(1))
        if bkn_value < lowest_bkn:
            lowest_bkn = bkn_value
            cloud_base_height_kuni.append(lowest_bkn)

    for match in ovc_matches:
        ovc_value = int(match.group(1))
        if ovc_value < lowest_ovc:
            lowest_ovc = ovc_value
            cloud_base_height_kuni.append(lowest_ovc)


page = requests.get(
    "https://www.aviationweather.gov/metar/data?ids=KCMH&format=raw&date=&hours=120"
)
soup = BeautifulSoup(page.content, "html.parser")
datas = soup.select("code")

for data in datas:
    text = data.get_text()

    lowest_sct = float("inf")
    lowest_bkn = float("inf")
    lowest_ovc = float("inf")

    sct_matches = re.finditer(r"SCT(\d+)", text)
    bkn_matches = re.finditer(r"BKN(\d+)", text)
    ovc_matches = re.finditer(r"OVC(\d+)", text)
    few = re.finditer(r"FEW(\d+)", text)

    for match in sct_matches:
        sct_value = int(match.group(1))
        if sct_value < lowest_sct:
            lowest_sct = sct_value
            cloud_base_height_CMH.append(lowest_sct)

    for match in bkn_matches:
        bkn_value = int(match.group(1))
        if bkn_value < lowest_bkn:
            lowest_bkn = bkn_value
            cloud_base_height_CMH.append(lowest_bkn)

    for match in ovc_matches:
        ovc_value = int(match.group(1))
        if ovc_value < lowest_ovc:
            lowest_ovc = ovc_value
            cloud_base_height_CMH.append(lowest_ovc)


# Sample data
import matplotlib.pyplot as plt


fig, axes = plt.subplots(1, 2, figsize=(14, 6))


axes[0].stem(cloud_base_height_CMH, use_line_collection=True)
axes[0].set_xlabel("Data Points")
axes[0].set_ylabel("CBH in ft")
axes[0].set_title("CMH Ceiling Height")
axes[0].grid(True)


axes[1].stem(cloud_base_height_kuni, use_line_collection=True)
axes[1].set_xlabel("Data Points")
axes[1].set_ylabel("CBH in ft")
axes[1].set_title("KUNI Ceiling Height")
axes[1].grid(True)


plt.tight_layout()


plt.show()
