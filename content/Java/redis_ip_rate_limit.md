Title: 接口防刷防爬：基于 IP + Redis 实现访问频率限制  
Date: 2024-10-01 18:05  
Modified: 2024-10-01 18:05  
Author: shiyi  
tags: Java  
keywords: Redis, 限流, 防刷, 接口安全, Spring Boot  
summary: 一文教你用Redis和注解实现轻量级防刷机制  
lang: zh  
status: published  
Slug: redis_ip_rate_limit  
url: redis_ip_rate_limit  

---

在后端开发中，接口被恶意刷取或频繁访问是常见问题。  
如果没有限制机制，轻则浪费带宽，重则压垮数据库。  

很多人一上来就引入复杂的限流框架（如 Sentinel、Guava RateLimiter），但其实在中小项目中，我们只需一个简单优雅的方案：  
——**利用 Redis + 注解 + 拦截器** 实现 IP 级别的访问频率限制。  

轻量、可控、可扩展，不依赖任何额外框架。

---

## 一、核心思路

原理非常简单：

> 当某个 IP 在指定时间窗口内访问接口次数超过限制，就直接拒绝请求。

流程如下：

1. 获取请求的 IP 地址  
2. 使用 Redis 以 “IP+接口路径” 为键  
3. 设置访问计数与过期时间  
4. 超出阈值则返回「请求过于频繁」

示例：  
```text
Key: rate_limit:/api/user/login:192.168.0.12  
Value: 5 (当前访问次数)  
TTL: 60s
```

---

## 二、环境准备

在 `pom.xml` 中添加 Redis 依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

同时在 `application.yml` 中配置 Redis：

```yaml
spring:
  redis:
    host: localhost
    port: 6379
    password:
```

---

## 三、自定义限流注解

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RateLimit {
    int limit() default 10;      // 最大访问次数
    int window() default 60;     // 时间窗口（秒）
}
```

通过注解，我们可以在任意接口上声明防刷策略，非常灵活。

---

## 四、获取客户端 IP 工具类

```java
import jakarta.servlet.http.HttpServletRequest;

public class IpUtils {
    public static String getClientIp(HttpServletRequest request) {
        String[] headers = {
                "x-forwarded-for",
                "Proxy-Client-IP",
                "WL-Proxy-Client-IP",
                "HTTP_CLIENT_IP",
                "HTTP_X_FORWARDED_FOR"
        };
        for (String header : headers) {
            String ip = request.getHeader(header);
            if (ip != null && ip.length() != 0 && !"unknown".equalsIgnoreCase(ip)) {
                return ip.split(",")[0];
            }
        }
        return request.getRemoteAddr();
    }
}
```

---

## 五、编写拦截器实现限流逻辑

```java
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.concurrent.TimeUnit;

@Component
@RequiredArgsConstructor
public class RateLimitInterceptor implements HandlerInterceptor {

    private final StringRedisTemplate redisTemplate;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (!(handler instanceof HandlerMethod method)) {
            return true;
        }

        RateLimit annotation = method.getMethodAnnotation(RateLimit.class);
        if (annotation == null) {
            return true;
        }

        String ip = IpUtils.getClientIp(request);
        String key = "rate_limit:" + request.getRequestURI() + ":" + ip;

        int limit = annotation.limit();
        int window = annotation.window();

        Long count = redisTemplate.opsForValue().increment(key);
        if (count == 1) {
            redisTemplate.expire(key, window, TimeUnit.SECONDS);
        }

        if (count != null && count > limit) {
            response.setStatus(429);
            response.setContentType("application/json;charset=UTF-8");
            response.getWriter().write("{\"code\":429,\"msg\":\"请求过于频繁，请稍后再试\"}");
            return false;
        }
        return true;
    }
}
```

---

## 六、注册拦截器

```java
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final RateLimitInterceptor rateLimitInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(rateLimitInterceptor)
                .addPathPatterns("/api/**");
    }
}
```

---

## 七、使用注解开启限流

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/api/user")
public class UserController {

    @RateLimit(limit = 5, window = 60)
    @GetMapping("/profile")
    public String getUserProfile() {
        log.info("访问用户资料接口");
        return "访问成功";
    }
}
```

**效果：**
同一个 IP 在 60 秒内最多只能访问 `/api/user/profile` 接口 5 次，超过将返回：

```json
{
  "code": 429,
  "msg": "请求过于频繁，请稍后再试"
}
```