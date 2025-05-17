# my-openai-sandbox

This repository contains a minimal command-line task management application written in Python.

## Usage

Install dependencies (there are none outside the standard library) and run the app with python:

```bash
python task_manager.py add "Buy milk"
python task_manager.py list
python task_manager.py done 1
python task_manager.py delete 1
```

Tasks are stored in `tasks.json` in the project directory.
