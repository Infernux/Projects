#include "pa_tlv_mapper.h"

#include <stdio.h>

#include "pa_helpers.h"
#include "queue.h"

void add_tlv_value_to_queue(Queue *queue, TLV *tlv) {
  switch(tlv->type) {
    case 0:
      push(queue, list_sinks_inputs);
      break;
    default:
      printf("Unknown instruction");
      break;
  }
}
