#include "pa_helpers.h"

#include <math.h>
#include <string.h>

#include "helpers.h"

static sink_info st_sink_info;
static sink_input_info st_sink_input_info;

void add_sink_info(sink_info *sink_info, const pa_sink_info *new_info) {
  if (sink_info->u1_sink_count < MAX_SINK_COUNT) {
    sink_info_sub *sis = &sink_info->sinks[sink_info->u1_sink_count];
    sis->index = new_info->index;
    strncpy(sis->name, new_info->name, 50);
    sis->volume = new_info->volume;
    sink_info->u1_sink_count++;
    PRINTF("sink %u name : %s\n", sis->index, sis->name);
    PRINTF("volume idx : %d %f\n", sis->index, GET_VOLUME(sis->volume));
  }
}

void clear_sink_info(sink_info *sink_info) {
  sink_info->u1_sink_count = 0;
}

void get_sink_info(sink_info *sink_info) {
  for(uint32_t i=0; i<sink_info->u1_sink_count; ++i) {
    sink_info_sub *sis = &sink_info->sinks[sink_info->u1_sink_count];
    PRINTF("sink %u name : %s\n", sis->index, sis->name);
    PRINTF("volume idx : %d %f\n", sis->index, GET_VOLUME(sis->volume));
  }
}

void add_sink_input_info(sink_input_info *sink_input_info, const pa_sink_input_info *new_info) {
  if (sink_input_info->u1_sink_count < MAX_SINK_INPUT_COUNT) {
    pa_cvolume volume = new_info->volume;

    sink_input_info_sub *sii = &sink_input_info->sinks[sink_input_info->u1_sink_count];
    strncpy(sii->name, new_info->name, 50);
    sii->volume = volume;
    sii->mute = new_info->mute;
    sii->sink_index = new_info->sink;

    PRINTF("sink input %u name : %s\n", new_info->index, new_info->name);
    PRINTF("attached to sink index %u\n", sii->sink_index);
    PRINTF("volume ch : %d %f\n", sii->volume.channels, GET_VOLUME(sii->volume));

    sink_input_info->u1_sink_count++;
  }
}

void clear_sink_input_info(sink_input_info *sink_input_info) {
  sink_input_info->u1_sink_count = 0;
}

void get_sink_input_info(sink_input_info *sink_input_info) {
  for(uint32_t i=0; i < sink_input_info->u1_sink_count; ++i) {
    sink_input_info_sub *sii = &sink_input_info->sinks[sink_input_info->u1_sink_count];
    PRINTF("sink input %d name : %s\n", sii->index, sii->name);
    PRINTF("attached to sink index %d\n", sii->sink_index);
    PRINTF("volume ch : %d %f\n", sii->volume.channels, GET_VOLUME(sii->volume));

    printf("%d\n", sii->index);
  }
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
  if(eol)
  {
    return;
  }

  add_sink_info(&st_sink_info, i);
}

void sink_input_info_list_callback(pa_context *c, const pa_sink_input_info *i, int eol, void *userdata)
{
  if(eol)
  {
    int fd = *((int*)userdata);
    int b = st_sink_input_info.u1_sink_count;
    printf("sent ? %d\n", write(fd, (void*)&b, sizeof(int)));
    sleep(1);
    for(int i=0; i<st_sink_input_info.u1_sink_count; ++i) {
      sink_input_info_sub *sii = &st_sink_input_info.sinks[i];
      printf("%s\n", sii->name);
      printf("sent %d? %d\n", i, write(fd, (void*)sii->name, sizeof(char)*50));
    }
    return;
  }

  add_sink_input_info(&st_sink_input_info, i);
}

pa_operation* list_sinks(pa_context *c, void* args, int *fd)
{
  return pa_context_get_sink_info_list(c, sink_info_list_callback, NULL);
}

pa_operation* list_sinks_inputs(pa_context *c, void* args, int *fd)
{
  clear_sink_input_info(&st_sink_input_info);
  return pa_context_get_sink_input_info_list(c, sink_input_info_list_callback, fd);
}

void move_sink_input_to_sink_idx_callback(pa_context *c, int success, void *userdata)
{
  PRINTF("%s\n", __func__);
}

pa_operation* move_sink_input_to_sink_idx(pa_context *c, void* args, int *fd) {
  uint32_t *u32_args = (uint32_t*)args;
  const uint32_t sink_input_idx = u32_args[0];
  const uint32_t sink_idx = u32_args[1];
  return pa_context_move_sink_input_by_index(c, sink_input_idx, sink_idx, move_sink_input_to_sink_idx_callback, NULL);
}

void mute_sink_callback(pa_context *c, int success, void *userdata)
{
  PRINTF("%s\n", __func__);
}

pa_operation* mute_sink(pa_context *c, void *args, int *fd) {
  PRINTF("%s\n", __func__);
  const uint32_t index = *((uint32_t*)args);
  PRINTF("Muting sink %d\n", index);
  return pa_context_set_sink_mute_by_index(c, index, 1, mute_sink_callback, NULL);
}

void mute_sink_input_callback(pa_context *c, int success, void *userdata)
{
  PRINTF("%s : success %d\n", __func__, success);
}

pa_operation* mute_sink_input(pa_context *c, void *args, int *fd) {
  PRINTF("%s\n", __func__);
  const uint32_t index = *((uint32_t*)args);
  PRINTF("Muting sink input %d\n", index);
  return pa_context_set_sink_input_mute(c, index, 1, mute_sink_input_callback, NULL);
}

pa_operation* set_sink_input_volume(pa_context *c, void *args, int *fd) {
  PRINTF("%s\n", __func__);
  const uint32_t index = ((uint32_t*)args)[0];
  const uint32_t volume = ((uint32_t*)args)[1];
  return pa_context_set_sink_input_volume(c, index, 1, mute_sink_input_callback, NULL);
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
