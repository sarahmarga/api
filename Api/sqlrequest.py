#!/usr/bin/python
# -*- coding: utf-8 -*- 

import  sqlite3

def getAllRecord(table,c):
    rq = "select * from " +table+" order by id desc"
    return c.execute(rq)

def getRecord(table,idt,c):
    rq = "select * from " +table+ " where id = '"+str(idt)+"'" 
    return c.execute(rq)
    #return c.fetchall

def createNewRecord(table,param,c):
    rq="INSERT INTO "+table+" "
    par="("
    for key in param.keys():
        par=par+key+","
    rq=rq+par[:-1]+") VALUES "
    par="("
    for val in param.values():
        par=par+"'"+str(val)+"',"
    rq=rq+par[:-1]+")"
    return c.execute(rq)
    
    

def updateFieldRecord(table,param,idt,c):
    rq= "update "+ table +" set"
    par = " "
    cl = []
    vl = []
    
    for key in param.keys():
  cl.append(key)
    
    for val in param.values():
	vl.append(val)
 
    for j in range(len(cl)):
        par = par+cl[j]+"= '"+str(vl[j])+"',"
    rq = rq+par[:-1]+" where id = '"+str(idt)+"'" 
    return c.execute(rq)
    #c.execute("select * from "+table)
    #return c.fetchall()
    

def deleteRecord(table,idt,c):
  
    rq="delete from "+ table +" where id = '"+str(idt)+"'"
    return c.execute(rq)
    #return c.fetchall()


def getIdperson(table,entry,c):
    
    rq = "select id from "+table+" where name = "+entry+ "or function= "+entry
    c.execute(rq)
    idt=c.fetchone()
    if idt is not None:
    	return idt
    else:
	return 0

def getId(table,entry,c):
    
    rq = "select id from "+table+" where name = "+entry 
    c.execute(rq)
    idt=c.fetchone()
    if idt is not None:
    	return idt
    else:
	return 0  
