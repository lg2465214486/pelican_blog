Title: git命令大全
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 操作命令
keywords: Git常用命令大全
summary: Git常用命令大全
lang: zh
status: published
Slug: git_command_all
url: git_command_all

<br>

# Git 命令大全

## 一、基础命令

### 1. 配置相关
```bash
git config --global user.name "Your Name"           # 设置全局用户名
git config --global user.email "your@email.com"     # 设置全局邮箱
git config --list                                  # 查看所有配置
git config --global core.editor "vim"              # 设置默认编辑器
```

### 2. 仓库初始化
```bash
git init                                          # 初始化本地仓库
git clone <url>                                   # 克隆远程仓库
git clone -b <branch> <url>                       # 克隆指定分支
```

## 二、分支操作

### 1. 分支管理
```bash
git branch                                        # 查看本地分支
git branch -a                                     # 查看所有分支(包括远程)
git branch <branch-name>                          # 创建新分支
git checkout <branch-name>                        # 切换分支
git checkout -b <new-branch>                      # 创建并切换分支
git merge <branch-name>                           # 合并分支
git branch -d <branch-name>                       # 删除本地分支
git branch -D <branch-name>                       # 强制删除本地分支
git push origin --delete <branch-name>            # 删除远程分支
```

### 2. 远程分支
```bash
git fetch                                         # 获取远程更新
git fetch -p                                      # 获取远程更新并清理已删除的远程分支
git pull                                          # 拉取远程分支并合并
git pull origin <branch-name>                     # 拉取指定远程分支
git push -u origin <branch-name>                  # 推送并设置上游分支
```

## 三、提交历史

### 1. 提交操作
```bash
git status                                        # 查看状态
git add <file>                                    # 添加文件到暂存区
git add .                                         # 添加所有修改到暂存区
git commit -m "message"                           # 提交更改
git commit --amend                                # 修改最后一次提交
git commit --amend -m "new message"               # 修改最后一次提交信息
```

### 2. 查看历史
```bash
git log                                           # 查看提交历史
git log --oneline                                 # 简洁版历史
git log --graph                                   # 图形化显示分支
git log -p <file>                                 # 查看文件的修改历史
git blame <file>                                  # 查看文件每行修改人
```

## 四、撤销操作

### 1. 撤销更改
```bash
git restore <file>                                # 撤销工作区修改
git restore --staged <file>                       # 撤销暂存区修改
git reset HEAD <file>                             # 取消暂存(同git restore --staged)
git reset --hard                                  # 丢弃所有本地修改
git revert <commit-id>                            # 撤销指定提交
```

### 2. 重置操作
```bash
git reset --soft <commit-id>                      # 重置到指定提交(保留修改)
git reset --mixed <commit-id>                     # 重置到指定提交(取消暂存)
git reset --hard <commit-id>                      # 彻底重置到指定提交
```

## 五、远程仓库

### 1. 远程操作
```bash
git remote -v                                     # 查看远程仓库
git remote add <name> <url>                       # 添加远程仓库
git remote remove <name>                          # 删除远程仓库
git remote rename <old> <new>                     # 重命名远程仓库
git remote set-url <name> <newurl>                # 修改远程仓库地址
```

### 2. 标签操作
```bash
git tag                                           # 查看标签
git tag <tag-name>                                # 创建轻量标签
git tag -a <tag-name> -m "message"                # 创建带注释标签
git push origin <tag-name>                        # 推送标签到远程
git push origin --tags                            # 推送所有标签
git tag -d <tag-name>                             # 删除本地标签
git push origin --delete <tag-name>                # 删除远程标签
```

## 六、高级操作

### 1. 储藏更改
```bash
git stash                                         # 储藏当前修改
git stash save "message"                          # 储藏并添加说明
git stash list                                    # 查看储藏列表
git stash apply                                   # 应用最近的储藏
git stash pop                                     # 应用并删除最近的储藏
git stash drop                                    # 删除最近的储藏
```

### 2. 子模块
```bash
git submodule add <url> <path>                    # 添加子模块
git submodule update --init --recursive           # 初始化并更新子模块
git submodule foreach 'git pull origin master'    # 更新所有子模块
```

### 3. 其他实用命令
```bash
git diff                                          # 查看未暂存的修改
git diff --staged                                 # 查看已暂存的修改
git cherry-pick <commit-id>                       # 选择某个提交应用到当前分支
git rebase <branch>                               # 变基操作
git reflog                                        # 查看所有操作记录
git gc                                            # 清理不必要的文件并优化本地仓库
```

## 七、Git Flow 工作流常用命令

```bash
git flow init                                     # 初始化git-flow
git flow feature start <name>                     # 开始新功能
git flow feature finish <name>                    # 完成功能开发
git flow release start <version>                  # 开始新版本发布
git flow release finish <version>                 # 完成版本发布
git flow hotfix start <version>                   # 开始热修复
git flow hotfix finish <version>                  # 完成热修复
```

## 八、Git 钩子

```bash
ls .git/hooks/                                    # 查看可用钩子
chmod +x .git/hooks/pre-commit                    # 使钩子可执行
```