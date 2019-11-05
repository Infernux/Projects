#include <stdio.h>
#include <stdlib.h>

#include <pulse/context.h>
#include <pulse/error.h>
#include <pulse/introspect.h>
#include <pulse/mainloop.h>

#define PRINTF(format, ...) printf(format, ##__VA_ARGS__)

void sink_info_list_callback(pa_context *c, const pa_sink_info *i, int eol, void *userdata)
{
  PRINTF("%s\n", __func__);
  if(eol)
  {
    return;
  }

  PRINTF("sink %d name : %s\n", i->index, i->name);
  PRINTF("num ports %d\n", i->n_ports);
}

void connection_callback(pa_context *c, void *userdata)
{
  pa_context_state_t state = pa_context_get_state(c);

  PRINTF("%s\n", __func__);

  switch(state)
  {
    case PA_CONTEXT_UNCONNECTED:
      PRINTF("Unconnected\n");
      break;
    case PA_CONTEXT_CONNECTING:
      PRINTF("Connecting\n");
      break;
    case PA_CONTEXT_READY:
      PRINTF("Ready\n");
      pa_operation *state = pa_context_get_sink_info_list(c, sink_info_list_callback, userdata); /* should be spawned by the connection state callback */
      break;
    case PA_CONTEXT_TERMINATED:
      PRINTF("Terminated\n");
      break;
    default:
      PRINTF("Unimplemented\n");
      break;
  }
}

//pa_operation_get_state()
//pa_operation_cancel()

//pa_context_connect()
//pa_context_set_state_callback() <--
int main()
{
  PRINTF("henlo\n");

  pa_mainloop *mainloop = pa_mainloop_new();
  char *servername = NULL;
  pa_proplist *proplist = pa_proplist_new();
  pa_proplist_sets(proplist, PA_PROP_APPLICATION_NAME, "app name");

  pa_context *context = pa_context_new_with_proplist(pa_mainloop_get_api(mainloop), servername, proplist);
  pa_proplist_free(proplist);

  const pa_spawn_api *spawn_api = NULL; /* parameters on how to spawn a thread */

  enum pa_context_state state = PA_CONTEXT_CONNECTING;
  pa_context_set_state_callback(context, connection_callback, &state);

  /* connect */
  int error = pa_context_connect(context, servername, PA_CONTEXT_NOAUTOSPAWN, spawn_api);
  while(state != PA_CONTEXT_READY && state != PA_CONTEXT_FAILED)
  {
    pa_mainloop_iterate(mainloop, 1, NULL);
  }

  /* disconnect */
  pa_context_disconnect(context);
}
