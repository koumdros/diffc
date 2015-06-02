### Features ###
  * coloring
  * simple (1 python script)
  * portable (written in python, tested with python 2.x and 3.x)
  * fast

### Download ###
  * python 2.x ( >= 2.4 ) : http://diffc.googlecode.com/svn/trunk/bin/python2/diffc
  * python 3.x : http://diffc.googlecode.com/svn/trunk/bin/python3/diffc

### Usage ###
```
diffc [OPTION] FILE1 FILE2
```
```
... | diffc

ex.)
 svn diff ... | diffc 
 cat aaa.diff | diffc
 diffc < aaa.diff
```

### Screenshots ###
coloring the differences

![http://diffc.googlecode.com/svn/trunk/docs/images/diffc-screenshot-1.png](http://diffc.googlecode.com/svn/trunk/docs/images/diffc-screenshot-1.png)

supporting unified diff

![http://diffc.googlecode.com/svn/trunk/docs/images/diffc-screenshot-3.png](http://diffc.googlecode.com/svn/trunk/docs/images/diffc-screenshot-3.png)

using with a version control system

![http://diffc.googlecode.com/svn/trunk/docs/images/diffc-screenshot-4.png](http://diffc.googlecode.com/svn/trunk/docs/images/diffc-screenshot-4.png)

### Configurations ###
  * You can specify the underlying diff command used by **diffc** by setting up environment variable _DIFFC\_DIFF\_CMD_
```
 export DIFFC_DIFF_CMD=/usr/bin/diff
```

