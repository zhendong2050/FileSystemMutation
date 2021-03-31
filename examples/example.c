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
