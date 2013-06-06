#配置数据库

* 新建数据库 course

		create database course

* 新建用户 csadmin

		grant all privileges on course.* to 'csadmin'@'localhost'
		    identified by 'csadminpass' with grant option;
		grant all privileges on course.* to 'csadmin'@'%'
		    identified by 'csadminpass' with grant option;


		