#ifndef __URENO_VBUS_INTERFACE
#define __URENO_VBUS_INTERFACE

#include <v8.h>
#include "vbus.h"
#include <node.h>
#include <node_object_wrap.h>

using namespace v8;

class IVBUS : public node::ObjectWrap {
    public:
        static void Init(v8::Isolate* i);
        static void NewInstance(const FunctionCallbackInfo<Value>& args);
        // static VBUS& bus_ref;

    private:
        explicit IVBUS(VBUS&);
        ~IVBUS();
        static Persistent<Function> constructor;

        static void New(const FunctionCallbackInfo<Value>& args);
        static void Use(const FunctionCallbackInfo<Value>& args);
        static void Get(const FunctionCallbackInfo<Value>& args);
        static void Read(const FunctionCallbackInfo<Value>& args);
        static void Write(const FunctionCallbackInfo<Value>& args);
        static void GetModuleID(const FunctionCallbackInfo<Value>& args);
};
#endif