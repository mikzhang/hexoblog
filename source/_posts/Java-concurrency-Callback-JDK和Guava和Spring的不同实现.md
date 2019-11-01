
---
title: Java-concurrency-Callback-JDK和Guava和Spring的不同实现
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - concurrency
---

Java-concurrency-Callback-JDK和Guava和Spring的不同实现

<!-- more -->

## 概念先行

随着移动互联网的蓬勃发展，手机App层出不穷，其业务也随之变得错综复杂。针对于开发人员来说，可能之前的一个业务只需要调取一次第三方接口以获取数据，而如今随着需求的增加，该业务需调取多个不同的第三方接口。通常，我们处理方法是让代码同步顺序的去调取这些接口。显然，调取接口数量的增加必然会造成响应时间的增加，势必会对系统性能造成一定影响。

为了保证系统响应迅速，需要寻找一种方法能够使调取接口能够异步执行，而java正好提供了类似的方法，在java.util.concurrent中包含了Future相关的类，运用其中的一些类可以进行异步计算，以减少主线程的等待时间。比如启动一个main方法，main中又包含了若干个其它任务，在不使用java future的情况下，main方法中的任务会同步阻塞执行，一个执行完成后，才能去执行另一个；如果使用java future，则main方法中的任务会异步执行，main方法不用等待一个任务的执行完成，只需往下执行就行。一个任务的执行结果又该怎么获取呢?这里就需要用到Future接口中的isDone()方法来判断任务是否执行完，如果完成完成则可获取结果，如果没有完成则需要等待，可见虽然主线程中的多个任务是异步执行，但是无法确定任务什么时候执行完成，只能通过不断去监听以获取结果，所以这里是阻塞的。这样，可能某一个任务执行时间很长会拖累整个主任务的执行。

针对这样的情况，google对java.util.concurrent中的许多类进行封装，最终产生了google guava框架，其中com.google.common.util中的ListenableFuture就是本文要叙述的重点。查看com.google.common.util，发现其中的很多类都是对java.util.concurrent的封装，以增加特有的方法。ListenableFuture扩展了future方法，增加了addListener方法，该方法可以监听线程，并通过回调函数来获取结果，达到线程之间异步非阻塞执行。

首先，了解下同步、异步、阻塞、非阻塞相关概念；其次，简单介绍java future和guava future相关技术，并通过示例代码进一步对其进行理解；最后，对java future和guava future进行比较。


**同步、异步、阻塞、非阻塞**

同步：所谓同步，就是在发出一个功能调用时，在没有得到结果之前，该调用就不返回。也就是必须一件一件事做,等前一件做完了才能做下一件事。

异步：异步的概念和同步相对。当一个异步过程调用发出后，调用者不能立刻得到结果。实际处理这个调用的部件在完成后，通过状态、通知和回调来通知调用者。

阻塞：阻塞调用是指调用结果返回之前，当前线程会被挂起（线程进入非可执行状态，在这个状态下，cpu不会给线程分配时间片，即线程暂停运行）。函数只有在得到结果之后才会返回。

非阻塞：非阻塞和阻塞的概念相对应，指在不能立刻得到结果之前，该函数不会阻塞当前线程，而会立刻返回。


## 关于异步回调

### Java自带的Future-Callback

#### Java  Future

**Executors创建线程池的几种常见方式**

|类名|	说明|
|:---|:---|
|newCachedThreadPool|	缓存型池子，先查看池中有没有以前建立的线程，如果有，就reuse；如果没有，就建一个新的线程加入池中。缓存型池子通常用于执行一些生存期很短的异步型任务。因此在一些面向连接的daemon型SERVER中用得不多。能reuse的线程，必须是timeout IDLE内的池中线程，缺省timeout为60s，超过这个IDLE时长，线程实例将被终止并移出池子。注意：放入CachedThreadPool的线程超过TIMEOUT不活动，其会自动被终止。|
|newFixedThreadPool|	和cacheThreadPool类似，有可用的线程就使用，但不能随时建新的线程。其独特之处：任意时间点，最多只能有固定数目的活动线程存在，此时如果有新的线程要建立，只能放在另外的队列中等待，直到当前的线程中某个线程终止直接被移出池子。cache池和fixed池调用的是同一个底层池，只不过参数不同:fixed池线程数固定，并且是0秒IDLE（无IDLE）。所以FixedThreadPool多数针对一些很稳定很固定的正规并发线程，多用于服务器。cache池线程数支持0-Integer.MAX_VALUE(显然完全没考虑主机的资源承受能力)，60秒IDLE。|
|ScheduledThreadPool|	调度型线程池。这个池子里的线程可以按schedule依次delay执行，或周期执行。|
|SingleThreadExecutor|	单例线程，任意时间池中只能有一个线程。用的是和cache池和fixed池相同的底层池，但线程数目是1-1,0秒IDLE（无IDLE）。|

