# mysqldump import helper

This script works inside pipe to mysql cli and try life a little better. If nothing specified, its just add some sql statements to improve import speed.

```
$ ./mih.py --help
usage: mih.py [-h] [-b before.sql] [-a after.sql] [-l NUM] [-d DATABASE]

Slice MySQL sql dumps for faster uploading and reduce memory consumption

optional arguments:
  -h, --help            show this help message and exit
  -b before.sql, --before before.sql
                        Add content of file BEFORE sql dump
  -a after.sql, --after after.sql
                        Add content of file AFTER sql dump
  -l NUM, --line NUM    Enforce commit every NUM lines.
  -d DATABASE, --database DATABASE
                        Add code for creating and using DATABASE
 ```

- -b insert some file before main sql stream. Say for database creation, setting options and limits.
- -a insert some file after main sql stream. Useful for comitting changes, activating triggers, etc.
- -l insert "COMMIT;" after NUM inserts. Helps when you restore big dump on small machine
- -d add "DROP/CREATE database" in sql stream. For fast re-importing.

Example:

```
gzip -d -c file.sql.gz | mih.py -a re-index.sql -l 1000 -d test | mysql -u root
```

This script make in "as fast as possible" mode, no "no errors" flag here.
