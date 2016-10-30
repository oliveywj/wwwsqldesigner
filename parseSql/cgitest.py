#!/usr/bin/env python

import cgi
import cgitb    #show error on webbrowser when error occurs
import random

import sys
sys.path.insert(0,'./sqlparse-0.2.2-py2.7.egg')
import sqlparse


cgitb.enable()

sql = """
-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'indi'
-- 2323
-- ---

DROP TABLE IF EXISTS `indi`;
		
CREATE TABLE `indi` (
  `indi_cd` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `code` INTEGER NULL DEFAULT NULL,
  `friend` INTEGER NULL DEFAULT NULL,
  `asdf` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`indi_cd`)
) COMMENT '2323';

-- ---
-- Table 'guys'
-- 
-- ---

DROP TABLE IF EXISTS `guys`;
		
CREATE TABLE `guys` (
  `guy_cd` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `guy_name` INTEGER NULL DEFAULT NULL,
  `gf_cd` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`guy_cd`)
);

-- ---
-- Table 'girls'
-- 
-- ---

DROP TABLE IF EXISTS `girls`;
		
CREATE TABLE `girls` (
  `girls_cd` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `girls_name` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`girls_cd`)
);

-- ---
-- Table 'girls'
-- 
-- ---
DROP TABLE IF EXISTS `girls`;

CREATE TABLE `city` (
  `city_cd` int(11) NOT NULL AUTO_INCREMENT,
  `city_name` varchar(100) DEFAULT NULL,
  `country_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`city_cd`)
); ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

CREATE TABLE manufacturer (
  `manufacturer_id` int(11) NOT NULL AUTO_INCREMENT,
  `manufacturer_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`manufacturer_id`)
); ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

ALTER TABLE `guys` ADD FOREIGN KEY (gf_cd) REFERENCES `girls` (`girls_cd`);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `guys` ADD FOREIGN KEY (gf_cd) REFERENCES `girls` (`girls_cd`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `indi` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `guys` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `girls` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `indi` (`indi_cd`,`code`,`friend`,`asdf`) VALUES
-- ('','','','');
-- INSERT INTO `guys` (`guy_cd`,`guy_name`,`gf_cd`) VALUES
-- ('','','');
-- INSERT INTO `girls` (`girls_cd`,`girls_name`) VALUES
-- ('','');

"""

xmlHeader="""<?xml version="1.0" encoding="utf-8" ?>
<!-- SQL XML created by WWW SQL Designer, https://github.com/ondras/wwwsqldesigner/ -->
<!-- Active URL: http://webserver.wonjin.info/swModeling/wwwsqldesigner/ -->
<sql>
<datatypes db="mysql">
	<group color="rgb(238,238,170)" label="Numeric">
		<type label="Integer" quote="" sql="INTEGER" length="0"/>
	 	<type label="TINYINT" quote="" sql="TINYINT" length="0"/>
	 	<type label="SMALLINT" quote="" sql="SMALLINT" length="0"/>
	 	<type label="MEDIUMINT" quote="" sql="MEDIUMINT" length="0"/>
	 	<type label="INT" quote="" sql="INT" length="0"/>
		<type label="BIGINT" quote="" sql="BIGINT" length="0"/>
		<type label="Decimal" quote="" sql="DECIMAL" length="1" re="DEC"/>
		<type label="Single precision" quote="" sql="FLOAT" length="0"/>
		<type label="Double precision" quote="" sql="DOUBLE" length="0" re="DOUBLE"/>
	</group>

	<group color="rgb(255,200,200)" label="Character">
		<type label="Char" quote="'" sql="CHAR" length="1"/>
		<type label="Varchar" quote="'" sql="VARCHAR" length="1"/>
		<type label="Text" quote="'" sql="MEDIUMTEXT" length="0" re="TEXT"/>
		<type label="Binary" quote="'" sql="BINARY" length="1"/>
		<type label="Varbinary" quote="'" sql="VARBINARY" length="1"/>
		<type label="BLOB" quote="'" sql="BLOB" length="0" re="BLOB"/>
	</group>

	<group color="rgb(200,255,200)" label="Date &amp; Time">
		<type label="Date" quote="'" sql="DATE" length="0"/>
		<type label="Time" quote="'" sql="TIME" length="0"/>
		<type label="Datetime" quote="'" sql="DATETIME" length="0"/>
		<type label="Year" quote="" sql="YEAR" length="0"/>
		<type label="Timestamp" quote="'" sql="TIMESTAMP" length="0"/>
	</group>
	
	<group color="rgb(200,200,255)" label="Miscellaneous">
		<type label="ENUM" quote="" sql="ENUM" length="1"/>
		<type label="SET" quote="" sql="SET" length="1"/>
		<type label="Bit" quote="" sql="bit" length="0"/>
	</group>
</datatypes>

"""

##########################
### getting rid of comments
##########################