**Executors创建线程池源码**
```
//调用newCachedThreadPool方法，可以创建一个缓冲型线程池，而在改方法中通过传参创建一个ThreadPoolExecutor，我么你会很奇怪明明返回的是一个ExecutorService，怎么会创建了一个ThreadPoolExecutor呢？
public static ExecutorService newCachedThreadPool() {
        return new ThreadPoolExecutor(0, Integer.MAX_VALUE,60L, 
                   TimeUnit.SECONDS, new SynchronousQueue<Runnable());
}
 
// ThreadPoolExecutor继承了抽象的service类AbstractExecutorService
public class ThreadPoolExecutor extends AbstractExecutorService {}
 
//AbstractExecutorService实现了ExecutorService接口
public abstract class AbstractExecutorService implements ExecutorService {}
 
//所以ExecutorService其实是ThreadPoolExecutor的基类，这也就解释清楚了
```

**ExecutorService**
ExecutorService是一个接口，它继承了Executor，在原有execute方法的基础上新增了submit方法，传入一个任务，该方法能够返回一个Future对象，可以获取异步计算结果。
```
//ExecutorService继承了Executor，并扩展了新方法。
public interface ExecutorService extends Executor { }
 
//Executor中的方法
void execute(Runnable command);
 
//增加了submit方法，该方法传任务来获取Future对象，而Future对象中可以获取任务的执行结果
<T> Future<T> submit(Callable<T> task);
Future<?> submit(Runnable task);
```

**Future(获取异步计算结果)**
Future接口中有下表所示方法，可以获取当前正在执行的任务相关信息

|方法	|说明|
|:---|:---|
|boolean cancel(boolean interruptIf)|	取消任务的执行|
|boolean isCancelled()|	任务是否已取消，任务正常完成前将其取消，返回 true|
|boolean isDone()|	任务是否已完成，任务正常终止、异常或取消，返回true|
|V get()|	等待任务结束，然后获取V类型的结果|
|V get(long timeout, TimeUnit unit)|	获取结果，设置超时时间|

**FutureTask**

Executor框架利用FutureTask来完成异步任务，并可以用来进行任何潜在的耗时的计算。一般FutureTask多用于耗时的计算，主线程可以在完成自己的任务后，再去获取结果。

FutureTask包装了Callable和Runnable接口对象,提供对Future接口的基本实现，开始、取消计算、查询计算是否完成、获取计算结果。仅当计算完成时才能检索结果，当计算没有完成时，该方法会一直阻塞直到任务转入完成状态。一旦完成计算，不能够重新开始或取消计算。通过Excutor(线程池)来执行,也可传递给Thread对象执行。如果在主线程中需要执行比较耗时的操作时，但又不想阻塞主线程时，可以把这些作业交给Future对象在后台完成，当主线程将来需要时，就可以通过Future对象获得后台作业的计算结果或者执行状态。

```
//通过传入任务来构造FutureTask
public FutureTask(Callable<V> callable) {}
public FutureTask(Runnable runnable, V result) {}
 
//FutureTask中同样有获取当前任务状态的方法
public boolean isCancelled(){}
public boolean isDone() {}
public boolean cancel(boolean mayInterruptIfRunning) {}
 
//FutureTask实现RunnableFuture
public class FutureTask<V> implements RunnableFuture<V> {}
 
//RunnableFuture继承Runnable和Future
public interface RunnableFuture<V> extends Runnable, Future<V> 
```

**示例代码**

