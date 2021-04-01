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
  * cd    
 
* Step 2
