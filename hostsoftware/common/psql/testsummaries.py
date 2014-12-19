#!/bin/env python2

from dbmanager import DBManager

dbman = DBManager("dbname=zaehlrohr user=zaehlrohr", "30C3")

print dbman.get_summary('daily','ErsterStock')

print dbman.get_capsules('Baellebad')