```
package future.java;
 
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
 
public class TestFuture {
    // 创建线程池
    final static ExecutorService service = Executors.newCachedThreadPool();
 
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        Long t1 = System.currentTimeMillis();
 
        // 任务1
        Future<Boolean> booleanTask = service.submit(new Callable<Boolean>() {
            @Override
            public Boolean call() throws Exception {
                return true;
            }
        });
 
        while (true) {
            if (booleanTask.isDone() && !booleanTask.isCancelled()) {
                //模拟耗时
                Thread.sleep(500);
                Boolean result = booleanTask.get();
                System.err.println("BooleanTask: " + result);
                break;
            }
        }
 
        // 任务2
        Future<String> stringTask = service.submit(new Callable<String>() {
            @Override
            public String call() throws Exception {
                return "Hello World";
            }
        });
 
        while (true) {
            if (stringTask.isDone() && !stringTask.isCancelled()) {
                String result = stringTask.get();
                System.err.println("StringTask: " + result);
                break;
            }
        }
 
 
 
        // 任务3
        Future<Integer> integerTask = service.submit(new Callable<Integer>() {
            @Override
            public Integer call() throws Exception {
                return new Random().nextInt(100);
            }
        });
 
        while (true) {
            if (integerTask.isDone() && !integerTask.isCancelled()) {
                Integer result = integerTask.get();
                System.err.println("IntegerTask: " + result);
                break;
            }
        }
 
        // 执行时间
        System.err.println("time: " + (System.currentTimeMillis() - t1));
    }
 
}
```


### Guava提供的ListenableFuture-Callback

ListenableFuture是可以监听的Future，它是对java原生Future的扩展增强。Future表示一个异步计算任务，当任务完成时可以得到计算结果。如果希望计算完成时马上就拿到结果展示给用户或者做另外的计算，就必须使用另一个线程不断的查询计算状态。这样做会使得代码复杂，且效率低下。如果使用ListenableFuture，Guava会帮助检测Future是否完成了，如果完成就自动调用回调函数，这样可以减少并发程序的复杂度。

**多线程异步处理：常用类**

1. **MoreExecutors**    该类是final类型的工具类，提供了很多静态方法。例如listeningDecorator方法初始化ListeningExecutorService方法，使用此实例submit方法即可初始化ListenableFuture对象。
2. **ListeningExecutorService** 该类是对ExecutorService的扩展，重写ExecutorService类中的submit方法，返回ListenableFuture对象。
3. **ListenableFuture** 该接口扩展了Future接口，增加了addListener方法，该方法在给定的excutor上注册一个监听器，当计算完成时会马上调用该监听器。不能够确保监听器执行的顺序，但可以在计算完成时确保马上被调用。
4. **FutureCallback**    该接口提供了OnSuccess和OnFailuren方法。获取异步计算的结果并回调。
5. **Futures**    该类提供和很多实用的静态方法以供使用。
6. **ListenableFutureTask**    该类扩展了FutureTask类并实现ListenableFuture接口，增加了addListener方法。

**代码示例**

JayGuavaExecutors.java--基于Guava封装的线程池
```
package com.jay.util.tools.base;
 
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
 
import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;
 
/**
 * 基于Guava封装的线程池
 *
 * @author hetiewei
 * @date 2016年8月15日 上午11:16:54
 *
 */
public class JayGuavaExecutors {
	public static final int DEFAULT_MAX_THREAD = 1000;
	private static ListeningExecutorService defaultCompletedExecutorService = null;
	private static final Object lock = new Object();
 
	public static ListeningExecutorService newCachedExecutorService(int maxThreadNumber, final String namePrefix) {
		return MoreExecutors.listeningDecorator(new ThreadPoolExecutor(0, maxThreadNumber, 60L, TimeUnit.SECONDS,
				new SynchronousQueue<Runnable>(), new ThreadFactory() {
 
					private final AtomicInteger poolNumber = new AtomicInteger(1);
 
					@Override
					public Thread newThread(Runnable r) {
						Thread thread = new Thread(r, namePrefix + poolNumber.getAndIncrement());
						return thread;
					}
				}));
 
	}
 
	public static ListeningExecutorService newCachedExecutorService(String namePrefix) {
		return newCachedExecutorService(DEFAULT_MAX_THREAD, namePrefix);
	}
 
	public static ListeningExecutorService getDefaultCompletedExecutorService() {
		if (defaultCompletedExecutorService == null) {
			synchronized (lock) {
				if (defaultCompletedExecutorService == null) {
					defaultCompletedExecutorService = newCachedExecutorService("Completed-Callback-");
				}
			}
		}
		return defaultCompletedExecutorService;
	}
	
}
```

