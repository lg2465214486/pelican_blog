Title: Git命令大全
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: 操作命令
keywords: Git常用命令大全
summary: 这是一份非常全面的 Git 命令大全，包含了常用命令、使用场景、参数解释和细节说明
lang: zh
status: published
Slug: git_command_all
url: git_command_all

<br>

# Git 命令大全

---

### 第一部分：基础与初始化

这些命令用于初始配置和创建/获取仓库。

| 命令 | 解释与细节 |
| :--- | :--- |
| `git config --global user.name "Your Name"` | 设置全局用户名，**每次提交都会记录这个信息**。 |
| `git config --global user.email "your_email@example.com"` | 设置全局邮箱地址，**每次提交都会记录这个信息**。 |
| `git config --list` | 列出当前所有的 Git 配置。 |
| `git init` | 将当前目录初始化为一个新的 Git 仓库。会创建一个 `.git` 隐藏文件夹。 |
| `git clone <repo_url>` | 克隆（下载）一个远程仓库到本地。例如：`git clone https://github.com/user/repo.git` |
| `git clone <repo_url> <directory_name>` | 克隆仓库，并指定本地文件夹的名称。 |

---

### 第二部分：日常工作流（添加与提交）

这是你日常使用最频繁的一组命令，构成了基本的工作流。

| 命令 | 解释与细节 |
| :--- | :--- |
| `git status` | 查看工作区和暂存区的状态。**显示有哪些文件被修改、新增或删除，以及它们是否已暂存。** |
| `git add <file>` | 将指定文件的**当前更改**添加到暂存区。 |
| `git add .` 或 `git add -A` | 添加**所有**的更改（包括新建、修改、删除的文件）到暂存区。 |
| `git add -u` | 添加**所有已跟踪文件的更改**到暂存区（不包括未跟踪的新文件）。 |
| `git reset <file>` | 将指定文件从暂存区**撤出**，但保留工作区的修改。 |
| `git reset` | 将所有文件从暂存区撤出，相当于撤销 `git add`。 |
| `git commit -m "Commit message"` | 将暂存区的内容提交到本地仓库，并附上提交信息。 |
| `git commit -a -m "Message"` | **捷径**：相当于 `git add -u` + `git commit -m`，会自动把所有**已跟踪文件**的修改添加并提交。**注意：不包含新文件！** |
| `git diff` | 查看**工作区**和**暂存区**之间的差异（即，你修改了但还没 `git add` 的内容）。 |
| `git diff --staged` (或 `--cached`) | 查看**暂存区**和**最后一次提交**之间的差异（即，你已经 `git add` 了但还没 `git commit` 的内容）。 |
| `git restore <file>` | **（Git 2.23+）** 丢弃工作区中指定文件的修改，恢复到最后一次提交的状态。**危险操作，不可恢复！** |
| `git restore --staged <file>` | **（Git 2.23+）** 将指定文件从暂存区移出，等同于 `git reset <file>`。 |

---

### 第三部分：查看历史与日志

用于查看项目的提交历史。

| 命令 | 解释与细节 |
| :--- | :--- |
| `git log` | 按时间顺序显示提交历史。 |
| `git log --oneline` | 以简洁的单行形式显示提交历史。 |
| `git log --graph` | 以 ASCII 图形显示分支和合并历史。 |
| `git log --stat` | 显示每次提交的文件修改统计信息（哪些文件被修改，增删行数）。 |
| `git log -p` | 显示每次提交的详细内容差异（Patch）。 |
| `git log -n <limit>` | 仅显示最近 n 次的提交，例如 `git log -2`。 |
| `git show <commit_id>` | 显示某一次提交的元数据和内容变化。 |

---

### 第四部分：分支与合并

Git 的核心功能，用于并行开发和功能集成。

| 命令 | 解释与细节 |
| :--- | :--- |
| `git branch` | 列出所有本地分支。当前分支前面会标一个 `*` 号。 |
| `git branch -a` | 列出所有本地和远程分支。 |
| `git branch <branch_name>` | 创建一个新分支。 |
| `git checkout <branch_name>` | 切换到指定分支。 |
| `git switch <branch_name>` | **（Git 2.23+）** 专门用于切换分支的命令，比 `checkout` 更语义化。 |
| `git checkout -b <branch_name>` | 创建并立即切换到新分支。**经典组合命令**。 |
| `git switch -c <branch_name>` | **（Git 2.23+）** 同上，创建并切换到新分支。 |
| `git merge <branch_name>` | 将指定分支合并到**当前分支**。 |
| `git branch -d <branch_name>` | 删除一个**已合并**的分支（安全删除）。 |
| `git branch -D <branch_name>` | **强制删除**一个分支，即使它还没有被合并。**危险操作！** |
| `git mergetool` | 使用配置好的合并工具来解决合并冲突。 |

