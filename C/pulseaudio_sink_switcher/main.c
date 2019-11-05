#include <stdio.h>
#include <stdlib.h>

#include <pulse/context.h>
#include <pulse/mainloop.h>
#include <pulse/error.h>

void connection_callback(pa_context *c, void *userdata)
{
  pa_context_state_t state = pa_context_get_state(c);

  printf("%s\n", __func__);

  switch(state)
  {
    case PA_CONTEXT_UNCONNECTED:
      printf("Unconnected\n");
      break;
    case PA_CONTEXT_CONNECTING:
      printf("Connecting\n");
      break;
    case PA_CONTEXT_READY:
      printf("Ready\n");
      break;
    case PA_CONTEXT_TERMINATED:
      printf("Terminated\n");
      break;
    default:
      printf("Unimplemented\n");
      break;
  }
}

//pa_operation_get_state()
//pa_operation_cancel()

//pa_context_connect()
//pa_context_set_state_callback() <--
int main()
{
  printf("henlo\n");

  pa_mainloop *mainloop = pa_mainloop_new();
  char *servername = NULL;
  pa_proplist *proplist = pa_proplist_new();
  pa_proplist_sets(proplist, PA_PROP_APPLICATION_NAME, "app name");

  pa_context *context = pa_context_new_with_proplist(pa_mainloop_get_api(mainloop), servername, proplist);
  pa_proplist_free(proplist);

  const pa_spawn_api *spawn_api = NULL; /* parameters on how to spawn a thread */
  void *userdata = NULL;
  pa_context_set_state_callback(context, connection_callback, userdata);
  int error = pa_context_connect(context, servername, PA_CONTEXT_NOAUTOSPAWN, spawn_api);

  pa_context_disconnect(context);
}
