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
  for(int idx=0; idx<bytecount; ++idx) \
  { \
    printf("%d", ((char*)addr)[idx]); \
  } \
  printf("\n"); \
}

//#define LOG(...) printf(__VA_ARGS__)
#define LOG(...)

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
static char* static_symbol(const char *filename, const char *addr_offset)
{
  char *res_value = NULL;
  int str_offset = -1;
  int str_table_offset = -1;

  int fd = open(filename, O_RDONLY);
  if(fd==-1)
  {
    LOG("Failed to open file %s\n", filename);
    return NULL;
  }

  struct stat fd_stat;
  fstat(fd, &fd_stat);
  void *map_start = mmap(0, fd_stat.st_size, PROT_READ, MAP_SHARED, fd, 0);
  if(map_start == MAP_FAILED)
  {
    LOG("\tmmap, failed %s\n", strerror(errno));
    exit(1);
  }

  Elf64_Ehdr *header = (Elf64_Ehdr *)map_start;
  Elf64_Shdr *sections = (Elf64_Shdr*)((char*)map_start + header->e_shoff);

  /* e_shstrndx is indexed on 1 */
  int str_section_idx = header->e_shstrndx - 1;

  LOG("\tstr offset : %x\n", header->e_phoff);
  LOG("\toffset : %x\n", header->e_shoff);
  LOG("\tSection count %d\n", header->e_shnum);
  LOG("\tString table offset : %d\n", header->e_shstrndx);

  for(int i=0; i<header->e_shnum; ++i)
  {
    if(sections[i].sh_type == SHT_SYMTAB)
    {
      LOG("\t== SHT_SYMTAB ==\n");

      str_table_offset = sections[i].sh_name;
      LOG("\t\tSection size : %x, %d, offset : %x\n", sections[i].sh_size, sections[i].sh_name, sections[i].sh_offset);
      LOG("\t\tSymbol count : %d\n", sections[i].sh_size / sizeof(Elf64_Sym));

      char *syms = map_start + sections[i].sh_offset;
      uint64_t int_addr_offset = strtol(addr_offset, NULL, 16);
      for(size_t sym_idx = 0; sym_idx < sections[i].sh_size / sizeof(Elf64_Sym); ++sym_idx, syms += sections[i].sh_entsize)
      {
        Elf64_Sym *loc_sym = (Elf64_Sym*)syms;

        if(int_addr_offset == loc_sym->st_value) {
          LOG("\t\tsym value = %x\n", loc_sym->st_name);
          str_offset = loc_sym->st_name;
        }
      }
      LOG("\t\tSymbol count : %d\n", sections[i].sh_size / sizeof(Elf64_Sym));
    } 
  }

  if(sections[str_section_idx].sh_type == SHT_STRTAB) {
    if(str_table_offset == -1)
    {
      LOG("\tstr_table_offset not set\n");
      return NULL;
    }

    LOG("\t== SHT_STRTAB ==\n");

    LOG("\t\tSection size : %x\n", sections[str_section_idx].sh_size);

    char *sym_addr = map_start + sections[str_section_idx].sh_offset + str_offset;
    size_t sym_name_len = strlen(sym_addr);
    if(sym_name_len > 500) {
      LOG("\t\tSymbol name probably too long, bailing\n");
      return NULL;
    }
    res_value = (char*)malloc(sizeof(char) * (sym_name_len + 1));
    strncpy(res_value, sym_addr, sym_name_len);
    res_value[sym_name_len] = '\0';
  }

  int ret = munmap(map_start, fd_stat.st_size);
  if (ret != 0) {
    LOG("(%s:%d) Failed munmap\n", __func__, __LINE__);
    if(res_value) {
      free(res_value);
    }
    close(fd);
    exit(1);
  }

  close(fd);

  return res_value;
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
    char *sym_name = static_symbol(fun_info, &fun_info[plus+1]);
    if(sym_name) {
      printf("(call to static function %s)\n", sym_name);
      free(sym_name);
    }
  } else {
    printf("(call to %s)\n", &fun_info[start]);
  }
}

__attribute__((no_instrument_function))
void __cyg_profile_func_enter(void *this_fn,
    void *call_fn)
{
  LOG("own pid : %d\n", getpid());

  //char **sym = backtrace_symbols(&this_fn, 1);
  char **sym = backtrace_symbols(&this_fn, 1);
  print_function_name(sym[0]);
  free(sym);
}
