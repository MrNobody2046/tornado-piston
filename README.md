# tornado-piston
A mini-framework for Tornado for creating RESTful APIs


##### 目标

- 简单易用的RestFul框架，可定制，通过API支持良好的CRUD风格
- 用户侧重关心module这一层，框架来完成数据到数据api的跨越
- 使用适配器来接驳不同的数据库，ORM框架
- 自动生成url path route
- 内置部分库的异步支持


##### 方案，实现


- Resource 定义handler
- Adaptor 数据段的适配器
- Request/Response 对请求/返回的包装，不同于tornado内置的Requst
- Codes 标准错误码
- Utils 工具
