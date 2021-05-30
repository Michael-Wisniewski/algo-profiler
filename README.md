![lint](./.github/lint.svg)
![coverage](./.github/coverage.svg)

## algo-profiler

Package of profiling tools which allows to run:
* unit tests
* stress tests
* coverage tests
* single time check
* time check for the whole data set
* functions call time check
* functions call time check by line
* single memory check
* memory check by line

</br>

#### Output from runnig `test_script.py`:

```shell
                                    UNIT TESTS   
                                 
Function: search(wanted_name, names)
1/3 PASSED List with wanted name.
2/3 PASSED List without wanted name.
3/3 FAILED Test data with wrong anser.

FAILED TESTS SUMMARY

3/3 FAILED Test data with wrong anser.

False != 1


                                   STRESS TESTS   
                                
Function: search(wanted_name, names)
Function: naive_search(wanted_name, names)
1/10 PASSED input: 1
2/10 PASSED input: 112
3/10 PASSED input: 223
4/10 PASSED input: 334
5/10 PASSED input: 445
6/10 PASSED input: 556
7/10 PASSED input: 667
8/10 PASSED input: 778
9/10 PASSED input: 889
10/10 PASSED input: 1000

ALL TESTS PASSED



                                   COVERAGE TEST   
                               
Function: search(wanted_name, names)

There are missing lines.

Statements          Missed              Cover               
------------------------------------------------------------
9                   1                   89%                 
------------------------------------------------------------

> def search(wanted_name, names):
>     if len(names) == 0:
!         return False
  
>     name_index = False
      
>     for index, name in enumerate(names):
>         if name == wanted_name:
>             name_index = index
  
>     [1] * 10 ** 7 # creating list for slowing down code
      
>     return name_index


                                    TIME CHECK   
                                 
Function: search(wanted_name, names)

wanted_name: 'John'
names(100): ['thnrdydc', 'kqzpwppy', 'abweuj', 'cdbgl', 'eclggbij', 'ghitucvom', ...]

Function run time: 0.058536 sec

                                       TIMER   
                                   
Function: search(wanted_name, names)
Function iterations: 1


Run number             Function argument      Avg time (sec)         
---------------------------------------------------------------------
1/10                   1000                   0.06441631799680181    
---------------------------------------------------------------------
2/10                   2000                   0.0633777969997027     
---------------------------------------------------------------------
3/10                   3000                   0.06647152899677167    
---------------------------------------------------------------------
4/10                   4000                   0.06454603500606027    
---------------------------------------------------------------------
5/10                   5000                   0.06406402600259753    
---------------------------------------------------------------------
6/10                   6000                   0.06021741300355643    
---------------------------------------------------------------------
7/10                   7000                   0.062483297995640896   
---------------------------------------------------------------------
8/10                   8000                   0.0654375469966908     
---------------------------------------------------------------------
9/10                   9000                   0.06167987599474145    
---------------------------------------------------------------------
10/10                  10000                  0.06140587400295772    
---------------------------------------------------------------------


                                    C PROFILER   
                                 
Function: search(wanted_name, names)

wanted_name: 'John'
names(10): ['John', 'depyi', 'nviec', 'wnekfkym', 'actbnuzm', 'kvsurhsh', ...]

         5 function calls in 0.061 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.061    0.061 {built-in method builtins.exec}
        1    0.000    0.000    0.061    0.061 <string>:1(<module>)
        1    0.061    0.061    0.061    0.061 test_function.py:1(search)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}



                                   LINE PROFILER   
                               
Function: search(wanted_name, names)

wanted_name: 'John'
names(10): ['xlbahlit', 'egofoerl', 'ydwsdywic', 'wdufivdn', 'mtjpaop', 'mdvybzg', ...]

Timer unit: 1e-06 s

Total time: 0.060849 s
File: /home/mikex929/Desktop/kursy/profiling/drugie_podejscie/Profiler/test_function.py
Function: search at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           def search(wanted_name, names):
     2         1          3.0      3.0      0.0      if len(names) == 0:
     3                                                   return False
     4                                           
     5         1          1.0      1.0      0.0      name_index = False
     6                                               
     7        11          8.0      0.7      0.0      for index, name in enumerate(names):
     8        10          5.0      0.5      0.0          if name == wanted_name:
     9         1          1.0      1.0      0.0              name_index = index
    10                                           
    11         1      60828.0  60828.0    100.0      [1] * 10 ** 7 # creating list for slowing down code
    12                                               
    13         1          3.0      3.0      0.0      return name_index


                                   MEMORY CHECK   
                                
Function: search(wanted_name, names)

wanted_name 0.0001 MB: 'John'
names(10) 0.0007 MB: ['rqpdfx', 'ongjdih', 'awqqxsd', 'ufvmxcw', 'zmgal', 'znbja', ...]

Memory usage: 0.01 MiB

                                  MEMORY PROFILER   
                              
Function: search(wanted_name, names)

wanted_name 0.0001 MB: 'John'
names(10) 0.0007 MB: ['byacxdx', 'John', 'zbuskly', 'drdvl', 'nqtwmboe', 'wpfzx', ...]

Filename: /home/mikex929/Desktop/kursy/profiling/drugie_podejscie/Profiler/test_function.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
     1      0.0 MiB      0.0 MiB           1   def search(wanted_name, names):
     2      0.0 MiB      0.0 MiB           1       if len(names) == 0:
     3                                                 return False
     4                                         
     5      0.0 MiB      0.0 MiB           1       name_index = False
     6                                             
     7      0.0 MiB      0.0 MiB          11       for index, name in enumerate(names):
     8      0.0 MiB      0.0 MiB          10           if name == wanted_name:
     9      0.0 MiB      0.0 MiB           1               name_index = index
    10                                         
    11      0.1 MiB      0.1 MiB           1       [1] * 10 ** 7 # creating list for slowing down code
    12                                             
    13      0.1 MiB      0.1 MiB           1       return name_index

```

