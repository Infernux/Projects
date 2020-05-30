#include "pa_helpers.h"

#include <math.h>
#include <string.h>

#include "helpers.h"

static sink_info st_sink_info;
static sink_input_info st_sink_input_info;

void init_database()
{
  st_sink_info.u1_sink_count = 0;
  st_sink_input_info.u1_sink_count = 0;
  memset(st_sink_info.sinks, 0, sizeof(sink_info_sub));
  memset(st_sink_input_info.sinks, 0, sizeof(sink_input_info_sub));
}

void context_success_callback(pa_context *c, int success, void *userdata)
{
  PRINTF("%s\n", __func__);
}

void sink_info_list_callback(pa_context *c, const pa_sink_info *i, int eol, void *userdata)
{
  PRINTF("%s\n", __func__);
  if(eol)
  {
    return;
  }

  sink_info_sub *sis = &st_sink_info.sinks[st_sink_info.u1_sink_count];
  PRINTF("sink %d name : %s\n", i->index, i->name);
  PRINTF("volume idx : %d %f\n", i->index, GET_VOLUME(i->volume));
  sis->index = i->index;
  strncpy(sis->name, sis->name, 50);
  sis->volume = i->volume;

  st_sink_info.u1_sink_count++;
}

void sink_input_info_list_callback(pa_context *c, const pa_sink_input_info *i, int eol, void *userdata)
{
  PRINTF("%s\n", __func__);
  if(eol)
  {
    return;
  }

  PRINTF("sink input %d name : %s\n", i->index, i->name);
  PRINTF("attached to sink index %d\n", i->sink);
  pa_cvolume volume = i->volume;
  PRINTF("volume ch : %d %f\n", volume.channels, GET_VOLUME(i->volume));

  printf("%d\n", i->index);
  sink_input_info_sub *sii = &st_sink_input_info.sinks[st_sink_input_info.u1_sink_count];
  strncpy(sii->name, i->name, 50);
  sii->volume = volume;
  sii->mute = i->mute;

  st_sink_input_info.u1_sink_count++;
}

pa_operation* list_sinks(pa_context *c)
{
  return pa_context_get_sink_info_list(c, sink_info_list_callback, NULL);
}

pa_operation* list_sinks_inputs(pa_context *c)
{
  return pa_context_get_sink_input_info_list(c, sink_input_info_list_callback, NULL);
}

double get_volume_for_sink_index(pa_context *c, int index)
{
  return pa_sw_volume_from_linear(pa_cvolume_avg(&st_sink_input_info.sinks[index].volume));
}

void set_volume_for_sink_index(pa_context *c, int index, double volume)
{
  double cur_volume = pa_sw_volume_to_linear(pa_cvolume_avg(&st_sink_input_info.sinks[index].volume));
  double diff_volume_linear = volume - cur_volume;
  double diff_volume = pa_sw_volume_from_linear(fabs(diff_volume_linear));

  pa_cvolume *new_volume;

  if(diff_volume_linear > 0.) {
    new_volume = pa_cvolume_inc(&st_sink_input_info.sinks[index].volume, diff_volume);
  } else if (diff_volume_linear < 0.) {
    new_volume = pa_cvolume_dec(&st_sink_input_info.sinks[index].volume, diff_volume);
  } else {
    return;
  }

  int userdata = 0x42; /* Use an enum */
  pa_context_set_sink_input_volume(c, index, new_volume, context_success_callback, &userdata);
}
