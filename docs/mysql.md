数据库变更记录
=============
巡考人员分类库
DROP TABLE IF EXISTS `xunkao_cat`;

CREATE TABLE `xunkao_cat` (
  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '类别名称',
  `weight` TINYINT(4) NOT NULL DEFAULT '1' COMMENT '权重',
  `status` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='巡考分类';

3、巡考人员库people

DROP TABLE IF EXISTS `people`;
CREATE TABLE `people` (
  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `cat_id` INT(11) NOT NULL DEFAULT '0' COMMENT '默认岗位分类id',
  `name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '姓名',
  `sfzh` INT(18) NOT NULL DEFAULT '0' COMMENT '身份证号',
  `sex` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '性别 1：男 2：女',
  `nickname` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '昵称',
  `xunkao_id` CHAR(100) NOT NULL DEFAULT '' COMMENT '编号',
  `weight` CHAR(4) NOT NULL DEFAULT 'C' COMMENT '权重 A：优 B：良 C：合格 D：警告 E：黑名单',
  `status` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `danwei` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '单位',
  `bumen` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '部 门',
  `chepai` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '车牌号',
  `mobile` VARCHAR(11) NOT NULL DEFAULT '' COMMENT '手机号码',
  `avatar` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '会员头像',
  `address` VARCHAR(150) NOT NULL DEFAULT '' COMMENT '家庭地址',
  `bankcard` INT(19) NOT NULL DEFAULT '0' COMMENT '银行卡号',
  `salt` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '随机salt',
  `reg_ip` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '注册ip',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
  PRIMARY KEY (`id`)
) ENGINE=INNODB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='巡考人员表'

1、数据字典表

DROP TABLE IF EXISTS `dic_desc`;

CREATE TABLE `dic_desc` (
  `dic_id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `dic_name` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '字典名称',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
  PRIMARY KEY (`dic_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='数据字典表';


2、数据字典状态表dic_status

CREATE TABLE `dic_status` (
  `status_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `dic_id` int(11) unsigned NOT NULL,
  `status_name` varchar(200) NOT NULL,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`status_id`),
  KEY `dic_id` (`dic_id`),
  CONSTRAINT `dic_id` FOREIGN KEY (`dic_id`) REFERENCES `dic_desc` (`dic_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据字典状态表';

4、考试列表exam_list

DROP TABLE IF EXISTS `exam_list`;

CREATE TABLE `exam_list` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `exam_name` varchar(200) NOT NULL DEFAULT '' COMMENT '考试名称',
  `exam_code` varchar(50) NOT NULL DEFAULT '' COMMENT '考试代码',
  `abbreviation` varchar(50) NOT NULL DEFAULT '' COMMENT '考试简称',
  `exam_date` varchar(50) NOT NULL DEFAULT '' COMMENT '考试年月',
  `summary` varchar(300) NOT NULL DEFAULT '' COMMENT '描述',
  `exam_status` int(11) unsigned NOT NULL COMMENT '状态 归档  启用  关闭',
  `exam_cat` int(11) unsigned NOT NULL COMMENT '考试类别 1：专业技术 2：执业资格 3：公务员事业单位 4：社会化 5：其他 ',
  `keshu` int(11) unsigned NOT NULL DEFAULT '1' COMMENT '科数',
  `days` float unsigned NOT NULL DEFAULT '1' COMMENT '天数',
  `canbu` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '餐补次数',
  `kaodian` varchar(200) NOT NULL DEFAULT '' COMMENT '考点',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `exam_status` (`exam_status`),
  KEY `exam_cat` (`exam_cat`),
  CONSTRAINT `exam_cat` FOREIGN KEY (`exam_cat`) REFERENCES `dic_status` (`status_id`) ON UPDATE CASCADE,
  CONSTRAINT `exam_status` FOREIGN KEY (`exam_status`) REFERENCES `dic_status` (`status_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='考试列表'


5、考试科目表exam_kemu

DROP TABLE IF EXISTS `exam_kemu`;

CREATE TABLE `exam_kemu` (
  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `exam_id` INT(11) UNSIGNED NOT NULL  COMMENT '考试id',
  `exam_name` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '考试名称',
  `changci` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '场次名称',
  `kemu_name` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '科目名称',
  `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
  `last_time` INT(11)  UNSIGNED NOT NULL COMMENT '科目时长',
  `kaochang` INT(11) NOT NULL DEFAULT '0' COMMENT '考场数量',
  `status` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `beizhu1` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '备注1',
  `beizhu2` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '备注2',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
  PRIMARY KEY (`id`),
  CONSTRAINT `exam_id2` FOREIGN KEY (`exam_id`) REFERENCES `exam_list` (`id`) ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='考试科目表';



6、考点库kaodian

DROP TABLE IF EXISTS `kaodian`;

CREATE TABLE `kaodian` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL DEFAULT '' COMMENT '考点名称',
  `address` varchar(200) NOT NULL DEFAULT '' COMMENT '考点地址',
  `kaochang` int(11) NOT NULL DEFAULT '0' COMMENT '考场数量',
  `linkman` varchar(50) NOT NULL DEFAULT '' COMMENT '联系人',
  `tel` varchar(50) NOT NULL DEFAULT '' COMMENT '联系电话',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考点库表';


7、考务安排表exam_kaowu

DROP TABLE IF EXISTS `exam_kaowu`;
CREATE TABLE `exam_kaowu` (
  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `exam_id` INT(11) UNSIGNED NOT NULL COMMENT '考试id',
  `name_id` INT(11) UNSIGNED NOT NULL COMMENT '姓名id',
  `job_id` INT(11) UNSIGNED NOT NULL COMMENT '岗位id',
  `job` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '工作岗位',
  `workplace` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '工作层级：考区、考点、考场、其他',
  `kaodian` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '工作考点',
  `kaochang` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '工作考场',
  `workdays` FLOAT UNSIGNED NOT NULL COMMENT '工作天数',
  `canbu` INT(11) UNSIGNED NOT NULL COMMENT '餐补天数',
  `beizhu1` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注一',
  `beizhu2` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注二',
  `beizhu3` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '备注三',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
  PRIMARY KEY (`id`),
  KEY `exam_id` (`exam_id`),
  KEY `name_id` (`name_id`),
  KEY `job_id` (`job_id`),
  CONSTRAINT `exam_id` FOREIGN KEY (`exam_id`) REFERENCES `exam_list` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `name_id` FOREIGN KEY (`name_id`) REFERENCES `people` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `job_id` FOREIGN KEY (`job_id`) REFERENCES `people_cat` (`id`) ON UPDATE CASCADE
) ENGINE=INNODB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COMMENT='考务安排表'



8、考点安排表exam_kaodian

DROP TABLE IF EXISTS `exam_kaodian`;

CREATE TABLE `exam_kaodian` (
  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `exam_id` INT(11) UNSIGNED NOT NULL  COMMENT '考试id',
  `exam_name` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '考试名称',
  `kaodian_id` INT(11) UNSIGNED NOT NULL  COMMENT '考点id',
  `kaodian_name` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '考点名称',
  `kaodian_address` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '考点地址',
  `kaochang` INT(11) NOT NULL DEFAULT '0' COMMENT '考场数量',
  `kaochang_stnum` INT(11) NOT NULL DEFAULT '1' COMMENT '起始考场号',
  `kemu` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '考试科目',
  `xunkao_num` INT(11) NOT NULL DEFAULT '0' COMMENT '巡考人员数量',
  `menjian_num` INT(11) NOT NULL DEFAULT '0' COMMENT '门检人员数量',
  `beizhu1` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '备注1',
  `beizhu2` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '备注2',
  `beizhu3` VARCHAR(200) NOT NULL DEFAULT ''  COMMENT '备注3',
  `updated_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后插入时间',
  PRIMARY KEY (`id`),
  CONSTRAINT `exam_id3` FOREIGN KEY (`exam_id`) REFERENCES `exam_list` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `kaodian_id` FOREIGN KEY (`kaodian_id`) REFERENCES `kaodian` (`id`) ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='考点安排表';
