# 总结

## 摘要
...
2022-2024 是LLM 时代
2025-?是智能体agent 时代
???

## 核心
* 1.system_promt
系统引导(理论)：专家系统：基础理论支撑
提供总体把控，尽量使用专业知识(够强，够专业，够全面)和丰富的实战经验，结合强大的逻辑表述语言，引导大模型进行思考推理。
而且尽量避免产生幻觉等等。

* 2.tool-action
工具(工程)：程序员、工人：具体落实
提供具体的操作，在程序员工作软件就是编码、硬件就是操作设备(机器人难不成是具身智能)、还有其他业务场景吗？？？上课教学？
像工具有：tts，ocr、asr等等，这些小模型其实可以大模型结合起来用！！！

* 3.aim、obseration、finish
目标：总体目标与阶段目标

* 4.step
步骤：智能体的抽象步骤；
有多种方式，react，plan-action......


* 5.llm_output解析
thought
action

action-result ->context-user_promt
observation

thought
observation
action


迭代循环，知道llm知道finish 或者超过限制的maxStep阈值


* 6.llm选型
    token？
    上下文限制？


***

# 实战
for example：you neet build one agent for trip at a city base on the weather；

## first: system_promt

> 专业知识 + promt输出结构


代码：

```
你是一个智能旅行助手，根据用户输入的城市和天气情况，为用户提供定制化的旅行建议。



```
上面这段提示词，是一个专业的知识，也是一个promt输出结构。
它定义了智能体的行为，包括它的专业知识和它的输出格式。
如果没有提示词结构，llm会输出随机的文字，而不是按照我们的期望。
>抽象
1.智能体摘要，类似于注释，就是智能体是什么，需要做什么，有什么工具，具体怎么做；  有点像传统编程里的注释

2.可用工具介绍  ；有点像传统编程里的依赖库、封装对象类、脚本工具类
结构：
- '方法体': 注释

3.行动格式输出 llm_output() ;有点像传统编程里的if-else 、while、for实现的具体业务逻辑。
结构：
智能体的回答必须严格遵循以下格式。
首先，是你的思考过程
然后，是你要执行的具体行动
每次回复只输出一对Thought-Action：
Thought: [这里是你的思考过程和下一步计划]
Action: [这里是你要调用的工具，格式为 function_name(arg_name="arg_value")]

4. 任务完成 finish 调出点；有点像传统编程里的输出、展示、打印等
当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后面使用`finish(answer="")`来输出最终答案

请开始吧！

```
${你是什么，你的任务是干什么，可以利用工具来一步一步解决问题(you are a ...,your job is to do ...,you can use tools to solve problem step by step)}

# avaliabel_tool 可用工具
'方法体 函数名(函数参数)' : 方法注释

# action_format 行动格式
你的回答必须严格遵循以下格式，首先是你的思考过程，然后是你要执行的具体行动。

```


## second：tool
getWeather(city) -> result

getTripResult(city,weather)

> 经验及工具的使用知识


代码：
```
```


## third： 数据解构

针对tool返回结果进行数据解析，获取有用信息放入user_promt中。
比如getWeather中需要获取到天气变量。
getTripResult中需要获取到返回的搜索结果。然后进行解析。放入user_promt中。

> json+regex

代码：
```
```


## fourth: llm


## fifth: 步骤 + user_promt
针对system_promt中定义的返回数据结构。
需要进行自定义的逻辑代码限制。将

比如：对于llm的返回，需要按照自己的逻辑规则，对结果进行解析，很关键。第4步中的步骤，thought、action、observation等等key的。


# 疑问
> 1.LLM是如何可以调用本地的工具tool的
llm不是输出文字吗，本地tool getWeather是本地的一个脚本scrpt？