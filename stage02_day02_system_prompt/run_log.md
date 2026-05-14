# 运行记录

## concise

```powershell
python system_prompt_demo.py --style concise "解释什么是 AI Agent"
```

结果：

待设置 `OPENAI_API_KEY` 后运行并填写。

## teacher

```powershell
python system_prompt_demo.py --style teacher "解释什么是 AI Agent"
```

结果：

待设置 `OPENAI_API_KEY` 后运行并填写。

## engineer

```powershell
python system_prompt_demo.py --style engineer "解释什么是 AI Agent"
```

结果：

待设置 `OPENAI_API_KEY` 后运行并填写。

## 错误场景

```powershell
python system_prompt_demo.py --style unknown "解释什么是 AI Agent"
python system_prompt_demo.py
```

结果：

已验证：

```text
调用失败: 缺少环境变量 OPENAI_API_KEY。请先设置 API key。
```

```text
system_prompt_demo.py: error: argument --style: invalid choice: 'unknown' (choose from concise, engineer, teacher)
```
