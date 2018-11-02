#ifndef __URENO_NAPI_INTERFACE
#define __URENO_NAPI_INTERFACE

#include <v8.h>
#include <node.h>
#include <node_object_wrap.h>

using namespace v8;

class UrenoNAPI : public node::ObjectWrap {
    public:
        static void Init(v8::Isolate* i);
        static void NewInstance(const FunctionCallbackInfo<Value>& args);
        // static VBUS& bus_ref;

    private:
        explicit UrenoNAPI();
        ~UrenoNAPI();
        static Persistent<Function> constructor;

        static void New(const FunctionCallbackInfo<Value>& args);
        static void Use(const FunctionCallbackInfo<Value>& args);
};
#endif