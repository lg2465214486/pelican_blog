Title: 全局异常处理与统一返回结构最佳实践  
Date: 2025-10-01 19:10  
Modified: 2025-10-01 19:10  
Author: shiyi  
tags: Java  
keywords: Spring Boot, 全局异常处理, 统一返回结构, @ControllerAdvice  
summary: 统一异常返回结构是一套后端项目的基石，本篇从零构建最优雅的全局异常体系  
lang: zh  
status: published  
Slug: global_exception_handler  
url: global_exception_handler  

---

在后端开发中，最容易被忽视但最重要的部分之一，就是 **异常处理**。  
没有统一的异常体系，项目就会出现：

❌ Controller 层 try-catch 满天飞  
❌ 返回格式不统一（有的返回JSON、有的返回字符串）  
❌ 错误信息暴露敏感内容  
❌ 前端无法知道哪种错误该怎么处理  

而成熟的后台系统必须做到：

✅ 所有接口异常统一出口  
✅ 统一 JSON 返回结构  
✅ 自定义业务异常（如“用户不存在”、“余额不足”）  
✅ 记录详细日志便于排查  
✅ 控制错误信息外泄风险  

今天，我们将从零实现一套可复用、可扩展且非常优雅的 Spring Boot 全局异常处理体系。

---

## 一、统一返回结构设计

首先设计一个标准的响应结构，建议如下：

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ApiResponse<T> {

    private int code;       // 状态码
    private String msg;     // 提示信息
    private T data;         // 业务数据

    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(200, "success", data);
    }

    public static <T> ApiResponse<T> error(int code, String msg) {
        return new ApiResponse<>(code, msg, null);
    }
}
```

优点：

✅ 结构统一
✅ 可扩展性强
✅ 前端处理逻辑一致
✅ 支持泛型

---

## 二、自定义业务异常（核心）

所有业务错误（如库存不足、用户不存在、权限不足）都应该用自定义异常表示。

```java
public class BusinessException extends RuntimeException {

    private final int code;

    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }

    public int getCode() {
        return code;
    }
}
```

以后要抛出业务异常时：

```java
if (user == null) {
    throw new BusinessException(404, "用户不存在");
}
```

代码清爽且易读。

---

## 三、创建全局异常处理器（核心能力）

Spring Boot 提供 `@ControllerAdvice` + `@ExceptionHandler`，用于捕获所有异常。

```java
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 处理业务异常
     */
    @ExceptionHandler(BusinessException.class)
    public ApiResponse<?> handleBusinessException(BusinessException ex) {
        log.warn("业务异常: {}", ex.getMessage());
        return ApiResponse.error(ex.getCode(), ex.getMessage());
    }

    /**
     * 处理参数校验异常
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ApiResponse<?> handleValidException(MethodArgumentNotValidException ex) {
        String msg = ex.getBindingResult().getFieldError().getDefaultMessage();
        return ApiResponse.error(400, msg);
    }

    /**
     * 处理所有未捕获异常
     */
    @ExceptionHandler(Exception.class)
    public ApiResponse<?> handleException(Exception ex) {
        log.error("系统异常: ", ex);
        return ApiResponse.error(500, "系统繁忙，请稍后再试");
    }
}
```

三种情况全部覆盖：

| 类型                              | 说明             |
| ------------------------------- | -------------- |
| BusinessException               | 所有自定义业务错误      |
| MethodArgumentNotValidException | 参数校验错误（@Valid） |
| Exception                       | 系统未知异常（兜底）     |

---

## 四、参数校验（Bean Validation）自动接入异常体系

在 DTO 上添加：

```java
public class UserCreateRequest {

    @NotBlank(message = "用户名不能为空")
    private String username;

    @Email(message = "邮箱格式不正确")
    private String email;
}
```

Controller：

```java
@PostMapping("/create")
public ApiResponse<?> createUser(@Valid @RequestBody UserCreateRequest request) {
    ...
}
```

如果参数不合法，将自动被 `handleValidException()` 捕获并返回：

```json
{
  "code": 400,
  "msg": "邮箱格式不正确",
  "data": null
}
```

无需手写 try-catch，非常优雅。

---

## 五、统一 Controller 返回结构（可选增强）

如果你希望所有 Controller 自动包装成 ApiResponse，可以使用 ResponseBodyAdvice：

```java
@RestControllerAdvice
public class ApiResponseWrapper implements ResponseBodyAdvice<Object> {

    @Override
    public boolean supports(MethodParameter methodParameter, Class converterType) {
        return true;
    }

    @Override
    public Object beforeBodyWrite(Object body, MethodParameter methodParameter,
                                  MediaType mediaType, Class converterType,
                                  ServerHttpRequest request, ServerHttpResponse response) {
        if (body instanceof ApiResponse) {
            return body; // 已经包装过
        }
        return ApiResponse.success(body);
    }
}
```

效果：

接口返回原对象：

```java
return userVO
```

实际响应：

```json
{
  "code": 200,
  "msg": "success",
  "data": { ...userVO }
}
```

强迫症福音。

---

## 六、为什么一定要做全局异常处理？

| 功能          | 意义             |
| ----------- | -------------- |
| 统一返回格式      | 前端一次性适配        |
| 日志统一输出      | 方便日志系统收集、分析    |
| 屏蔽敏感异常      | 防止泄露系统信息       |
| 业务异常与系统异常分离 | 便于监控与运维        |
| 开发体验提升      | 无需手写 try-catch |

---

## 七、日志输出最佳实践（配合 logback）

业务异常建议用 `warn`：

```java
log.warn("业务异常: {}", ex.getMessage());
```

系统异常用 `error`：

```java
log.error("系统异常:", ex);
```

这样在日志平台中也能按等级分类，清晰明了。

---

## 八、最终效果展示

当系统出现业务异常：

```json
{
  "code": 404,
  "msg": "用户不存在",
  "data": null
}
```

参数错误：

```json
{
  "code": 400,
  "msg": "手机号不能为空",
  "data": null
}
```

系统异常：

```json
{
  "code": 500,
  "msg": "系统繁忙，请稍后再试",
  "data": null
}
```

前端无需额外适配，不同类型错误在结构上保持完全一致。

---