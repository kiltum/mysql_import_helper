#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

def start_sql():
	return """
SET @@local.net_read_timeout=100000;
SET @@GLOBAL.connect_timeout=100000;
SET @@GLOBAL.wait_timeout=100000;
SET @@GLOBAL.interactive_timeout=100000;
SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT;
SET AUTOCOMMIT = 0;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS;
SET UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;
"""

def end_sql():
	return """
COMMIT;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET AUTOCOMMIT = @OLD_AUTOCOMMIT;
QUIT
"""

def main():
	parser = argparse.ArgumentParser(description='Slice MySQL sql dumps for faster uploading and reduce memory consumption')
	parser.add_argument("-b", "--before", metavar='before.sql', help="Add content of file BEFORE sql dump")
	parser.add_argument("-a", "--after", metavar='after.sql', help="Add content of file AFTER sql dump")
	parser.add_argument("-l", "--line", type = int, metavar='NUM', help="Enforce commit every NUM lines.")
	parser.add_argument("-d", "--database", help="Add code for creating and using DATABASE")

	args = parser.parse_args()

	if args.before:
		if not os.path.isfile(args.before):
			print "%s not exist. abort" % args.before
			return

	if args.after:
		if not os.path.isfile(args.after):
			print "%s not exist. abort" % args.after
			return

	slice_at = 1000000
	if args.line:
		slice_at = args.line

	# ok, start

	print start_sql()

	if args.database:
		print "DROP DATABASE IF EXISTS %s;" % args.database
		print "CREATE DATABASE IF NOT EXISTS %s;" % args.database
		print "USE %s;" % args.database

	if args.before:
		file = open(args.before,"r")
		for line in file:
			print line,
		file.close()
	
	count = 1
	line_before = ""

	for line in sys.stdin:
		print line,
		# flush only on INSERT statements
		if "INSERT" in line_before: 
			count = count + 1
			if count > slice_at:
				count = 1
				print "COMMIT;"
		
		line_before = line

	if args.after:
		file = open(args.after,"r")
		for line in file:
			print line,
		file.close()

	print end_sql()

if __name__ == "__main__":
    main()