index=1
while index != 0:
    index=sql.find('\n',index) +1 #index points the first char of the sentence
    
    if sql[index:index+2]=='--':
        sql=sql[:index]+sql[sql.find('\n',index)+1:]
        index-=2

sqlPlainStatements=[]
sqlCreateStatements=[]
sqlAlterStatements=[]
tables=[]

sqlTuples=[sqlparse.parse(sqls) for sqls in sqlparse.split(sql)]

#print type (sqlTuples[0][0]) # =>  <class 'sqlparse.sql.Statement'>
for sqls in sqlTuples:
    #print sqls
    if sqls: #getting rid of empty tuples
        sqlPlainStatements.append(sqls[0])
        
#print sqlPlainStatements[1].get_type()  # => ret : u'CREATE'
for sqls in sqlPlainStatements:
    if sqls.get_type() == u'CREATE':
        sqlCreateStatements.append(sqls)

for sqls in sqlPlainStatements:
    if sqls.get_type() == u'ALTER':
        sqlAlterStatements.append(sqls)
#print sqlAlterStatements[0]
        
for sqls in sqlCreateStatements:
    singleTable=[]
    if(sqls.get_name()[0] =='`'):
        singleTable.append(sqls.get_name()[1:-1])
        #print sqls.get_name()[1:-1]
    else:
        singleTable.append(sqls.get_name())
        #print sqls.get_name()

    """
    # for checking structure
    idx=0
    while (sqls.token_next(idx)[0]):
        print idx,'Type:',type(sqls.token_next(idx)), type(sqls.token_next(idx)[0]),type(sqls.token_next(idx)[1]), '\
        || Data: ',sqls.token_next(idx)[0], sqls.token_next(idx)[1]
        idx+=2
    """    
    """
    # for checking
    idx=2
    print idx,'Data: ',sqls.token_next(idx)[0], sqls.token_next(idx)[1],'Type:',type(sqls.token_next(idx)), type(sqls.token_next(idx)[0]),type(sqls.token_next(idx)[1])

    idx=4
    print idx,'Data: ',sqls.token_next(idx)[0], sqls.token_next(idx)[1],'Type:',type(sqls.token_next(idx)), type(sqls.token_next(idx)[0]),
    print type(sqls.token_next(idx)[1])
    """
    
    singleTable.append(sqls.token_next(4)[1])
    
    tables.append(singleTable)
    
    #print '--'*20
    
    
tableUpdate=[]

for table in tables: #getting rid of ()
    stringTable=str(table[1])
    stringTable=stringTable[stringTable.find('(')+1:stringTable.rfind(')')] 
    #print stringTable
    table[1]=stringTable
    tableUpdate.append(table)
    
for table in tableUpdate: #getting rid of KEY
    Attributes=[]
    stringRows=[]
    
    stringTable=str(table[1])
    #print stringTable
    stringRows=stringTable.split(',')
    #print len(stringRows)
    for row in stringRows:
        row=row.replace('\n',' ')
        row=row.strip()
        #print row
        if row.find('KEY')==-1:
            Attributes.append(row)
    table[1]=Attributes

    """
    tableUpdate - {table}
    table - [name, {rows}]
    Total : tableUpdate[#table][1][#row]
    """
    
    
xmlStringTable="" #total for db
for table in tableUpdate: #getting rid of ` and split it by space and write XML
    rowAtoms=[]
    Attributes=[]
    xmlStringRow=""
    xmlStringRow="""<table x=" """ +str(random.randint(30,800))+""" " y=" """+str(random.randint(30,600))+""" " name=" """+table[0]+""" ">"""   #total for a table
    
    stringRows=table[1]
    #print 'stringRows : ',stringRows
    for row in stringRows:
        
        #print 'row :',row
        row=row.replace('`','')
        rowAtoms=row.split(' ')
        #print rowAtoms
        xmlStringRow=xmlStringRow+"""<row name=" """ + rowAtoms[0] + """" null="1" autoincrement="0">""" +'\n'
        
        rowAtoms=[word.strip() for word in rowAtoms]
        #print rowAtoms
        
        for word in rowAtoms:
            if word.find('INTEGER')!= -1:
                xmlStringRow=xmlStringRow+"""<datatype>"""+word.strip()+"""</datatype>"""+'\n'
        
        
        if row.find('DEFAULT NULL'):
            xmlStringRow=xmlStringRow+"""<default>NULL</default></row>"""+'\n'
        else :
            xmlStringRow=xmlStringRow+"""<default>NULL</default></row>"""+'\n' #needs more task
            
        #print xmlStringRow
    
            
    table[1]=Attributes
    xmlStringTable=xmlStringTable+xmlStringRow+'</table>'+'\n'
    
    
xmlHeader=xmlHeader+xmlStringTable+'</sql>'



print("Content-type: text/text\n")    #\n : unless, Internal Server Error!

form = cgi.FieldStorage()

print(xmlHeader)

