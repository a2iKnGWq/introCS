//greedy algorithm

#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void)
{
    float received;

    //prompt for change
    do
    {
        received = get_float();
    }
    while(received <0);

    int cents = round(100*received);
    int coins = 0;

    for (int i = 25; i > 0; i--)
    {
        if (i == 25 || i == 10 || i == 5 || i == 1)
        {
            //subtract 25 cents
            while (cents >= i)
            {
                cents -= i;
                coins++;
            }
        }
    }

    //print out
    printf("%i\n", coins);
}
