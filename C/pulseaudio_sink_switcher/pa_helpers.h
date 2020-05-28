#ifndef PA_HELPERS_H__
#define PA_HELPERS_H__

#include <pulse/context.h>
#include <pulse/error.h>
#include <pulse/introspect.h>
#include <pulse/mainloop.h>

typedef struct sink_info_sub_
{
  char name[50];
  uint32_t index;
  pa_cvolume volume;
  int mute;
} sink_info_sub;

typedef struct sink_input_info_sub_
{
  char name[50];
  uint32_t index;
  pa_cvolume volume;
  int mute;
} sink_input_info_sub;

typedef struct sink_info_
{
  uint8_t u1_sink_count;
  sink_info_sub sinks[5];
} sink_info;

typedef struct sink_input_info_
{
  uint8_t u1_sink_count;
  sink_input_info_sub sinks[20];
} sink_input_info;

void init_database();

pa_operation* list_sinks(pa_context *c);
pa_operation* list_sinks_inputs(pa_context *c);
double get_volume_for_sink_index(pa_context *c, int index);
void set_volume_for_sink_index(pa_context *c, int index, double volume);

#endif /* PA_HELPERS_H__ */
