 # Questions    //in 2019 pset3

## What's `stdint.h`?

A header file in bmp.h what originally contains exact-width integer types (typedef uint8_t  BYTE;
typedef uint32_t, int32_t, uint16_t
)

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

To make it more space efficent, not dealing with extra storage unnecessarily. we need exact lengths of values to not slip when a program reads it.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 3, 3, 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

0x4d42 (0x stands for hexadecimal)

## What's the difference between `bfSize` and `biSize`?

bfSize: The size, in bytes, of the bitmap file.
biSize: The number of bytes required by the structure.

## What does it mean if `biHeight` is negative?

The bitmap is a top-down DIB and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

Couldn't find, or malloc space in RAM.

## Why is the third argument to `fread` always `1` in our code? (For example, see lines 40, 44, and 75.)

The 2nd argument is the size of a struct, and we want to read/write only one struct.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Changes the filepointer's offset (for instance from where to read)

## What is `SEEK_CUR`?

The (current) location of the filepointer's offset from where it can be changed
