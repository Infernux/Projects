#include "pa_helpers.h"

#include <math.h>
#include <string.h>

#include "helpers.h"

static sink_info st_sink_info;
static sink_input_info st_sink_input_info;

void add_sink_info(sink_info *sink_info, const pa_sink_info *new_info) {
  if (sink_info->u1_sink_count < MAX_SINK_COUNT) {
    sink_info_sub *sis = &sink_info->sinks[sink_info->u1_sink_count];
    PRINTF("sink %d name : %s\n", new_info->index, new_info->name);
    PRINTF("volume idx : %d %f\n", new_info->index, GET_VOLUME(new_info->volume));
    sis->index = new_info->index;
    strncpy(sis->name, new_info->name, 50);
    sis->volume = new_info->volume;
    sink_info->u1_sink_count++;
  }
}

void clear_sink_info(sink_info *sink_info) {
  sink_info->u1_sink_count = 0;
}

void add_sink_input_info(sink_input_info *sink_input_info, const pa_sink_input_info *new_info) {
  if (sink_input_info->u1_sink_count < MAX_SINK_INPUT_COUNT) {
    PRINTF("sink count : %d\n", sink_input_info->u1_sink_count);
    PRINTF("sink input %d name : %s\n", new_info->index, new_info->name);
    PRINTF("attached to sink index %d\n", new_info->sink);
    pa_cvolume volume = new_info->volume;
    PRINTF("volume ch : %d %f\n", volume.channels, GET_VOLUME(new_info->volume));

    printf("%d\n", new_info->index);
    sink_input_info_sub *sii = &sink_input_info->sinks[sink_input_info->u1_sink_count];
    strncpy(sii->name, new_info->name, 50);
    sii->volume = volume;
    sii->mute = new_info->mute;

    sink_input_info->u1_sink_count++;
  }
}

void clear_sink_input_info(sink_input_info *sink_input_info) {
  sink_input_info->u1_sink_count = 0;
}

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

  add_sink_info(&st_sink_info, i);
}

void sink_input_info_list_callback(pa_context *c, const pa_sink_input_info *i, int eol, void *userdata)
{
  PRINTF("%s\n", __func__);
  if(eol)
  {
    return;
  }

  add_sink_input_info(&st_sink_input_info, i);
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
