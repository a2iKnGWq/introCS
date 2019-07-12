// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 676        //definitelly need bigger, but first let just try to iplement

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    int n = tolower(word[0]) - 'a';
    int m = (word[1] != '\0') ? (tolower(word[1]) - 'a') : 0;
    return 26*n + m;
}

unsigned int words = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO

        //for each new word malloc a node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        //copy word into node
        strcpy(new_node->word, word);

        //set poiter in node

        int index = hash(new_node->word);

        if (hashtable[index] == NULL)
        {
            hashtable[index] = new_node;
            new_node->next = NULL;
        }
        else
        {
            new_node->next = hashtable[index];
            hashtable[index] = new_node;
        }

        words++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return words;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    node *cursor = hashtable[hash(word)];

    int slen = strlen(word);
    char wordnew[slen + 1];
    for(int i = 0; i < slen; i++)
    {
        wordnew[i] = tolower(word[i]);
    }
    wordnew[slen] = '\0';

    while (cursor != NULL)
    {
        if(strcmp(cursor->word, wordnew) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    for(int i = N-1; i > -1; i--)
    {
        node *cursor = hashtable[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
    //return false;
}
