# tornado-piston
A mini-framework for Tornado for creating RESTful APIs


##### 目标

-简单易用的RestFul框架，不适合复杂的业务逻辑，通过API支持良好的CRUD风格
-用户侧重关心module这一层，框架来完成数据到数据api的跨越
-使用适配器来接驳不同的后端
-自动生成url path route
-内置部分库的异步支持


##### 方案


Resource 定义handler
Adaptor 定义Object Module
