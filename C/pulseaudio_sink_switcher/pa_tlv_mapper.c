#include "pa_tlv_mapper.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pa_helpers.h"
#include "queue.h"

void add_tlv_value_to_queue(Queue *queue, TLV *tlv) {
  Transaction transaction;
  switch(tlv->type) {
    case TYPE_LIST_SINKS:
      transaction.func = list_sinks;
      transaction.args = NULL;
      break;
    case TYPE_LIST_INPUT_SINKS:
      transaction.func = list_sinks_inputs;
      transaction.args = NULL;
      break;
    case TYPE_MUTE_SINK:
      transaction.func = mute_sink;
      transaction.args = malloc(sizeof(uint32_t) * 1);
      memcpy(transaction.args, tlv->value, sizeof(uint32_t) * 1);
      break;
    case TYPE_MUTE_INPUT_SINK:
      transaction.func = mute_sink_input;
      transaction.args = malloc(sizeof(uint32_t) * 1);
      memcpy(transaction.args, tlv->value, sizeof(uint32_t) * 1);
      break;
    case TYPE_MOVE_INPUT_SINK:
      transaction.func = move_sink_input_to_sink_idx;
      transaction.args = malloc(sizeof(uint32_t) * 2);
      memcpy(transaction.args, tlv->value, sizeof(uint32_t) * 2);
      break;
    default:
      printf("Unknown instruction");
      break;
  }
  push(queue, transaction);
}
