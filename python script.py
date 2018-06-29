#!/usr/bin/env python3
'''importing the database functions from funcsdb file'''
from funcsdb import send_query1, send_query2, send_query3

'''each query is calling a function to load the results from
 datapase into query array containing results'''

query1 = send_query1()
query2 = send_query2()
query3 = send_query3()

'''print the data in each array using format method to concatenate the
 results in an appropriate way such as psql does in it's shell'''

print("-------------------the most popular three articles--------------------")
print("", )

for x in range(0, 3):
    print("{0:30}         {1:6} views".format(query1[x][0], query1[x][1]))

print("", )
print("----------------the most popular three article authors----------------")

print("", )

for y in range(0, 4):
    print("{0:30}         {1:6} views".format(query2[y][0], query2[y][1]))

print("", )
print("-----------days when more than 1% of requests lead to errors----------")
print("", )

print("{0:30} 		{1:6} ".format(query3[0][0], query3[0][1]))
print("",)