#### 合并细节：
- **快进合并（Fast-forward）**：如果目标分支是当前分支的直接上游，Git 只会将指针向前移动。不会产生新的提交。
- **三方合并（3-way Merge）**：如果分支已经分叉，Git 会创建一个新的“合并提交”，将两个分支的历史联系在一起。这可能会产生**冲突**，需要手动解决。

---

### 第五部分：远程协作

与远程仓库（如 GitHub, GitLab）交互的命令。

| 命令 | 解释与细节 |
| :--- | :--- |
| `git remote -v` | 查看已配置的远程仓库及其 URL。 |
| `git remote add <name> <url>` | 添加一个新的远程仓库，并为其起一个简称（通常叫 `origin`）。 |
| `git fetch <remote>` | 从远程仓库下载所有数据（分支、提交等）到本地，但**不会自动合并**到你的工作区。**安全操作**。 |
| `git pull <remote> <branch>` | **=`git fetch` + `git merge`**。从远程拉取更新并立即合并到当前分支。 |
| `git pull --rebase` | **=`git fetch` + `git rebase`**。拉取更新并使用变基而非合并，可以使历史线更整洁。 |
| `git push <remote> <branch>` | 将本地分支的提交推送到远程仓库。 |
| `git push -u origin main` | **首次推送**分支时使用 `-u` (或 `--set-upstream`) 参数，建立本地分支与远程分支的跟踪关系。之后可以直接用 `git push`。 |
| `git push --force-with-lease` | **比 `--force` 更安全**的强制推送。它会检查远程分支是否有你未知的新提交，如果没有才强制覆盖。**谨慎使用！** |
| `git remote show <remote>` | 显示某个远程仓库的详细信息。 |

---

### 第六部分：撤销与回退

用于修正错误，是 Git 的强大之处，但也需要谨慎使用。

| 命令 | 解释与细节 | 适用场景 |
| :--- | :--- | :--- |
| `git commit --amend` | **修补提交**。将暂存区的更改与最后一次提交合并，**生成一个新的提交ID**。可以用来修改提交信息或漏掉的文件。 | **仅限未推送的提交** |
| `git reset --soft <commit_id>` | 回退到某个提交，但**保留工作区和暂存区**的更改。之后的更改处于 `git add` 后的状态。 | 撤销提交，但想保留更改重新提交 |
| `git reset --mixed <commit_id>` | **默认选项**。回退到某个提交，**保留工作区**的更改，但重置暂存区。之后的更改处于未 `git add` 的状态。 | 撤销提交和 `git add` |
| `git reset --hard <commit_id>` | **彻底回退**。回退到某个提交，**丢弃工作区和暂存区**的所有更改，完全恢复到那次提交的状态。**非常危险！** | 彻底抛弃之后的更改 |
| `git revert <commit_id>` | **安全撤销**。创建一个**新的提交**，其内容是指定提交的相反操作（逆向补丁）。历史记录会被保留。 | **推荐用于已推送的提交** |

---

### 第七部分：储藏与清理

用于临时保存工作现场。

| 命令 | 解释与细节 |
| :--- | :--- |
| `git stash` | 将当前工作区和暂存区的修改临时储藏起来，让工作区变干净。 |
| `git stash save "message"` | 储藏并添加说明信息。 |
| `git stash list` | 列出所有的储藏。 |
| `git stash pop` | 应用最近一次的储藏，并**将其从储藏列表中删除**。 |
| `git stash apply` | 应用最近一次的储藏，但**不将其从列表中删除**。 |
| `git stash drop` | 删除指定的储藏。 |
| `git stash clear` | 清空所有储藏。 |
| `git clean -fd` | **危险！** 删除所有未跟踪的文件和目录（`-f` 强制，`-d` 包括目录）。通常与 `git reset --hard` 结合使用来彻底还原。 |

---

### 第八部分：标签

用于标记重要的节点（如发布版本）。

| 命令 | 解释与细节 |
| :--- | :--- |
| `git tag` | 列出所有标签。 |
| `git tag -a v1.0 -m "Version 1.0"` | 创建一个带注解的标签。 |
| `git tag v1.0-lightweight` | 创建一个轻量标签（只是一个指向提交的指针）。 |
| `git show v1.0` | 显示某个标签的详细信息。 |
| `git push origin v1.0` | 将单个标签推送到远程。 |
| `git push origin --tags` | 将所有本地标签推送到远程。 |