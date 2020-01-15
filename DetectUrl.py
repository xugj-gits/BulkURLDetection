# 导出表格数据：
# TDK是否被改表格要求：序号，域名，Title，Keywords，Description
# 网站能否打开表格要求：序号，域名，是否打开状态


import urllib.request
import time
import datetime
import opertaeExcel
import tdk

# 这个是你放网址的文件名，改过来就可以了
file = open('待检测URL.txt')
lines = file.readlines()
aa = []
for line in lines:
    temp = line.replace('\n', '')
    aa.append(temp)

print('开始检查：')

array = [["序号", "域名", "是否打开状态"]]
for index, a in enumerate(aa):
    tempUrl = a
    if len(tempUrl) == 0:
        lines.remove(tempUrl + '\n')
        continue

    print(str(index + 1) + " 正在检测：" + tempUrl)
    try:
        response = urllib.request.urlopen(tempUrl)
        if response.status == 301:
            array.append([index, tempUrl, "301跳转"])
    except urllib.error.HTTPError:
        array.append([index, tempUrl, "未打开"])
        lines.remove(tempUrl + '\n')
    except urllib.error.URLError:
        array.append([index, tempUrl, "未打开"])
        lines.remove(tempUrl + '\n')
    except BaseException:
        with open('error.txt', 'a') as f:
            f.write('\n')
            f.write(BaseException)


print(array)

tdk.test(lines, 20)
opertaeExcel.write_excel_xlsx("打开状态检测结果.xlsx", "打开检测结果", array)
