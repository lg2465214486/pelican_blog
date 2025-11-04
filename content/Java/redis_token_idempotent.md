Title: 高并发场景下的接口幂等性设计（Redis + Token）  
Date: 2024-10-01 20:00  
Modified: 2024-10-01 20:00  
Author: shiyi  
tags: Java  
keywords: 幂等性, Redis, Token, 高并发, Spring Boot  
summary: 防止重复下单、重复支付、接口多次提交的轻量级幂等解决方案  
lang: zh  
status: published  
Slug: redis_token_idempotent  
url: redis_token_idempotent  

---

> 防止重复下单、重复支付、接口多次提交的轻量级幂等解决方案

在高并发系统中，“重复请求”是最常见的问题之一，例如：

- 用户连续点了两次「支付」
- 网络超时导致客户端自动重试
- 前端重复提交表单
- 用户刷新页面重复发送请求
- 异步任务或 MQ 消费重复执行  

如果没有幂等校验，就会出现：

❌ 重复下单  
❌ 重复支付  
❌ 库存超卖  
❌ 业务数据错乱  

业务越关键（支付/订单/库存），幂等性越重要。

今天我们用 **Redis + Token + 注解 + 拦截器** 实现一个轻量级且优雅的接口幂等方案，适合所有 Spring Boot 项目。

---

## 一、幂等性的本质是什么？

> 同一个请求，不管执行多少次，最终结果都保持一致。

例如：

| 场景 | 是否需要幂等？ |
|------|----------------|
| 创建订单接口 | ✅ 需要幂等 |
| 支付接口 | ✅ 必须幂等 |
| 查询接口 | ⭕ 天然幂等 |
| 更新用户信息 | ✅ 需要幂等 |
| 增加积分 | ✅ 需要幂等防止重复加分 |

幂等性实现方式有很多，比如：

- 数据库唯一约束  
- 状态机控制  
- 分布式锁  
- Token + Redis（今天介绍）  

其中 **“Token + Redis” 是后端最常用也最轻量的一种方案**。

---

## 二、核心方案设计

###✅ 思路：

1. 客户端访问接口前，先向后端请求一个幂等 Token  
2. 客户端在真正请求业务接口时，将 Token 放在 Header  
3. 后端用 Redis 检查这个 Token 是否已被使用  
4. 如果没用过 → 正常执行，并把 Token 设置为“已使用”  
5. 如果用过 → 直接返回“重复请求”

示例 Redis Key：

```

idempotent:order:create:ff1a2c3e

````

只允许使用一次。

---

## 三、步骤一：生成幂等 Token

在 Controller 中提供一个生成 Token 的接口：

```java
@RestController
@RequestMapping("/api/token")
public class TokenController {

    @Resource
    private StringRedisTemplate redisTemplate;

    @GetMapping("/create")
    public String createToken() {
        String token = UUID.randomUUID().toString();
        redisTemplate.opsForValue().set("idempotent:" + token, "1", Duration.ofMinutes(10));
        return token;
    }
}
````

前端调用后收到 token，例如：

```
a1e2f3d4-cd88-443f-bec1-98e5cbafbd5f
```

调用业务接口时，放入请求头：

```
Idempotent-Token: a1e2f3d4-cd88-443f-bec1-98e5cbafbd5f
```

---

## 四、步骤二：创建幂等注解

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Idempotent {
    String message() default "请勿重复提交";
}
```

任何接口只需加上 @Idempotent 即可实现幂等。

---

## 五、步骤三：编写拦截器实现幂等校验

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class IdempotentInterceptor implements HandlerInterceptor {

    private final StringRedisTemplate redisTemplate;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {

        if (!(handler instanceof HandlerMethod method)) {
            return true;
        }

        Idempotent idempotent = method.getMethodAnnotation(Idempotent.class);
        if (idempotent == null) {
            return true;
        }

        String token = request.getHeader("Idempotent-Token");
        if (token == null) {
            throw new BusinessException(400, "缺少 Idempotent-Token");
        }

        String key = "idempotent:" + token;

        Boolean success = redisTemplate.delete(key);
        if (Boolean.FALSE.equals(success)) {
            // Token 不存在或已经被消费
            throw new BusinessException(429, idempotent.message());
        }

        // 校验通过，继续执行
        return true;
    }
}
```

### 🔥 核心点：

采用 `redisTemplate.delete(key)`

✅ Redis 删除操作是原子性的
✅ 第一次成功删除 → 允许执行
✅ 第二次删除结果为 false → 拒绝重复请求

完美保证接口只执行一次。

---

## 六、步骤四：注册拦截器

```java
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final IdempotentInterceptor interceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(interceptor).addPathPatterns("/api/**");
    }
}
```

---

## 七、步骤五：业务接口加上注解即可

```java
@Slf4j
@RestController
@RequestMapping("/api/order")
public class OrderController {

    @Idempotent(message = "请勿重复下单")
    @PostMapping("/create")
    public ApiResponse<?> createOrder(@RequestBody OrderRequest request) {
        log.info("订单创建中...");
        return ApiResponse.success("创建成功");
    }
}
```

前端重复点击按钮 / 刷新页面 / 网络重试，都将收到：

```json
{
  "code": 429,
  "msg": "请勿重复下单",
  "data": null
}
```

---

## 八、为什么选择 Token 而不是锁？

对比锁的方案，Token 方案的优势：

| 能力         | Token + Redis | 分布式锁 |
| ---------- | ------------- | ---- |
| 防重复请求      | ✅ 强           | ✅ 强  |
| 防刷新提交      | ✅ 强           | ❌    |
| 前端可控（按钮禁用） | ✅ 强           | ❌    |
| 操作成本       | ✅ 低           | ❌ 高  |
| 性能         | ✅ 极高          | ✅ 高  |

Token 是前后端协作式方案，用户体验更好，性能更高。

---