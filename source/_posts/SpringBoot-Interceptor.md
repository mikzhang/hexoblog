---
title: SpringBoot-Interceptor
date: 2017-01-06 12:52:48
categories: SpringBoot
tags:
    - SpringBoot
    - Interceptor
---

SpringBoot 下添加 Interceptor

<!-- more -->

## xml方式
```
<mvc:interceptors>
    <bean class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor"/>
    <mvc:interceptor>
        <mvc:mapping path="/**"/>
        <mvc:exclude-mapping path="/admin/**"/>
        <bean class="org.springframework.web.servlet.theme.ThemeChangeInterceptor"/>
    </mvc:interceptor>
    <mvc:interceptor>
        <mvc:mapping path="/secure/*"/>
        <bean class="org.example.SecurityInterceptor"/>
    </mvc:interceptor>
</mvc:interceptors>
```

## SpringBoot 中 @Configuration 方式

### 创建 Interceptor
```
@Component
public class Interceptor1 extends HandlerInterceptorAdapter {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("preHandle1");
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView) throws Exception {
        System.out.println("postHandle1");
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable Exception ex) throws Exception {
        System.out.println("afterCompletion1");
    }

}
```
Interceptor1 同理

### 创建 InterceptorConfig
```
@Configuration
public class InterceptorConfig extends WebMvcConfigurerAdapter {

    @Autowired
    private Interceptor1 interceptor1;
    @Autowired
    private Interceptor2 interceptor2;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(interceptor1).addPathPatterns("/**");
        registry.addInterceptor(interceptor2).addPathPatterns("/**")/*.excludePathPatterns("/api/xxx")*/;
    }
}
```

## 结果
访问 http://localhost:8080/greeting
```
preHandle1
preHandle2
postHandle2
postHandle1
afterCompletion2
afterCompletion1
```

ref:
[http://jinnianshilongnian.iteye.com/blog/1670856](http://jinnianshilongnian.iteye.com/blog/1670856)