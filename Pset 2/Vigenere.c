//SOMEWHY IT DOESN'T WORK FOR PLAINTEXT: world!$? ..BUT SEEMS TO WORK FOR EVEYTHING ELSE...

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // validity checking
    if (argc == 2 )
    {
        int local = 0;
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!(isalpha(argv[1][i])))
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
            printf("Usage: ./vigenere keyword\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }



    //changing keyword to an array of ints      a = 0, b = 1, ...
    int key[strlen(argv[1])];

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (islower(argv[1][i]))
        {
            key[i] = (int) (argv[1][i] - 'a');
        }
        else
        {
            key[i] = (int) (argv[1][i] - 'A');
        }
    }



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
        else if (isupper(plain[i]))
        {
            numbers[i] = (int) (plain[i] - 'A');
        }
        else
        {
            numbers[i] = 30;        //just something other
        }
    }



    int new_numbers[strlen(plain)];

    for (int i = 0, n = strlen(plain), k = strlen(argv[1]), j = 0; i < n; i++)
    {
        if (isalpha(plain[i]))
        {
            new_numbers[i] = (numbers[i] + key[ j % k]) % 26;
            j++;
        }
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
            else if (isupper(plain[i]))
            {
                cipher[i] = (char) (new_numbers[i] + 'A');
            }
            else
            {
                eprintf("alpha not lower nor upper... idk what that means..\n");
            }
        }
        else
        {
            cipher[i] = plain[i];
        }
    }


    //output

    printf("ciphertext: %s\n", cipher);
}
