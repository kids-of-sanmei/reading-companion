# 2026-05-14 第 1 天任务

阶段：第 1 阶段 - Python 与项目基础

目标：创建并运行一个最小 Python 命令行待办事项脚本。

预计时间：60 到 120 分钟

## 学习

- 复习如何从命令行运行 Python 脚本。
- 复习 Python 基础：变量、列表、函数，以及 `if __name__ == "__main__"`。
- 复习如何通过 `sys.argv` 或 `argparse` 读取命令行参数。

## 构建

- 在本文件夹内完成 `todo.py`。
- 实现一个最小命令行待办事项脚本，支持：
  - `python todo.py add "learn Python basics"`
  - `python todo.py list`
  - `python todo.py clear`
- 第 1 天允许待办事项只在脚本单次运行期间保存在内存中，不要求写入文件。

## 验证

- 至少运行下面三类命令：
  - 添加一个任务
  - 列出任务
  - 清空任务
- 记录你运行过的命令，以及修复过的错误信息。

## 交付物

- `todo.py`
- `notes.md`
- 本任务说明文件：`daily_agent_tasks.md`

## 完成标准

- 脚本运行时没有语法错误。
- 已实现 `add`、`list` 和 `clear` 命令。
- `notes.md` 记录了使用命令。
- 你能解释为什么脚本从 `if __name__ == "__main__"` 代码块开始执行。

## 如果卡住

- 先让 `python todo.py list` 打印一个空列表。
- 再让 `python todo.py add "task"` 把任务文本打印出来。
- 前两步都能运行后，再添加 `clear` 命令。
