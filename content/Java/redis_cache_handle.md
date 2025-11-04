Title: 基于 Redis 的注解式缓存设计@Cacheable实战
Date: 2024-10-01 18:50  
Modified: 2024-10-01 18:50  
Author: shiyi  
tags: Java  
keywords: Spring Cache, Redis, 缓存设计, @Cacheable, Spring Boot  
summary: 一文掌握 Redis + Spring Cache 注解式缓存的最佳实践  
lang: zh  
status: published  
Slug: redis_cache_handle
url: redis_cache_handle  

---

> 一文掌握 Redis + Spring Cache 注解式缓存的最佳实践

在现代后端开发中，「性能瓶颈」往往不在 CPU，而在 I/O：  
数据库访问慢、外部 API 慢、复杂查询慢……  

这些场景有一个共同解决方案：**缓存**。  
而 Spring Boot 已经提供了一个非常优雅的缓存体系 —— **Spring Cache**。  
只需一个注解，就能轻松实现读写缓存、自动失效、异步更新等操作。

今天，我们结合 **Redis + Spring Cache**，讲解一个真正实用的注解式缓存方案，让你的接口性能直接提升一个维度。

---

## 一、Spring Cache 是什么？

Spring Cache 是一个统一的缓存访问抽象。其核心思想是：

> “我不关心你底层是 Redis / Caffeine / 内存缓存，我用注解就能完成所有缓存逻辑。”

常用注解包括：

| 注解 | 说明 |
|------|------|
| `@Cacheable` | 查询时自动从缓存读取，不存在则执行方法并缓存结果 |
| `@CachePut` | 每次执行方法并刷新缓存 |
| `@CacheEvict` | 清除缓存 |
| `@Caching` | 组合多个缓存规则 |

---

## 二、准备工作：引入 Redis 与 Spring Cache

在 `pom.xml` 中加入依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>

<dependency>
    <groupId>com.fasterxml.jackson.datatype</groupId>
    <artifactId>jackson-datatype-jsr310</artifactId>
</dependency>
````

---

## 三、开启 Spring Cache

在启动类或配置类上启用缓存：

```java
@EnableCaching
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

---

## 四、配置 Redis 缓存序列化（最佳实践）

Spring 默认 JDK 序列化不推荐，会出现乱码且体积大。
我们使用 Jackson 作为 Redis 序列化工具。

```java
@Configuration
public class RedisConfig {

    @Bean
    public RedisCacheConfiguration redisCacheConfiguration() {
        return RedisCacheConfiguration.defaultCacheConfig()
                .serializeKeysWith(RedisSerializationContext
                        .SerializationPair.fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(RedisSerializationContext
                        .SerializationPair.fromSerializer(jacksonSerializer()))
                .entryTtl(Duration.ofMinutes(30));   // 默认 30 分钟过期
    }

    @Bean
    public Jackson2JsonRedisSerializer<Object> jacksonSerializer() {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.activateDefaultTyping(
                LaissezFaireSubTypeValidator.instance,
                ObjectMapper.DefaultTyping.NON_FINAL
        );
        return new Jackson2JsonRedisSerializer<>(objectMapper, Object.class);
    }
}
```

这样缓存的对象可读性强、不丢失类型信息。

---

## 五、开始使用 @Cacheable

假设我们有一个用户查询接口，经常被调用：

```java
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    @Cacheable(cacheNames = "user", key = "#id", unless = "#result == null")
    public UserVO getUserById(Long id) {
        System.out.println("查询数据库中...");
        return userRepository.findUser(id);
    }
}
```

### 解释：

* `cacheNames = "user"` → Redis 的缓存前缀，将存为：

  ```
  user::1
  ```
* `key = "#id"` → 缓存键为方法入参
* `unless = "#result == null"` → 查询结果为 null 时不缓存
* 方法第一次执行会打印“查询数据库中…”，第二次开始则直接从 Redis 读取，性能显著提升。

---

## 六、@CachePut：更新缓存

当用户资料被修改时，需要刷新缓存：

```java
@CachePut(cacheNames = "user", key = "#user.id")
public UserVO updateUser(UserVO user) {
    userRepository.update(user);
    return user;
}
```

每次调用都会执行数据库更新，同时更新缓存。

---

## 七、@CacheEvict：删除缓存

当用户删除账户时，需要清除缓存：

```java
@CacheEvict(cacheNames = "user", key = "#id")
public void deleteUser(Long id) {
    userRepository.deleteById(id);
}
```

支持清空整个缓存空间：

```java
@CacheEvict(cacheNames = "user", allEntries = true)
public void clearAll() {}
```

---

## 八、缓存雪崩/穿透/击穿的进阶设计

虽然注解方式很简单，但我们仍然需要应对高并发下的常见问题：

### 1. 缓存穿透

用户请求不存在的 Key
解决方案：

* `unless = "#result == null"` 避免缓存 null
* 或使用「布隆过滤器」提前判断

###  2. 缓存击穿

热点 Key 过期瞬间大量请求同时打入数据库
解决方案：

* 强制给热点数据加「互斥锁」
* 或使用随机过期时间避免同时失效

###  3. 缓存雪崩

大量缓存同一时间失效
解决方案：

* 设置过期时间随机值：

  ```java
  .entryTtl(Duration.ofMinutes(30))
  .computePrefixWith(cacheName -> cacheName + ":" + RandomUtil.randomInt(5))
  ```

在 Spring Cache + Redis 的体系下，这些方案非常容易扩展。

---

## 九、查询逻辑示例：Redis 优先级

使用 @Cacheable 后，查询流程如下：

1. 查 Redis 是否有缓存
2. 没有 → 执行方法 → 将结果写入 Redis
3. 有缓存 → 直接返回

传统：

```
Controller → Service → DB
```

现在：

```
Controller → Redis →（必要时）DB
```

接口 QPS 轻松翻倍，数据库压力大幅降低。

---

> 写业务逻辑的时间越少，系统越可靠；缓存是提升性能最划算的手段。
