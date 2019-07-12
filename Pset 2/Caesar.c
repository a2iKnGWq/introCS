#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc == 2 )
    {
        int local = 0;
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!(isdigit(argv[1][i])))
            {
                local = 1;
                break;
            }
        }
        if (local == 0)
        {
            printf("Success\n%s\n", argv[1]);
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]);



    string plain = get_string("plaintext: ");
    printf("\n");


    int numbers[strlen(plain)];

    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        if (islower(plain[i]))      //check if isupper or islower
        {
            numbers[i] = (int) (plain[i] - 'a');        // (int) transforms to ascii        - 'a' ???
        }
        //do something with the non-alpha charachters
        else      //think it's isupper
        {
            numbers[i] = (int) (plain[i] - 'A');
        }
    }

    int new_numbers[strlen(plain)];

    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        new_numbers[i] = (numbers[i] + key)%26;
    }

    //transform "back" everything
    char cipher[strlen(plain)];
    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        if (isalpha(plain[i]))
        {
            if (islower(plain[i]))      //check if isupper or islower
            {
                cipher[i] = (char) (new_numbers[i] + 'a');        // (int) transforms to ascii    - 'a' ???
            }
            //do something with the non-alpha charachters
            else      //think it's isupper
            {
                cipher[i] = (char) (new_numbers[i] + 'A');
            }
        }
        else
        {
            cipher[i] = plain[i];
        }
    }



    //output

    printf("ciphertext: ");
    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        printf("%c", cipher[i]);
    }
    printf("\n");
}
