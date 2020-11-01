# 公共数据爬取

## 1.行政区划数据爬取

#### 1.1 数据来源国家统计局网站
```
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html
```

#### 1.2 数据存储MySQL
```
数据结构:
CREATE TABLE `t_area` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(12) DEFAULT NULL COMMENT '区划代码',
  `name` varchar(50) DEFAULT NULL COMMENT '名称',
  `p_code` varchar(12) DEFAULT NULL COMMENT '区划代码(父级)',
  `level` varchar(10) DEFAULT NULL COMMENT '层级',
  `order` varchar(10) DEFAULT NULL COMMENT '排序',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=702064 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='行政区划(http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html)';
```
```
截至2020年数据统计:
#省份 31
select count(1) from t_area where level='1'
#市 342
select count(1) from t_area where level='2'
#区县 3272
select count(1) from t_area where level='3'
#乡镇 43010
select count(1) from t_area where level='4'
##村镇 655408
select count(1) from t_area where level='5'
```

#### 1.3 scrapy优化配置
```
CONCURRENT_REQUESTS = 100 //最大请求并发
DOWNLOAD_DELAY = 0.5 //请求间隔,该数乘以0.5~1.5的系数,单位秒
LOG_LEVEL = "INFO" //日志级别
```