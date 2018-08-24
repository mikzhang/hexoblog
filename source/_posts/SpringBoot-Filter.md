---
title: SpringBoot-Filter
date: 2017-01-06 12:52:48
categories: SpringBoot
tags:
    - SpringBoot
    - Filter
---

SpringBoot 下添加 Filter

<!-- more -->

## xml方式
传统的javaEE增加Filter是在web.xml中配置，如以下代码
```
<filter>
   <filter-name>TestFilter</filter-name>
    <filter-class>com.cppba.filter.TestFilter</filter-class>
</filter>
<filter-mapping>
  <filter-name>TestFilter</filter-name>
  <url-pattern>/*</url-pattern>
  <init-param>
    <param-name>paramName</param-name>
    <param-value>paramValue</param-value>
  </init-param>
</filter-mapping>
```

## SpringBoot 中 @Bean 方式

### 创建 Filter
```
package com.cppba.filter;
 
import javax.servlet.*;
import java.io.IOException;
 
public class TestFilter implements Filter {
  @Override
  public void init(FilterConfig filterConfig) throws ServletException {
 
  }
 
  @Override
  public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain)
      throws IOException, ServletException {
    System.out.println("TestFilter");
    chain.doFilter(servletRequest, servletResponse);//放行,否则被拦截
  }
 
  @Override
  public void destroy() {
 
  }
}
```

### Application 中增加一个@bean
```
@Bean
 public FilterRegistrationBean testFilterRegistration() {
 
   FilterRegistrationBean registration = new FilterRegistrationBean();
   registration.setFilter(new TestFilter());
   registration.addUrlPatterns("/*");
   registration.addInitParameter("paramName", "paramValue");
   registration.setName("testFilter");
   registration.setOrder(1);
   return registration;
 }
```

### 结果
启动项目会看到控制台打印如下
![20180824195419](20180824195419.png)
访问项目http://127.0.0.1:8080/test， 看到控制台打印出:TestFilter
![20180824195459](20180824195459.png)


## SpringBoot 中 @WebFilter 方式

### 更改 Filter
```
package com.cppba.filter;
 
import javax.servlet.*;
import java.io.IOException;

@Component
@WebFilter(filterName = "testFilter1", urlPatterns = "/*")
@Order(1)
public class TestFilter implements Filter {
  @Override
  public void init(FilterConfig filterConfig) throws ServletException {
 
  }
 
  @Override
  public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain)
      throws IOException, ServletException {
    System.out.println("TestFilter");
    chain.doFilter(servletRequest, servletResponse);//放行,否则被拦截
  }
 
  @Override
  public void destroy() {
 
  }
}
```
比较核心的代码是自定义类上面加上 @WebFilter, 其中 @Order 注解表示执行过滤顺序，值越小，越先执行,
@compontent 注入Bean

### spring-boot的入口处加上scanBasePackages
```
@SpringBootApplication(scanBasePackages = "com.cppba")
public class Application {
  public static void main(String[] args) throws UnknownHostException {
    SpringApplication app = new SpringApplication(Application.class);
    Environment environment = app.run(args).getEnvironment();
  }
}
```

这种方法效果和上面版本一样

ref:
[Spring boot下添加filter](https://www.cnblogs.com/OnlyCT/p/7133639.html)


