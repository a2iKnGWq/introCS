#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        fprintf(stderr, "Usage: 2 argumentum vactor\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Couldn't open file\n");
        return 2;
    }

    unsigned char buffer[512];      //unsigned int would be too large
        //with unsigned int [128]   the main boolean could be simpler   0xffd8ffe0 <= buffer[0] <= 0xffd8ffef
    FILE *img = NULL;

    int jpegcount = 0;
    while (fread(buffer, sizeof(unsigned char), 512, file) == 512)       //alternative boolean ((ch = fgetc(file)) != EOF)
    {

        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] >= 0xe0) && (buffer[3] <= 0xef)))
        {
            //start new
            jpegcount++;

            char filename[8];
            sprintf(filename, "%03i.jpg", jpegcount-1);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fprintf(stderr, "Couldn't open file\n");
                return 3;
            }
            fwrite(buffer, sizeof(char), 512, img);
            fclose(img);
        }

        else
        {
            if (jpegcount > 0) //already found a new jpeg?
            {
                //fopen  with 'a'
                char filename[8];
                sprintf(filename, "%03i.jpg", jpegcount-1);
                img = fopen(filename, "a");
                if (img == NULL)
                {
                    fprintf(stderr, "Couldn't open file\n");
                    return 3;
                }
                fwrite(buffer, sizeof(char), 512, img);
                fclose(img);
            }
        }
    }

    fclose(file);
}