# 运行记录

## 正常调用

命令：

```powershell
python first_api_call.py "用一句话解释什么是 AI Agent"
```

结果：

待设置 `OPENAI_API_KEY` 后运行。

## 错误场景：缺少问题参数

命令：

```powershell
python first_api_call.py
```

结果：

```text
用法: python first_api_call.py "用一句话解释什么是 AI Agent"
```

## 错误场景：缺少 OPENAI_API_KEY

命令：

```powershell
python first_api_call.py "测试"
```

结果：

```text
缺少环境变量 OPENAI_API_KEY。请先设置 API key，再运行脚本。
```
