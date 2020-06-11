#ifndef PA_TLV_MAPPER_H__
#define PA_TLV_MAPPER_H__

#include "queue.h"
#include "tlv.h"

enum {
  TYPE_LIST_SINKS,
  TYPE_LIST_INPUT_SINKS,
  TYPE_MUTE_SINK,
  TYPE_MUTE_INPUT_SINK,
  TYPE_MOVE_INPUT_SINK
};

void add_tlv_value_to_queue(Queue *queue, TLV *tlv);

#endif /* PA_TLV_MAPPER_H__ */