GuavaExecutorsTest.java 测试类
```
package com.jay.util.tools.base.test;
 
import java.util.Random;
import java.util.concurrent.Callable;
 
import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
import com.jay.util.tools.base.JayGuavaExecutors;
 
public class GuavaExecutorsTest {
 
	public static void main(String[] args) {
		Long t1 = System.currentTimeMillis();
 
		// 任务1
		ListenableFuture<Boolean> booleanTask = JayGuavaExecutors.getDefaultCompletedExecutorService()
				.submit(new Callable<Boolean>() {
 
					@Override
					public Boolean call() throws Exception {
						return true;
					}
 
				});
		Futures.addCallback(booleanTask, new FutureCallback<Boolean>() {
 
			@Override
			public void onSuccess(Boolean result) {
				System.out.println("BooleanTask : " + result);
			}
 
			@Override
			public void onFailure(Throwable t) {
				System.out.println("BooleanTask 执行失败 【" + t.getMessage() + "】 ");
			}
		});
 
		// 任务2
		ListenableFuture<String> stringTask = JayGuavaExecutors.getDefaultCompletedExecutorService()
				.submit(new Callable<String>() {
					@Override
					public String call() throws Exception {
						return "Hello World";
					}
				});
 
		Futures.addCallback(stringTask, new FutureCallback<String>() {
			@Override
			public void onSuccess(String result) {
				System.err.println("StringTask: " + result);
			}
 
			@Override
			public void onFailure(Throwable t) {
				System.err.println("StringTask 执行失败 【" + t.getMessage() + "】 ");
			}
		});
 
		// 任务3
		ListenableFuture<Integer> integerTask = JayGuavaExecutors.getDefaultCompletedExecutorService()
				.submit(new Callable<Integer>() {
					@Override
					public Integer call() throws Exception {
						return new Random().nextInt(100);
					}
				});
		Futures.addCallback(integerTask, new FutureCallback<Integer>() {
			@Override
			public void onSuccess(Integer result) {
				try {
					Thread.sleep(500);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				System.err.println("IntegerTask: " + result);
			}
 
			@Override
			public void onFailure(Throwable t) {
				System.err.println("IntegerTask 执行失败 【" + t.getMessage() + "】 ");
			}
		});
 
		Long t2 = System.currentTimeMillis();
		
		 // 执行时间
        System.err.println("time: " + (t2 - t1));
	}
 
	public static void main1(String[] args) {
		for (int i = 0; i < 10; i++) {
			JayGuavaExecutors.getDefaultCompletedExecutorService().submit(new Runnable() {
 
				@Override
				public void run() {
					System.out.println("xxxxx");
					try {
						Thread.sleep(1000);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					System.out.println("xxxxx1");
				}
			});
		}
	}
}

/* result:

BooleanTask : true
StringTask: Hello World
IntegerTask: 67
time: 527
*/
```

## Spring4提供的异步请求封装模板

ListenableFuture通过异步回调机制来实现请求的非阻塞。
通常情况下，客户端获取数据并不会只发送一次http请求，可能会有多个http请求。这样，使用上一篇博客中的方法，就会产生大量的冗余代码，因为请求处理的代码除了一些参数不同外，其它地方都大致相同。我们发现不同请求之间的区别在于：请求地址的不同、响应类型的不同，可能还会有额外请求参数的不同。我们可以将请求数据和响应数据进行封装，这样，只需要一个字段来标识每一次http请求属于哪一个业务就可以实现批量发送http请求，整个过程是异步非阻塞的，一旦获取到数据就会触发回调函数，进而获取到响应数据，最后再进行业务逻辑相关处理

### RestTemplate简介

#### 定义

RestTemplate是Spring3.0中出现的新类，其可以简化HTTP服务器通信，处理HTTP连接，使应用程序代码通过提供url和响应类型(可能的模板变量)便可提取结果

#### 方法

