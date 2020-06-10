#ifndef PA_HELPERS_H__
#define PA_HELPERS_H__

#include <pulse/context.h>
#include <pulse/error.h>
#include <pulse/introspect.h>
#include <pulse/mainloop.h>

#define GET_VOLUME(volume) pa_sw_volume_to_linear(volume.values[0])

#define MAX_SINK_COUNT 5
#define MAX_SINK_INPUT_COUNT 20

typedef struct sink_info_sub_
{
  uint8_t valid;
  char name[50];
  uint32_t index;
  pa_cvolume volume;
  int mute;
} sink_info_sub;

typedef struct sink_input_info_sub_
{
  uint8_t valid;
  char name[50];
  uint32_t index;
  uint32_t sink_index;
  pa_cvolume volume;
  int mute;
} sink_input_info_sub;

typedef struct sink_info_
{
  uint8_t u1_sink_count;
  sink_info_sub sinks[MAX_SINK_COUNT];
} sink_info;

typedef struct sink_input_info_
{
  uint8_t u1_sink_count;
  sink_input_info_sub sinks[MAX_SINK_INPUT_COUNT];
} sink_input_info;

void init_database();

pa_operation* list_sinks(pa_context *c, void *args);
pa_operation* list_sinks_inputs(pa_context *c, void *args);
pa_operation* mute_sink(pa_context *c, void *args);
pa_operation* mute_sink_input(pa_context *c, void *args);
double get_volume_for_sink_index(pa_context *c, int index);
void set_volume_for_sink_index(pa_context *c, int index, double volume);

#endif /* PA_HELPERS_H__ */
