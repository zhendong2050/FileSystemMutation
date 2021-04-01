# FileSystemMutation
Hooking file related function calls
## Deps
* python-pysparser
  * sudo apt-get update -y
  * sudo apt-get install -y python-pycparser
* pycparser-fake-libc
  * pip3 install pycparser-fake-libc
* Python3 and gcc 
  * They should be already in your Linux system.
## Running the example
* Result demo

Original source code
```
 #include <stdio.h>
 
 int main() {
    FILE *fp;
    char c[1000];
 
    fp = fopen("test.txt", "r");
    fscanf(fp, "%[^\n]", c);
    printf("Data from the file: \n%s\n", c);
    fclose(fp);
    return 0;
 }

```
Instrumented source code
```
#include <stdio.h>

int main()
{
  FILE *fp;
  char c[1000];
  fopen_handler("test.txt", "r", "../../examples/example.c:7:9"); //prehandler function: the last arg indicating the context 
  fp = fopen("test.txt", "r");
  fscanf(fp, "%[^\n]", c);
  printf("Data from the file: \n%s\n", c);
  fclose(fp);
  return 0;
}

```
* Step 1: instrumenting source code with PycParser
  * git clone https://github.com/zhendong2050/FileSystemMutation.git
  * cd examples
  * python3 ../instrumentation/instrumentor/instrumentor.py example.c > example_inst.c
  
  You will find the fopenHander has been instrumented in the source cde in file example_inst.c      

* Step 2: packing the prehander as a static library
  * cd instrumentation
  * gcc -c codebean.c -o codebean.o
  * ar rcs libcodebean.a codebean.o
  
* step 3: compiling the instrumented code
  * cd examples
  * gcc -I../instrumentation example_inst.c ../instrumentation/libcodebean.a -o example_inst

* step 4: running the instrumented code
  * ./example_inst

  You find the prehandler is executed. The message "handling the input file: test.txt"! 

##ToDo

The hooking function "fopen" is sort of done (you also can add other functions that need to be instrumented in the instrumentor.py file). 

Now the preHander does nothing but printing "handling the input file".  For file system mutation, you can play the fopen_handler function, e.g., mutating the file or replacing file with others before it is executed. Simply speaking, we can implement our idea in the prehandler function. Roughly, we have the following ToDos:   

* designing a structure to maintain the target file and its mutants 
* monitoring the input being executed and selecting the corresponding file mutants
* designing a strategy for selecting file mutant
* designing how file mutation operators

Have fun!!!


