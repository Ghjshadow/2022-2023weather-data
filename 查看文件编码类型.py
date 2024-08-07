import chardet

# 读取文件的部分内容来检测编码
with open('./weatherdata/weather_20220915_20221010.csv', 'rb') as f:
    result = chardet.detect(f.read(10000))  # 读取前 10000 个字节
    print(result)