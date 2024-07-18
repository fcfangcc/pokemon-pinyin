## 生成宝可梦的拼音、文字、图片，用于学习拼音和汉字

![image](/example.png)

## 安装
```shell
pip install pokemon_pinyin
```

## 使用
运行会生成满足条件的pdf文档

```shell
# 选择1-10号（包含10）
ppinyin run 1..10

# 选择1 3 5 7号
ppinyin run 1,3,5,7

# 选择1-100号，过滤某个字只包含l,v
ppinyin run 1..100 -fb m,a 
# 选择编号为1..100的宝可梦
# 共搜索到符合条件的宝可梦3只
# --- 文件已保存到`output_a4.pdf` ---
```

## 字体

默认自带simhei字体

也可以使用你自己喜欢的字体,只需要在命令行里面修改对应的参数即可


## package

Publish package
```
python -m build
```

Development mode
```
pip install --editable .
```