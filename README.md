# Question Answering for Recruitment Based on Knowledge Graph
## 任务计划
### 一. 职位关键词
#### 互联网行业
- 算法类:  机器学习, 数据挖掘, 知识图谱, 推荐系统, 深度学习, 算法工程师
- 开发类:  前端, 后端, Java, Python
- 产品:  产品经理, 数字产品经理
#### 金融行业
#### 医学行业
### 二. 所爬取网站
1. 智联招聘
2. 前程无忧
3. 拉勾网
4. boss直聘
5. ~~猎聘网~~
6. 实习僧
7. ~~大街网~~
8. ~~应届生求职~~
9. ~~牛客网~~

### 三. 知识图谱构建模块
- step1: 职位->技能, 工作描述, 公司, 属性(工作地点, 工作经验, 工资)
- step2: 公司->公司评价标签, 属性(类型, 人数, 官网, 描述, 注册资本, 地址, 工资)
- step3: 技能节点进行NER, 提取关键词
- step4: 技能->百度百科信息, 推荐资料节点(视频, 书籍, 网站)
- step5: 工作描述进行断句以及主谓分析
 
    