```
//get方法
//其中url为请求地址，responseType为响应类(需要自己依据响应格式来确定)
//urlVariables为数组变量
public <T> T getForObject(String url, Class<T> responseType, Object... urlVariables) throws RestClientException 
 
//urlVariables为Map类型变量，其中key为请求字段名，value为请求字段值
public <T> T getForObject(String url, Class<T> responseType, Map<String, ?> urlVariables)
 
public <T> T getForObject(URI url, Class<T> responseType) throws RestClientException
 
//ResponseEntity
public <T> ResponseEntity<T> getForEntity(String url, Class<T> responseType, Object... urlVariables) throws RestClientException
 
public <T> ResponseEntity<T> getForEntity(String url, Class<T> responseType, Map<String, ?> urlVariables) throws RestClientException
 
public <T> ResponseEntity<T> getForEntity(URI url, Class<T> responseType) throws RestClientException 
 
 
//post
public <T> T postForObject(String url, Object request, Class<T> responseType, Object... uriVariables) throws RestClientException
 
public <T> T postForObject(String url, Object request, Class<T> responseType, Map<String, ?> uriVariables) throws RestClientException
 
public <T> T postForObject(URI url, Object request, Class<T> responseType) throws RestClientException 
 
public <T> ResponseEntity<T> postForEntity(String url, Object request, Class<T> responseType, Object... uriVariables) throws RestClientException
 
public <T> ResponseEntity<T> postForEntity(String url, Object request, Class<T> responseType, Map<String, ?> uriVariables) throws RestClientException
 
public <T> ResponseEntity<T> postForEntity(URI url, Object request, Class<T> responseType) throws RestClientException
```

#### 说明

Spring提供的RestTemplate可用于访问Rest服务的客户端，其提供了多种便捷访问远程Http服务的方法，能够大大提高客户端的编写效率，但其并没有实现异步调用的功能。下面将引入Spring4.0提供的AsyncRestTemplate，该类可实现异步非阻塞处理http请求


### AsyncRestTemplate简介

#### 定义
AsyncRestTemplate是在Spring4.0中对RestTemplate进行扩展产生的新类，其为客户端提供了异步http请求处理的一种机制，通过返回ListenableFuture对象生成回调机制，以达到异步非阻塞发送http请求

#### 方法
```
//get
public <T> ListenableFuture<ResponseEntity<T>> getForEntity(String url, Class<T> responseType, Object... uriVariables) throws RestClientException
 
public <T> ListenableFuture<ResponseEntity<T>> getForEntity(String url, Class<T> responseType, Map<String, ?> urlVariables) throws RestClientException
 
public <T> ListenableFuture<ResponseEntity<T>> getForEntity(URI url, Class<T> responseType) throws RestClientException
 
 
//post
public <T> ListenableFuture<ResponseEntity<T>> postForEntity(String url, HttpEntity<?> request, Class<T> responseType, Object... uriVariables) throws RestClientException
 
public <T> ListenableFuture<ResponseEntity<T>> postForEntity(String url, HttpEntity<?> request, Class<T> responseType, Map<String, ?> uriVariables) throws RestClientException 
 
public <T> ListenableFuture<ResponseEntity<T>> postForEntity(URI url, HttpEntity<?> request, Class<T> responseType) throws RestClientException 
```

#### 说明

相比于RestTemplate，AsyncRestTemplate通过回调机制能够很好地异步处理多个http请求，使得客户端在主方法中不必等待服务器响应，而是继续执行后续代码，这样就较大地提高了代码的执行效率，减少响应时间。


### 基于AsyncRestTemplate实现批量异步调用

下面将介绍基于AsyncRestTemplate异步调用的轻量级框架，说框架有点吹牛皮的感觉，不过代码结构整体上看起来还是挺清晰的，如有不妥之处，请提供宝贵建议。其主要分为5个部分：业务标识、请求、响应，异步调用、请求处理。对应的类如下所示：

- 业务标识：IEnum、UserEnum(具体业务标识)
- 请求：BaseRequest、UserRequest(具体业务请求)、ConcreateWapper(请求包装)
- 响应：BaseResponse、UserRequest（具体业务响应）
- 异步调用：Templete、AbstractTemplete、AsynClientTemplete、CommonListenableCallBack
- 请求处理：FutureTpDao

先来个直观的例子：
```
public static void main(String[] args) {  
    AsyncRestTemplate template = new AsyncRestTemplate();  
    //调用完后立即返回（没有阻塞）  
    ListenableFuture<ResponseEntity<User>> future = template.getForEntity("http://localhost:9080/spring4/api", User.class);  
    //设置异步回调  
    future.addCallback(new ListenableFutureCallback<ResponseEntity<User>>() {  
        @Override  
        public void onSuccess(ResponseEntity<User> result) {  
            System.out.println("======client get result : " + result.getBody());  
        }  
  
        @Override  
        public void onFailure(Throwable t) {  
            System.out.println("======client failure : " + t);  
        }  
    });  
    System.out.println("==no wait");  
} 
```

