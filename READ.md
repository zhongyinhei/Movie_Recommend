# Movie_Recommend system

## 爬虫

**开发环境**： pycharm + python3.6

**软件架构**： mysql + scrapy


## 电影网站搭建

**开发环境**： IntelliJ IDEA + maven + git + linux + powerdesigner

**软件架构**： mysql  + spring + springmvc + mybatis

## 后台管理系统

**开发环境**： IntelliJ IDEA + maven + git + linux + powerdesigner

**软件架构**： mysql + mybatis + spring + springmvc + easyui

## 推荐系统（Spark）

**开发环境**： IntelliJ IDEA + maven + git + linux

**软件架构**： hadoop + zookeeper + flume + kafka + nginx + spark + hive + mysql


## 具体步骤：

**1.服务器规划（linux镜像为centos6）：**

    spark1（ip 192.168.13.134），分配8G内存，4核
    spark2（ip 192.168.13.135），分配6G内存，4核
    spark3（ip 192.168.13.136），分配6G内存，4核

**2.电影数据集，**地址： 本次下载的为1m大小的数据集

**3.环境的搭建：**

1）hdfs搭建

    spark1上搭建namenode,secondary namenode,datanode
    spark2上搭建datanode
    spark3上搭建datanode

2）yarn搭建

    spark1上搭建resourcemanager,nodemanager
    spark2上搭建nodemanager
    spark3上搭建nodemanager

3）mysql搭建,在spark2上搭建

4）hive搭建,在spark1上搭建

5）spark集群搭建，搭建standalone模式，spark1为master，其他为worker

**4.数据的清洗：** （上传数据至hdfs中，hdfs操作）

1）启动 hdfs： [root@spark1 ~]# start-dfs.sh

2）启动 yarn： [root@spark1 ~]# start-yarn.sh

3）启动 mysql： [root@spark2 ~]# service mysqld start

4）启动 hive： [root@spark1 ~]# hive –service metastore

5）启动 spark集群： [root@spark1 spark-1.6.1]# ./sbin/start-all.sh

6）代码(com.zxl.datacleaner.ETL)打包上传（spark-sql与hive集成）

    代码位于 package com.zxl.datacleaner.ETL，打包为 ETL.jar
    运行代码 spark-submit –class com.zxl.datacleaner.ETL –total-executor-cores 2 –executor-memory 2g lib/ETL.jar
    成功于hive中建表

**5.数据的加工，** 根据ALS算法对数据建立模型(ALS论文)

1）启动 hdfs： [root@spark1 ~]# start-dfs.sh

2）启动 yarn： [root@spark1 ~]# start-yarn.sh

3）启动 mysql： [root@spark2 ~]# service mysqld start

4）启动 hive： [root@spark1 ~]# hive –service metastore

5）启动 spark集群： [root@spark1 spark-1.6.1]# ./sbin/start-all.sh

6）代码(com.zxl.datacleaner.RatingData)打包上传，测试建立模型

**6.建立模型，** 根据RMSE(均方根误差)选取较好的模型

1）启动上述的服务

2）代码(com.zxl.ml.ModelTraining)打包上传，建立模型

注：com.zxl.ml.ModelTraining2中代码训练单个模型，其中参数 rank=50, iteration = 10, lambda = 0.01

    

- 代码位于 package com.zxl.ml.ModelTraining，打包为 Spark_Movie.jar
    

- 运行代码 spark-submit –class com.zxl.ml.ModelTraining lib/Spark_Movie.jar

**7.产生推荐结果**

1）启动上述的服务

2）代码(com.zxl.ml.Recommender)打包上传，产生推荐结果

**8.数据入库，** 存储为所有用户推荐的电影结果，mysql中存入的格式为(userid, movieid,rating)

1）启动上述的服务

2）代码(com.zxl.ml.RecommendForAllUsers)打包上传，数据入库

    

- 运行代码 spark-submit –class com.zxl.ml.RecommendForAllUsers –jars lib/mysql-connector-java-5.1.35-bin.jar lib/Spark_Movie.jar

**9.实时数据的发送**

1）安装nginx，用来接收电影网站上用户的点击信息，写入本地文件

2）安装flume，实时监控本地文件，将数据发送至kafka消息队列中

**10.实时数据的接收处理，**如果打包到服务器运行错误，也可在本地IDEA上运行

1）安装zookeeper

2）安装kafka，用来接收发送数据

3）启动上述的服务

4）启动zookeeper： [root@spark1 soft]# zkServer.sh start

4）启动flume：[root@spark1 flume]# bin/flume-ng agent -c ./conf/ -f conf/flume-conf.properties -Dflume.root.logger=DEBUG,console -n a1

5）启动kafka： [root@spark1 kafka_2.11-0.10.1.0]# bin/kafka-server-start.sh config/server.properties

6）代码(com.zxl.datacleaner.PopularMovies2)运行，用于为没有登录或新用户推荐，默认推荐观看最多的5部电影

7）代码运行(需指定jar包 kafka-clients-0.10.1.0.jar)


- spark-submit –class com.zxl.streaming.SparkDrStreamALS –total-executor-cores 2 –executor-memory 1g –jars lib/kafka-clients-0.10.1.0.jar lib/Spark_Movie.jar
