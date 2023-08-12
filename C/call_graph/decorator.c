#include "decorator.h"

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#include <errno.h>
#include <elf.h>
#include <execinfo.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>

#define DUMP_ADDR(addr, bytecount) \
{ \
  for(int aa=0; aa<bytecount; ++aa) \
  { \
    printf("%d", ((char*)addr)[aa]); \
  } \
  printf("\n"); \
}

__attribute__((no_instrument_function))
static char* find_str_offset(char *base_addr, int index)
{
  base_addr += 1;
  for(int i=0; i<index; ++i)
  {
    size_t offset = strlen(base_addr);
    base_addr += (offset+1);
  }
  return base_addr;
}

__attribute__((no_instrument_function))
static void static_symbol(const char *filename, const char *addr_offset)
{
  printf("===\n%s\n===", addr_offset);
  int str_offset = -1;
  int str_table_offset = -1;

  int fd = open(filename, O_RDONLY);
  if(fd==-1)
  {
    printf("Failed to open file %s\n", filename);
    return;
  }

  struct stat fd_stat;
  fstat(fd, &fd_stat);
  printf("size %d\n", fd_stat.st_size);
  void *map_start = mmap(0, fd_stat.st_size, PROT_READ, MAP_SHARED, fd, 0);
  if(map_start == MAP_FAILED)
  {
    printf("fded %s\n", strerror(errno));
    exit(1);
  }
  printf("map %p\n", map_start);

  Elf64_Ehdr *header = (Elf64_Ehdr *)map_start;
  printf("str offset : %x\n", header->e_phoff);
  printf("offset : %x\n", header->e_shoff);
  Elf64_Shdr *sections = (Elf64_Shdr*)((char*)map_start + header->e_shoff);
  printf("Section count %d\n", header->e_shnum);

  int found_str_sections = -1;
  for(int i=0; i<header->e_shnum; ++i)
  {
    //printf("\twoot %x, size : %x\n", sections[i].sh_offset, sections[i].sh_size);
    if(sections[i].sh_type == SHT_SYMTAB)
    {
      printf("\t== SHT_SYMTAB ==\n");

      str_table_offset = sections[i].sh_name;
      printf("\t\tSection size : %x, %d, offset : %x\n", sections[i].sh_size, sections[i].sh_name, sections[i].sh_offset);
      printf("\t\tSymbol count : %d\n", sections[i].sh_size / sizeof(Elf64_Sym));

      char *syms = map_start + sections[i].sh_offset;
      //printf("\t\tsym size = %x, %x\n", syms->st_size, sections[i].sh_offset);
      uint64_t int_addr_offset = strtol(addr_offset, NULL, 16);
      for(size_t sym_idx = 0; sym_idx < sections[i].sh_size / sizeof(Elf64_Sym); ++sym_idx, syms += sections[i].sh_entsize)
      {
        Elf64_Sym *loc_sym = (Elf64_Sym*)syms;

        if(int_addr_offset == loc_sym->st_value) {
          printf("\t\tsym value = %x\n", loc_sym->st_name);
          str_offset = loc_sym->st_name;
        }
      }
      printf("\t\tSymbol count : %d\n", sections[i].sh_size / sizeof(Elf64_Sym));
    } else if(sections[i].sh_type == SHT_STRTAB) {
      found_str_sections++;
      if(str_table_offset == -1)
      {
        printf("str_table_offset not set\n");
        continue;
      }

      if(found_str_sections == str_table_offset)
      {
        printf("== SHT_STRTAB ==\n");

        printf("Section size : %x\n", sections[i].sh_size);

        //char *sym_addr = find_str_offset(map_start + sections[i].sh_offset, str_offset);
        char *sym_addr = map_start + sections[i].sh_offset + str_offset;
        printf("\tStatic sym : %s\n", sym_addr);
      }
    }
  }
  close(fd);
}

__attribute__((no_instrument_function))
static void print_function_name(char *fun_info)
{
  size_t info_len = strlen(fun_info);

  size_t i=0;
  size_t start = 0, end = 0, plus = 0;
  for(i=0; i<info_len; ++i)
  {
    if(fun_info[i] == '(')
    {
      start = i+1;
      fun_info[i] = '\0';
    }

    if(fun_info[i] == '+')
    {
      plus = i;
      fun_info[plus] = '\0';
    }

    if(fun_info[i] == ')')
    {
      end = i;
      fun_info[end] = '\0';
      break;
    }
  }

  if(plus == start)
  {
    printf("(call to static function %s)\n", &fun_info[plus+1]);
    printf("call (%s)\n", fun_info);

    static_symbol(fun_info, &fun_info[plus+1]);
  } else {
    printf("(call to %s)\n", &fun_info[start]);
  }
}

__attribute__((no_instrument_function))
void __cyg_profile_func_enter(void *this_fn,
    void *call_fn)
{
  printf("own pid : %d\n", getpid());



  //char **sym = backtrace_symbols(&this_fn, 1);
  char **sym = backtrace_symbols(&this_fn, 1);
  print_function_name(sym[0]);
}