#### 业务标识（使用枚举类来标识业务请求）

使用枚举类能够比较好地标识具体业务，但是枚举类无法继承，这里通过定义一个空的接口IEnum对其进行抽象。可能看起来会有所不妥，但是也算是一种解决方法吧。

```
//空的接口
package acync;
 
public interface IEnum {
}
 
//具体业务标识枚举类，实现了IEnum接口
public enum UserEnum implements IEnum {
    ADD,
    UPDATE,
    DELETE,
    MODIFY;
}
```

#### 请求

通常情况下，客户端都是发送http请求（使用url的方式）来获取数据，这样，我们主需要获取请求的url地址即可。这里，定义接口BaseRequest提供build方法来构建请求接口，对于具体的业务请求只需实现接口并构建请求url即可

```
//基础请求接口，提供构建URL方法
package acync;
 
public interface BaseRequest {
    public String build();
}
 
 
//具体的请求类，依据业务情况自行构建URL地址
package acync;
 
public class UserRequest implements BaseRequest {
    private static final String REQ_URL = "http://www.126.com";
 
    @Override
    public String build() {
        return REQ_URL;
    }
}
```

#### 响应

对于请求响应这里也是定义抽象类BaseResponse，提供status来表示请求的响应状态，而具体的业务响应只需要实现抽象类，自定义实现即可。（其中，BaseResponse抽象类可依据具体的业务框架来定义实现）

```
//基础响应抽象类，提供状态码
package acync;
 
import java.io.Serializable;
 
public abstract class  BaseResponse implements Serializable{
    private String status;
}
 
 
//具体业务响应类
package acync;
 
public class UserResponse extends BaseResponse{
//TODO
}
```

#### 异步调用

下面的所列代码是整个请求的核心代码。首先，定义模版接口，接口中只提供了若干主要方法，从整体上看，方法的参数为业务请求类和响应类型，返回值为泛型类型的ListenableFuture对象；其次，定义抽象类和具体的实现类；最后，进过请求处理即可获取请求接口。这里不累赘，见下方代码

```
//异步调用模板接口
package acync;
 
import java.util.Map;
 
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.ResponseEntity;
import org.springframework.util.concurrent.ListenableFuture;
 
public interface Templete {
    <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest, Class<T> responseType) throws Exception;
 
    <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest,
            ParameterizedTypeReference<T> responseType) throws Exception;
 
    <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest, Class<T> responseType,
            Map<String, ?> uriVariables) throws Exception;
 
    <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest,
            ParameterizedTypeReference<T> responseType, Map<String, ?> uriVariables) throws Exception;
}
 
 

 
 
//异步调用抽象类
//这里仅仅提供少量的调取方法，可以自行扩展
 
package acync;
 
import java.util.Map;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.web.client.AsyncRestTemplate;
 
public abstract class AbstractTemplete implements Templete{
    public AsyncRestTemplate asyncRestTemplate;
 
    @Override
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest, Class<T> responseType)
            throws Exception {
        String url = baserequest.build();
        try {
            ListenableFuture<ResponseEntity<T>> t = asyncRestTemplate.getForEntity(url, responseType);
            return t;
        } catch (Exception e) {
            throw e;
        }
    }
 
    @Override
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest,
            ParameterizedTypeReference<T> responseType) throws Exception {
        String url = baserequest.build();
        try {
            ListenableFuture<ResponseEntity<T>> t = asyncRestTemplate.exchange(url, HttpMethod.GET, null, responseType);
            return t;
        } catch (Exception e) {
            throw e;
        }
    }
 
    @Override
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest, Class<T> responseType,
            Map<String, ?> uriVariables) throws Exception {
        String url = baserequest.build();
        ListenableFuture<ResponseEntity<T>> t = null;
        try {
            t = asyncRestTemplate.exchange(url, HttpMethod.GET, null, responseType, uriVariables);
            return t;
        } catch (Exception e) {
            throw e;
        }
    }
 
    @Override
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest,
            ParameterizedTypeReference<T> responseType, Map<String, ?> uriVariables) throws Exception {
        String url = baserequest.build();
        ListenableFuture<ResponseEntity<T>> t = null;
        try {
            t = asyncRestTemplate.exchange(url, HttpMethod.GET, null, responseType, uriVariables);
            return t;
        } catch (Exception e) {
            throw e;
        }
    }
 
    abstract void setTemplete(AsyncRestTemplate asyncRestTemplate);
 
}
 
 
 

 
 
// 具体的异步调用实现类
package acync;
 
import java.util.Map;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.ResponseEntity;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.web.client.AsyncRestTemplate;
 
public class AsynClientTemplete extends AbstractTemplete {
 
    public AsynClientTemplete(AsyncRestTemplate template) {
        setTemplete(template);
    }
 
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest, Class<T> responseType)
            throws Exception {
        return super.getAsyncForObject(baserequest, responseType);
    }
 
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest,
            ParameterizedTypeReference<T> responseType) throws Exception {
        return super.getAsyncForObject(baserequest, responseType);
    }
 
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest, Class<T> responseType,
            Map<String, ?> uriVariables) throws Exception {
        return super.getAsyncForObject(baserequest, responseType, uriVariables);
    }
 
    public <T> ListenableFuture<ResponseEntity<T>> getAsyncForObject(BaseRequest baserequest,
            ParameterizedTypeReference<T> responseType, Map<String, ?> uriVariables) throws Exception {
        return super.getAsyncForObject(baserequest, responseType, uriVariables);
    }
 
    @Override
    void setTemplete(AsyncRestTemplate template) {
        asyncRestTemplate = template == null ? new AsyncRestTemplate() : template;
    }
 
}
```

