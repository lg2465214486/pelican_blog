Title: MySQL 查询优化技巧：从慢 SQL 到高性能查询  
Date: 2025-10-28 20:25  
Modified: 2025-10-28 20:25  
Author: shiyi  
tags: MySQL  
keywords: MySQL, SQL优化, 索引优化, EXPLAIN, 覆盖索引  
summary: 掌握这些技巧，让你的查询速度从秒级进入毫秒级  
lang: zh  
status: published  
Slug: mysql_query_optimization  
url: mysql_query_optimization

---

在后端开发中，SQL 性能常常是系统瓶颈之一。  

一次不合理的查询，可能导致：

❌ 接口超时  
❌ 数据库 CPU 飙升  
❌ 锁等待加剧  
❌ 整个系统雪崩  

而一次合理的优化，则能让一个 2 秒的查询缩短到 20ms。

本文总结了 MySQL 最常用也最实用的查询优化技巧，覆盖慢查询排查、执行计划分析、索引优化、SQL 重写等场景。

---

# 一、开启慢查询日志（第一步先找到问题）

在优化 SQL 前，你必须知道“哪些 SQL 慢”。

在 MySQL 配置文件中启用慢查询：

```ini
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1   # 超过 1 秒记录
log_queries_not_using_indexes = 1
```

然后查看：

```bash
mysqldumpslow slow.log
```

你会找到最常被执行、最慢的 SQL，按“执行次数”排序特别有用。

---

# 二、使用 EXPLAIN 分析执行计划

拿到 SQL 后，第一件事：

```sql
EXPLAIN SELECT * FROM user WHERE email = 'test@test.com';
```

重点关注：

| 字段    | 说明               |
| ----- | ---------------- |
| type  | 访问类型（越往下越差）      |
| key   | 使用的索引            |
| rows  | 预计扫描行数           |
| Extra | 是否使用了覆盖索引/是否发生回表 |

### 最佳访问类型：

```
const > eq_ref > ref > range > index > ALL
```

出现 **ALL** = 全表扫描 → 必须优化。

### rows 越低越好

rows 代表 MySQL 预估要扫描多少行。

例如：

```
rows = 450000   ❌
rows = 3        ✅
```

rows 高通常代表：

* 没走索引
* 条件不精准
* 索引设计不合理

---

# 三、创建合适的索引（优化 SQL 的核心）

## 1. 精确匹配的字段需要索引

```sql
SELECT * FROM user WHERE email = 'xxx';
```

必须在 `email` 上建立索引：

```sql
ALTER TABLE user ADD INDEX idx_email(email);
```

---

## 2. 使用覆盖索引提高性能

覆盖索引 = 查询只需要索引中的字段，不需要回表。

```sql
SELECT id, username FROM user WHERE email = 'xxx';
```

如果 index(email, id, username)，则无需回表，性能极高。

---

## 3. 尽量使用“最左前缀原则”的联合索引

联合索引：

```
INDEX(a, b, c)
```

可用于：

✅ a

✅ a + b

✅ a + b + c

不能用于：

❌ b

❌ b + c

设计索引时应该优先将**区分度高的字段放前面**。

例如：

```
(性别, 年龄, 城市)
```

几乎没意义，因为性别只有两个值。

---

# 四、避免索引失效（非常关键）

索引常见失效场景：

### 1. 使用函数

```sql
WHERE DATE(create_time) = '2025-01-01'
```

优化为：

```sql
WHERE create_time >= '2025-01-01' 
  AND create_time < '2025-01-02'
```

---

### 2. like 前置通配符

```sql
WHERE name LIKE '%abc'
```

无法走索引。

优化：

```sql
WHERE name LIKE 'abc%'
```

---

### 3. 字段类型不一致

```sql
WHERE phone = 13333333333   -- phone 是 varchar
```

改为：

```sql
WHERE phone = '13333333333'
```

---

### 4. OR 条件未全走索引

```sql
WHERE email = 'a@test.com' OR phone = '13333333333'
```

其中一个没索引 → 整条都失效。

优化方法：

* 给两个字段都加索引
* 或拆成两条 SQL

---

# 五、优化分页查询（limit 100k, 20）

分页深度越大，越慢：

```sql
SELECT * FROM user LIMIT 100000, 20;
```

MySQL 实际做的是：

> 扫 100020 行 → 丢掉前 100000 行 → 返回后 20 行
> 非常慢

优化方法：

## 1. 覆盖索引 + 子查询

```sql
SELECT *
FROM user
WHERE id >= (
    SELECT id FROM user ORDER BY id LIMIT 100000, 1
)
LIMIT 20;
```

---

## 2. 使用“游标分页”（最推荐）

```sql
SELECT * FROM user
WHERE id > last_id
ORDER BY id
LIMIT 20;
```

性能可提升数十倍。

---

# 六、避免 SELECT *

```sql
SELECT * FROM orders;
```

问题：

* 回表成本高
* 占用带宽
* 无法使用覆盖索引
* 字段变更引发风险

替换为：

```sql
SELECT id, order_no, status FROM orders;
```

---

# 七、减少关联查询的数量

多表 JOIN 不一定慢，但 JOIN 太多一定慢。

## 推荐：一次查 ID → 批量 in 查询

例如订单 + 用户信息：

### 一条 SQL JOIN 三四张表：

```sql
SELECT *
FROM order o
JOIN user u ON o.user_id = u.id
JOIN ...
```

### 推荐方式：

1. 先查订单列表
2. 使用用户 ID 列表批量查询用户

```
SELECT * FROM user WHERE id IN (1, 2, 3, 4);
```

缓存友好、延迟低、可水平扩展。

---

# 八、常见 SQL 重写技巧

### 使用 EXISTS 替代 IN（大表场景）

```sql
SELECT * FROM product WHERE id IN (SELECT product_id FROM order_item);
```

改为：

```sql
SELECT * FROM product p WHERE EXISTS (
  SELECT 1 FROM order_item oi WHERE oi.product_id = p.id
);
```

更高效。

---

### 避免在 WHERE 中进行计算

```sql
WHERE amount * 2 > 100
```

改为：

```sql
WHERE amount > 50
```

---

### 避免负向条件

```sql
WHERE status != 1
```

改为：

```sql
WHERE status IN (2, 3, 4)
```

---

# 九、善用索引统计信息

```sql
SHOW INDEX FROM user;
SHOW TABLE STATUS LIKE 'user';
```

查看表大小、行数、索引分布，可以帮助你更好地优化。

---