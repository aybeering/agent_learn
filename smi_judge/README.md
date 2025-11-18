# 这是我的第一个agent项目
能够输入smi字符串，并生成相应的图片，在用户输入smi错误时，会解释可能报错的原因

## 能学习到的内容
- 使用节点处理调用函数的逻辑关系
- 调用llm来处理函数
- 理解如何连接节点

## 记录我的学习笔记
本smi中包含了一个类和多个函数，此处依依讲解
- 类```SearchState```
    定义了各个函数之间消息传递的内容，以及定义这些消息的格式
- ```judge_smi```与```smi_to_graph```
    这是两个功能性的函数，这两个函数调用了rdkit，产出期望的输出，并未调用llm
- ```guess_info_from_wrong_smi```
    这是一个专门用于调用与定义llm的函数，目前实现了在这个函数中写入简单的prompt，还并为增添其他逻辑信息
- ```search_smi```与```draw```
    这是两个节点函数，在节点函数内实现通过逻辑调用以上三个函数
- ```create_search_assistant```
    这是节点连接状态函数，可以定义节点之间的关系

## 使用方法
你可以直接使用来测试，请确保你有deepseek的api_key
```
DEEPSEEK_API_KEY="YOUR_API_KEY" python smi.py
```

## 环境
- rdkit
- tpying
- langgraph
