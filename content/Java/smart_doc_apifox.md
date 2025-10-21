Title: Java项目集成smart-doc
Date: 2025-02-03 10:20
Modified: 2025-09-03 10:20
Author: shiyi
tags: Java
keywords: 告别注解污染，让API文档生成更优雅、更智能
summary: 告别注解污染，让API文档生成更优雅、更智能
lang: zh
status: published
Slug: smart_doc_apifox
url: smart_doc_apifox


# 无侵入式接口文档生成：Java项目集成smart-doc实践

> 告别注解污染，让API文档生成更优雅、更智能

在Java后端开发中，API文档的维护一直是个令人头疼的问题。传统的Swagger/OpenAPI需要我们在代码中大量使用注解，这不仅污染了代码，还增加了维护成本。今天我要介绍一款无侵入式的接口文档生成工具——**smart-doc**，它将彻底改变你编写API文档的方式。

## 一、smart-doc是什么？

smart-doc是一款基于**源码**和**注释**生成API文档的工具，完全基于Java注释，不需要在代码中嵌入任何注解。它通过分析代码的泛型定义、注释等信息，自动生成Restful API文档，真正实现了代码与文档的分离。

### 核心特性：
- **零注解侵入**：只需编写标准的Java注释
- **自动推导**：智能分析参数、返回值
- **多格式支持**：支持HTML、Markdown、Postman等格式
- **OpenAPI兼容**：可生成OpenAPI 3.0+规范的文档
- **强大插件**：Maven、Gradle插件一键集成

## 二、为什么选择smart-doc？

### 与传统Swagger对比

| 特性 | Swagger | smart-doc |
|------|---------|-----------|
| 代码侵入性 | 需要大量注解 | 完全无侵入 |
| 文档质量 | 依赖注解完整性 | 基于标准注释 |
| 维护成本 | 代码修改需同步更新注解 | 注释即文档 |
| 学习成本 | 需要学习注解用法 | 使用标准Java注释 |

### 适用场景
- 追求代码整洁，不希望注解污染的业务系统
- 已有完善注释的遗留系统改造
- 需要生成多种格式文档的项目
- 希望降低团队学习成本的场景

## 三、快速开始

### 3.1 添加Maven插件

```xml
<plugin>
    <groupId>com.github.shalousun</groupId>
    <artifactId>smart-doc-maven-plugin</artifactId>
    <version>2.7.7</version>
    <configuration>
        <configFile>./src/main/resources/smart-doc.json</configFile>
        <projectName>Smart-Doc示例项目</projectName>
    </configuration>
</plugin>
```

### 3.2 创建配置文件

在`src/main/resources`下创建`smart-doc.json`：

```json
{
  "serverUrl": "http://localhost:8080",
  "isStrict": false,
  "allInOne": true,
  "outPath": "./src/main/resources/static/doc",
  "coverOld": true,
  "packageFilters": "com.example.controller.*",
  "projectName": "用户管理系统",
  "skipTransientField": true,
  "sortByTitle": false,
  "showAuthor": true,
  "requestExample": true,
  "responseExample": true
}
```

### 3.3 编写规范的代码注释

```java
/**
 * 用户管理控制器
 *
 * @author smart-doc
 * @version 1.0
 */
@RestController
@RequestMapping("/api/user")
public class UserController {
    
    /**
     * 根据用户ID查询用户信息
     *
     * @param userId 用户ID
     * @return 用户详细信息
     * @apiNote 这是一个获取用户信息的接口，需要传入有效的用户ID
     */
    @GetMapping("/{userId}")
    public ResponseEntity<UserVO> getUserById(
            @PathVariable @Min(1) Long userId) {
        // 业务逻辑
        UserVO user = userService.getById(userId);
        return ResponseEntity.ok(user);
    }
    
    /**
     * 创建新用户
     *
     * @param userDTO 用户创建请求
     * @return 创建结果
     */
    @PostMapping
    public ResponseEntity<Result<UserVO>> createUser(
            @Valid @RequestBody UserCreateDTO userDTO) {
        UserVO user = userService.create(userDTO);
        return ResponseEntity.ok(Result.success(user));
    }
}

/**
 * 用户创建请求DTO
 */
public class UserCreateDTO {
    /**
     * 用户名
     */
    @NotBlank(message = "用户名不能为空")
    private String username;
    
    /**
     * 邮箱地址
     */
    @Email(message = "邮箱格式不正确")
    private String email;
    
    /**
     * 手机号码
     */
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;
    
    // getter/setter省略
}

/**
 * 用户视图对象
 */
public class UserVO {
    /**
     * 用户ID
     */
    private Long id;
    
    /**
     * 用户名
     */
    private String username;
    
    /**
     * 创建时间
     */
    private LocalDateTime createTime;
    
    // getter/setter省略
}
```

### 3.4 生成文档

执行Maven命令生成文档：

```bash
mvn smart-doc:html
```

或者在IDE中直接运行Maven插件的目标。

运行结束后会在项目resources/static/doc目录下生成html版的接口文档

结果如下：

[![图1]({static}/images/smart_doc_apifox/1.png){: width="50%"}]({static}/images/smart_doc_apifox/1.png){: data-lightbox="gallery" .lightbox-image }

这个时候通过右键浏览器打开index.html文件就会发现完整的接口文档

smart-doc不仅是一个工具，更是一种开发理念的体现——优秀的代码应该自解释，而文档应该是代码的自然产物。尝试在项目中引入smart-doc，你会发现编写和维护API文档从未如此轻松！

---

**资源链接**：
- [smart-doc官方文档](https://smart-doc-group.github.io/)
- [示例项目源码](https://github.com/smart-doc-group/smart-doc-example)
- [Maven中央仓库](https://mvnrepository.com/artifact/com.github.shalousun/smart-doc)