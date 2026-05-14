# 第 1 阶段结尾验收任务

日期：2026-05-14

阶段：第 1 阶段 - Python 与项目基础

任务名称：构建一个可运行的 Python 命令行资料整理工具

预计时间：2 到 4 小时

## 验收目标

通过一个小型完整项目，验证你是否具备进入第 2 阶段 OpenAI API 学习前所需的基础能力：

- 能创建清晰的 Python 项目结构。
- 能编写可运行的命令行程序。
- 能处理参数、文件路径、JSON 数据和异常。
- 能读取 Markdown 或 TXT 文件并生成结构化结果。
- 能写基础 README 和运行说明。
- 能使用 Git 查看改动并保存版本。

## 项目要求

在本目录下完成一个命令行工具：`notes_tool.py`。

这个工具用于整理本地学习资料，至少支持下面 4 个命令：

```powershell
python notes_tool.py scan ./samples
python notes_tool.py summary ./samples
python notes_tool.py export ./samples output.json
python notes_tool.py stats output.json
```

## 功能说明

### 1. scan

扫描指定目录下的 `.md` 和 `.txt` 文件，并打印文件列表。

要求：

- 支持相对路径和绝对路径。
- 目录不存在时给出清晰错误提示。
- 空目录时不要崩溃。

### 2. summary

读取指定目录下的 `.md` 和 `.txt` 文件，打印每个文件的简短摘要。

摘要规则可以很简单：

- 文件名
- 文件行数
- 文件字符数
- 前 80 个字符作为预览

不要求调用 AI。

### 3. export

把扫描和摘要结果保存成 JSON 文件。

JSON 至少包含：

```json
{
  "source_dir": "./samples",
  "file_count": 2,
  "files": [
    {
      "name": "example.md",
      "path": "samples/example.md",
      "lines": 10,
      "chars": 300,
      "preview": "..."
    }
  ]
}
```

### 4. stats

读取 `export` 生成的 JSON 文件，并打印统计信息：

- 文件数量
- 总行数
- 总字符数
- 字符数最多的文件

## 目录结构要求

最终目录建议如下：

```text
stage01_final_acceptance/
  acceptance_task.md
  notes_tool.py
  README.md
  samples/
    example.md
    todo.txt
  output.json
```

## 编码要求

- 使用 Python 标准库即可，不要求安装第三方依赖。
- 可以使用 `argparse` 处理命令行参数。
- 可以使用 `pathlib` 处理文件路径。
- 可以使用 `json` 读写 JSON。
- 至少拆出 3 个函数，不要把所有逻辑都写在一个大函数里。
- 需要有 `main()` 函数。
- 脚本入口必须使用：

```python
if __name__ == "__main__":
    main()
```

## 错误处理要求

至少处理下面情况：

- 输入目录不存在。
- 输入路径不是目录。
- JSON 文件不存在。
- JSON 内容无法解析。
- 目录中没有 `.md` 或 `.txt` 文件。

错误信息要能让使用者知道下一步该怎么改。

## 验证命令

完成后，在 `stage01_final_acceptance/` 目录下运行：

```powershell
python notes_tool.py scan ./samples
python notes_tool.py summary ./samples
python notes_tool.py export ./samples output.json
python notes_tool.py stats output.json
```

再运行至少两个错误场景：

```powershell
python notes_tool.py scan ./missing
python notes_tool.py stats missing.json
```

## 交付物

- `notes_tool.py`
- `README.md`
- `samples/example.md`
- `samples/todo.txt`
- `output.json`
- 一段命令运行记录，写在 `README.md` 中

## 完成标准

满足下面条件，视为第 1 阶段通过：

- 四个核心命令都能运行。
- 正常输入能输出正确结果。
- 错误输入有清晰提示，不出现长 traceback。
- `output.json` 是合法 JSON。
- `README.md` 写清楚项目用途、运行方式和验证命令。
- 代码结构清楚，函数命名可读。
- 能解释 `argparse`、`pathlib`、`json` 在项目中的作用。

## 不通过标准

出现下面任一情况，建议继续补第 1 阶段基础：

- 只能复制代码，无法解释主要函数。
- 路径稍微变化就运行失败。
- JSON 读写不稳定。
- 报错时只出现 traceback，没有用户可读提示。
- 项目没有 README 或无法复现运行过程。

## 通过后的下一步

进入第 2 阶段：OpenAI API 基础。

下一任务建议：

编写一个最小命令行脚本，直接调用 OpenAI API，发送一条 user message，并打印模型返回结果。