#### 请求处理

上述四步都是为这一步做准备。请求处理这一步是请求的入口，在FutureTpDao中，通过getHttpData方法传入请求包装类ConcreateWapper，返回的Map对象MapIEnum, Object即为响应结果，只需依据具体的业务枚举类即可获取对应的业务请求数据

```
//包装了具体的请求信息
//其中的每一个Concreate对应一个具体的请求，baseEnum对应业务标识，variables为请求的额外参数，request为请求类和响应类组成的map
 
package acync;
 
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
 
public class ConcreateWapper {
    private List<Concreate> wrapper = new ArrayList<Concreate>();
 
    public ConcreateWapper(){}
 
    public void setParams(IEnum baseEnum, Map<String, ?> variables, Map<BaseRequest, ?> request) {
        wrapper.add(new Concreate(baseEnum, variables, request));
    }
 
    public List<Concreate> getWrapper() {
        return wrapper;
    }
 
    public static class Concreate {
        private IEnum baseEnum;
        private Map<String, ?> variables;
        private Map<BaseRequest, ?> request;
 
        public Concreate(IEnum baseEnum, Map<String, ?> variables, Map<BaseRequest, ?> request) {
            this.baseEnum = baseEnum;
            this.variables = variables;
            this.request = request;
        }
 
        public IEnum getBaseEnum() {
            return baseEnum;
        }
 
        public void setBaseEnum(IEnum baseEnum) {
            this.baseEnum = baseEnum;
        }
 
        public Map<String, ?> getVariables() {
            return variables;
        }
 
        public void setVariables(Map<String, ?> variables) {
            this.variables = variables;
        }
 
        public Map<BaseRequest, ?> getRequest() {
            return request;
        }
 
        public void setRequest(Map<BaseRequest, ?> request) {
            this.request = request;
        }
    }
}
 
 
 
 
 
 
 
//实现ListenableFutureCallback，实现回调功能
package acync;
 
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import org.springframework.http.ResponseEntity;
import org.springframework.util.concurrent.ListenableFutureCallback;
 
 
public class CommonListenableCallBack<T> implements ListenableFutureCallback<T> {
    private IEnum type;
    private Map<IEnum, Object> resultValue;
    private volatile CountDownLatch latch;
 
    public CommonListenableCallBack(IEnum type, Map<IEnum, Object> resultValue, CountDownLatch latch) {
        this.type = type;
        this.resultValue = resultValue;
        this.latch = latch;
    }
 
    @Override
    public void onSuccess(T result) {
        ResponseEntity<T> re = (ResponseEntity<T>) result;
        if (re != null && re.getBody() != null) {
            T body = re.getBody();
            if (type != null) {
                resultValue.put(type, body);
            }
        }
        latch.countDown();
    }
 
    @Override
    public void onFailure(Throwable ex) {
        latch.countDown();
    }
 
}
 
 
 
 
//FutureTpDao的构造函数可以传入自定义的AsyncRestTemplate，不传的话就是默认的
//其中的getHttpData()方法传入多个请求的包装类ConcreateWapper，返回数据组成的Map
//其中Map中的key对应的是业务标识，value对应的是请求对应的结果类
 
package acync;
 
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.web.client.AsyncRestTemplate;
import acync.ConcreateWapper.Concreate;
 
public class FutureTpDao {
    public AsynClientTemplete asynHttpClient;
 
    public FutureTpDao(){
        asynHttpClient = new AsynClientTemplete(null);
    }
 
    public FutureTpDao(AsyncRestTemplate tp) {
        asynHttpClient = new AsynClientTemplete(tp);
    }
 
    //获取数据
    public Map<IEnum, Object> getHttpData(ConcreateWapper wapper) {
        if (wapper == null)
            return new HashMap<IEnum, Object>();
        final CountDownLatch latch = new CountDownLatch(wapper.getWrapper().size());
        final Map<IEnum, Object> result = new HashMap<IEnum, Object>();
 
        if (wapper.getWrapper() != null) {
            for (final Concreate wp : wapper.getWrapper()) {
                try {
                    Map<BaseRequest, ?> requestMap = wp.getRequest();
                    for (final BaseRequest tpRequestInfo : requestMap.keySet()) {
                        getHttpdata(wp, tpRequestInfo, latch, requestMap, result);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
 
            try {
                latch.await();
            } catch (Exception e) {
                throw new RuntimeException(e.getMessage());
            }
        }
        return result;
    }
 
   //发送http请求，获取请求结果
    private void getHttpdata(Concreate wp, BaseRequest tpRequestInfo, CountDownLatch latch,
            Map<BaseRequest, ?> requestMap, Map<IEnum, Object> result) throws Exception {
        ListenableFuture<?> statResponse = null;
 
        if (requestMap.get(tpRequestInfo) instanceof ParameterizedTypeReference<?>) {
            ParameterizedTypeReference<?> responseType = (ParameterizedTypeReference<?>) requestMap.get(tpRequestInfo);
            statResponse = asynHttpClient.getAsyncForObject(tpRequestInfo, responseType, wp.getVariables());
        } else if (requestMap.get(tpRequestInfo) instanceof Class<?>) {
            Class<?> responseType = (Class<?>) requestMap.get(tpRequestInfo);
            statResponse = asynHttpClient.getAsyncForObject(tpRequestInfo, responseType);
        } else {
            throw new RuntimeException("requestType error...");
        }
 
        addCallBack(statResponse, wp.getBaseEnum(), latch, result);
    }
 
    //增加回调
    private <T> void addCallBack(ListenableFuture<T> statResponse, IEnum baseEnum, CountDownLatch latch,
            Map<IEnum, Object> result) {
        if (statResponse != null) {
            statResponse.addCallback(new CommonListenableCallBack<T>(baseEnum, result, latch));
        }
    }
}
```

#### 示例

```
package acync;
 
import java.util.HashMap;
import java.util.Map;
 
/**
 * 示例
 * 示例仅仅是一个样板，无法运行
 * 需要在web环境下运行，例如启动tomcat服务器并进行相关配置
 * @author liqqc
 *
 */
public class Demo {
 
    public static void main(String[] args) {
        ConcreateWapper wapper = new ConcreateWapper();
 
        Map<BaseRequest, Class<? extends BaseResponse>> request = new HashMap<BaseRequest, Class<? extends BaseResponse>>();
        request.put(new UserRequest(), new UserResponse().getClass());
        wapper.setParams(UserEnum.ADD, null, request);
        wapper.setParams(UserEnum.DELETE, null, request);
        wapper.setParams(UserEnum.UPDATE, null, request);
        wapper.setParams(UserEnum.MODIFY, null, request);
 
        FutureTpDao futureTpDao = new FutureTpDao();
        Map<IEnum, Object> futureData = futureTpDao.getHttpData(wapper);
        for (IEnum ienum : futureData.keySet()) {
            System.err.println(ienum + "=" + futureData.get(ienum));
        }
    }
}
```

ref:
https://blog.csdn.net/he90227/article/details/52210490
