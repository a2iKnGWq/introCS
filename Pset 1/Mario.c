#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int h;

    do
    {
        h = get_int("height: \n");
    }
    while (h < 0 || h > 23);        //   valid hights 0 - 23

    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h-1-i; j++)     //print spaces
        {
            printf(" ");
        }
        for (int k = 0; k < 1+i; k++)     //print hashes
        {
            printf("#");
        }

        printf("  ");       //in between space

        for (int k = 0; k < 1+i; k++)     //print 2nd hashes
        {
            printf("#");
        }
        for (int j = 0; j < h-1-i; j++)     //print 2nd spaces
        {
            printf(" ");
        }
        printf("\n");       //new line
    }
}
