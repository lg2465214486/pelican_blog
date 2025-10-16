Title: Oracle序列配合触发器实现插入数据时自增
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: oracle
keywords: Oracle序列配合触发器实现插入数据时自增
summary: Oracle序列配合触发器实现插入数据时自增
lang: zh
status: published
Slug: oracle_sequence_no
url: oracle_sequence_no




# Oracle序列配合触发器实现插入数据时自增

Oracle不能像MySQL/SQLServer那样设置主键自增

序列sequence+触发器trigger：实现数据表TBL_MESSAGE中的主键的自增

现有表：

```sql
create table TBL_MESSAGE(
	id number primary key,
	note varchar2(200) not null,
);
```

创建序列：

```sql
create sequence mess_seq
minvalue 1
maxvalue 99999999999
start with 1
increment by 1
nocache;
```
INCREMENT BY  -- 每次加几个 

START WITH  -- 从1开始计数 

NOMAXvalue -- 不设置最大值 

NOCYCLE -- 一直累加，不循环 

CACHE 20; --设置缓存cache个序列，如果系统down掉了或者其它情况将会导致序列不连续，也可以设置为---------NOCACHE

CURRVAL=返回 sequence的当前值  

NEXTVAL=增加sequence的值，然后返回 sequence 值(下一个sequence值)

当然这些属性都可以缺省

```sql
create sequence mess_seq;
```

## 下面进入正题

没有使用触发器的下使用序列如下：

```sql
insert into TBL_MESSAGE(id,note)
values(mess_seq.nextval,'第一条测试数据');
insert into TBL_MESSAGE(id,note)
values(mess_seq.nextval,'第二条测试数据');
insert into TBL_MESSAGE(id,note)
values(mess_seq.nextval,'第三条测试数据');
```

结果如下：
[![图1]({static}/images/oracle_sequence_no/1.png){: width="50%"}]({static}/images/oracle_sequence_no/1.png){: data-lightbox="gallery" .lightbox-image }

已经引用序列sequence实现了自增

但是，当在表中手动添加记录时，还是需要添加id

作为一个程序员这种重复的代码不想写那么多。

那么，怎么只输入note，然后保存、commit，实现id引用sequence自增呢？

现在使用触发器实现插入数据过程中id自增：

代码：

```sql
create or replace trigger tri_mes_id
	before insert on TBL_MESSAGE --作用表
	for each row --每行受影响
declare
	nextid number;
begin
	if :new.id is null or :new.id=0 then
		select mess_seq.nextval into nextid from dual;
	:new.id:=nextid;
	end if;
end tri_mes_id;
```
此时，只输入note，然后保存、commit，

id引用sequence实现了自增

测试：

```sql
insert into TBL_MESSAGE(note) values('第四条测试数据');
insert into TBL_MESSAGE(note) values('第五条测试数据');
insert into TBL_MESSAGE(note) values('第六条测试数据');
```

结果如下：

[![图2]({static}/images/oracle_sequence_no/2.png){: width="50%"}]({static}/images/oracle_sequence_no/2.png){: data-lightbox="gallery" .lightbox-image }

