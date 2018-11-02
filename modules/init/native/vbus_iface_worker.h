#ifndef URENO_VBUS_IFACE_WORKER_H
#define URENO_VBUS_IFACE_WORKER_H
#include <node.h>
#include <uv.h>
#include <v8.h>
#include <vector>

#include "vbus.h"

using namespace v8;
struct VBUSWork {
    uv_work_t request;
    Persistent<Function> callback;
    VBUS::value id;
    VBUS::value ptr;
    VBUS::value iptr;
    FunctionCallbackInfo<Value>* args;
    Isolate* i;
    Local<Value> val;

    VBUS::IM_IStream* is;
    VBUS::IM_IStream* os;
};


#endif