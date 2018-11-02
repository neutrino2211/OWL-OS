// #include <v8.h>
#include <node.h>
#include <nan.h>
#include <iostream>
#include <strings.h>
#include <future>
#include <cstdlib>
#include <iostream>
#include <thread>
#include "library.h"
#include "vbus.h"
// #include "UrenoNAPI.h"
#include "./vbus_iface.h"
#include "./vbus_iface_worker.h"
// #include "uv.h"
// #include <dlfcn.h>
// #include <iostream>
// #include <stdio.h>
// #include <strings.h>
// #include <dlfcn.h>
#include <vector>
#include <signal.h>
#include <unistd.h>

#define V8Args v8::FunctionCallbackInfo<v8::Value>
#define I v8::Isolate

using namespace v8;
using namespace std;

namespace init {
    using v8::FunctionCallbackInfo;
    using v8::Isolate;
    using v8::Local;
    using v8::Object;
    using v8::String;
    using v8::Number;
    using v8::Value;

    struct INITWork {
        uv_work_t request;
        vector<string> mods;
    };

    vector<string> mods = {"uid","cpu_usage"};
    VBUS bus = VBUS(mods);
    //JS Interface helper functions

    vector<int> s2v(string message){
        vector<int> m = vector<int>();
        int sm = message.length();
        for(int i=0; i < sm ; i++ ){
            int in = static_cast<int>(message[i]);
            m.push_back(in);
        }
        return m;
    }

    string v2s(vector<int> v){
        string m = "";
        int vm = (int) v.size();
        for(int i=0; i < vm ; i++){
            char ch = static_cast<char>(v.at(i));
            m += ch;
        }
        return m;
    }

    static void _iv_perform_read(uv_work_t* req){
        VBUSWork* w = static_cast<VBUSWork*>(req->data);
        // cout << i->identity() << endl;
        // w->id;
        // w->ptr;
        // w->iptr;
        int id = 0;
        int p = 0;
        int iptr = 0;
        cout << "Reading (js)" << endl;
        *w->is >> w->id;
        *w->is >> w->ptr;
        *w->is >> w->iptr;
        cout << "Done (js)" << endl;

        // w->id = id;
        // w->ptr = p;
        // w->iptr = iptr;

        // cout << id << p << iptr << endl;
    }

    static void _iv_op_complete(uv_work_t* r, int stat){
        cout << stat << " OPC" << endl;
        Isolate* i = Isolate::GetCurrent();
        HandleScope hs(i);
        VBUSWork* w = static_cast<VBUSWork*>(r->data);
        // if(w->callback.IsFunction()){
        //     cout << "Function" << endl;
        // } else {
        //     cout << "Not function" << endl;
        // }
        // Handle<Function> cb = Handle<Function>::Cast(w->callback);
        V8Args fv = *w->args;
        auto f = fv[1];
        // Local<Function>& cb = w->callback;
        int id = w->id.data();
        // int& mptr = w->ptr;
        // int& iptr = w->iptr;
        printf("Setting js arguments\n");
        const int argc = 3;
        Local<Value> argv[argc];
        argv[0] = Number::New(i,w->id.data());
        argv[1] = Number::New(i,w->ptr.data());
        argv[2] = Number::New(i,w->iptr.data());
        cout << "Almost done " << endl;
        // cout << << endl;
        
        // cb->Reset();
        // delete w;
        // try{
        //     // cout << sizeof cb->Call << endl;
        //     // Local<Function>::New(w->i,cb)->Call(w->i->GetCurrentContext()->Global(),2, argv);
        //     cout << "Exit tcb" << endl;
        //     // if(f.IsFunction()){
        //     //     cout << "Function" << endl;
        //     // } else {
        //     //     cout << "Not function" << endl;
        //     // }
        // }catch(exception& ex){
        //     cout << ex.what() << endl;
        // }
        cout << "Exit tcb" << endl;
        Local<Function>::New(Isolate::GetCurrent(),w->callback)->Call(f,argc,argv);
        cout << "Post call" << endl;
        // cout << id << " - " << w->ptr << " - " << w->iptr << endl;
        // cout << *w->callback << endl;
        // w->args->GetReturnValue().Set(&i,Undefined(&i));
        // args.GetReturnValue().Set(i,Undefined(i));
    }

    //JS Interface
    //---------------------------------------------------------------------------



    Persistent<Function> IVBUS::constructor;
    IVBUS::IVBUS(VBUS& bus){
        // bus_ref = bus;
        cout << "Vbus init" << endl;
    };

    IVBUS::~IVBUS(){};

    void IVBUS::Init(Isolate* i){
        Local<FunctionTemplate> tpl = FunctionTemplate::New(i, New);
        tpl->SetClassName(String::NewFromUtf8(i,"IVBUS"));
        tpl->InstanceTemplate()->SetInternalFieldCount(1);

        NODE_SET_PROTOTYPE_METHOD(tpl,"read",Read);
        NODE_SET_PROTOTYPE_METHOD(tpl,"write",Write);
        NODE_SET_PROTOTYPE_METHOD(tpl,"get",Get);
        NODE_SET_PROTOTYPE_METHOD(tpl,"syscall",Use);
        NODE_SET_PROTOTYPE_METHOD(tpl,"getModuleId",GetModuleID);

        constructor.Reset(i,tpl->GetFunction());
    }

    void IVBUS::New(const FunctionCallbackInfo<Value>& args){
        v8::Isolate* i = args.GetIsolate();

        if(args.IsConstructCall()){
            IVBUS* ivbus = new IVBUS(init::bus);
            ivbus->Wrap(args.This());
            args.GetReturnValue().Set(args.This());
        } else {
            Local<Value> argv[1] =  {args[0]};
            Local<Function> cons = Local<Function>::New(i,constructor);
            Local<Context> c = i->GetCurrentContext();
            Local<Object> inst = cons->NewInstance(c,1,argv).ToLocalChecked();
            args.GetReturnValue().Set(inst);
        }
    }

    void IVBUS::NewInstance(const FunctionCallbackInfo<Value>& args){
        v8::Isolate* i = args.GetIsolate();
        Local<Value> argv[1] =  {args[0]};
        Local<Function> cons = Local<Function>::New(i,constructor);
        Local<Context> c = i->GetCurrentContext();
        Local<Object> inst = cons->NewInstance(c,1,argv).ToLocalChecked();
        args.GetReturnValue().Set(inst);
    }

    void IVBUS::GetModuleID(const V8Args& args){
        I* i = args.GetIsolate();
        String::Utf8Value s(args[0]);
        string str(*s);
        // reverse(str.begin(),str.end());
        printf("Callback string (%s)",str.c_str());
        // string id = args[0]->IsUndefined() ? "" : str.c_str();
        args.GetReturnValue().Set(Number::New(i,init::bus.moduleBusID(str)));
    }

    void IVBUS::Get(const V8Args& args){
        I* is = args.GetIsolate();

        if(args[0]->IsNumber() && args[1]->IsNumber()){
            double i = args[0]->NumberValue();
            double j = args[1]->NumberValue();
            vector<int> space = init::bus.Get(i,j);
            cout << "Got memory space " << space.size() << endl;
            int s = (int) space.size();
            v8::Handle<v8::Array> arr = Array::New(is);
            printf("Initialised array\n");
            for(int k=1;k<s-3;k++){
                arr->Set(k,Number::New(is,space.at(k)));
            }
            printf("Finished setting array\n");
            args.GetReturnValue().Set(arr);
            printf("Returned\n");
        } else {
            args.GetReturnValue().Set(Array::New(0));
        }
    }

    void IVBUS::Write(const V8Args& args){
        I* i = args.GetIsolate();
        if(args[0]->IsNumber() && args[1]->IsNumber()){
            double i = args[0]->NumberValue();
            double j = args[1]->NumberValue();
            int defJSid = 0;
            int ip = 0;
            int k = (int) j;
            VBUS::IM_IStream* s = init::bus.connect((int)i);
            VBUS::value vbus_defjs(defJSid,defJSid);
            VBUS::value vbus_k(defJSid,k);
            VBUS::value vbus_ip(defJSid,ip);
            *s >> vbus_defjs;
            *s >> vbus_k;
            *s >> vbus_ip;
        }
    }

    void IVBUS::Use(const V8Args& args){
        I* i = args.GetIsolate();
        if(!args[0]->IsString()||!args[1]->IsString()){
            args.GetReturnValue().Set(Undefined(i));
            return;
        }
        String::Utf8Value s(args[0]);
        string name(*s);
        String::Utf8Value s2(args[1]);
        string data(*s2);
        ControlData cdata;
        cdata.data = init::s2v(data);
        cdata.bus = &init::bus;
        module_load(name,cdata);
        args.GetReturnValue().Set(String::NewFromUtf8(i,init::v2s(cdata.result).c_str()));
    }

    void IVBUS::Read(const V8Args& args){
        I* i = args.GetIsolate();
        // String::Utf8Value s(args[0]->ToString());
        // string ss(*s);
        // string mode = args[1]->IsUndefined() ? "" : ss;
        args.GetReturnValue().Set(Number::New(i,0));
        int id = (int) args[0]->NumberValue();
        HandleScope hs(i);
        int mid=0,mptr=0,iptr=0;
        const uint argc = 3;
        Local<Value> argv[argc];
        Local<Function> cb = Local<Function>::New(i,args[1]);
        // init::bus.waitFor((int) id);
        VBUS::IM_IStream* is = init::bus.connect(id);
        cout << "ID " << id << ";" << endl; 
        // *is >> mid;
        // *is >> mptr;
        // *is >> iptr;
        VBUS::value vbus_id;
        VBUS::value data_pointer;
        VBUS::value is_ptr;
        VBUSWork* w = new VBUSWork();
        w->callback.Reset(i,cb);
        w->i = i;
        printf("Assign vbus_id\n");
        w->id = vbus_id;
        printf("Assign data_pointer\n");
        w->ptr = data_pointer;
        w->args = &args;
        printf("Assign is_ptr\n");
        w->iptr = is_ptr;
        w->is = is;
        w->val = args[1];
        w->request.data = w;
        uv_queue_work(uv_default_loop(),&w->request,init::_iv_perform_read,init::_iv_op_complete);

        // argv[0] = Number::New(i,id);
        // argv[1] = Number::New(i,mptr);
        // argv[2] = Number::New(i,iptr);
        // cb->Call(Null(i),argc,argv);
        // args.GetReturnValue().Set(i,Undefined(i));
    }



    //-----------------------------------------------

    // Persistent<Function> UrenoNAPI::constructor;
    // UrenoNAPI::UrenoNAPI(){};

    // UrenoNAPI::~UrenoNAPI(){};

    // void UrenoNAPI::Init(Isolate* i){
    //     Local<FunctionTemplate> tpl = FunctionTemplate::New(i, New);
    //     tpl->SetClassName(String::NewFromUtf8(i,"UrenoNAPI"));
    //     tpl->InstanceTemplate()->SetInternalFieldCount(1);

    //     NODE_SET_PROTOTYPE_METHOD(tpl,"use",Use);

    //     constructor.Reset(i,tpl->GetFunction());
    // }

    // void UrenoNAPI::New(const FunctionCallbackInfo<Value>& args){
    //     v8::Isolate* i = args.GetIsolate();

    //     if(args.IsConstructCall()){
    //         UrenoNAPI* urenoNAPI = new UrenoNAPI();
    //         urenoNAPI->Wrap(args.This());
    //         args.GetReturnValue().Set(args.This());
    //     } else {
    //         Local<Value> argv[1] =  {args[0]};
    //         Local<Function> cons = Local<Function>::New(i,constructor);
    //         Local<Context> c = i->GetCurrentContext();
    //         Local<Object> inst = cons->NewInstance(c,1,argv).ToLocalChecked();
    //         args.GetReturnValue().Set(inst);
    //     }
    // }

    // void UrenoNAPI::NewInstance(const FunctionCallbackInfo<Value>& args){
    //     v8::Isolate* i = args.GetIsolate();
    //     Local<Value> argv[1] =  {args[0]};
    //     Local<Function> cons = Local<Function>::New(i,constructor);
    //     Local<Context> c = i->GetCurrentContext();
    //     Local<Object> inst = cons->NewInstance(c,1,argv).ToLocalChecked();
    //     args.GetReturnValue().Set(inst);
    // }

    // void UrenoNAPI::Use(const V8Args& args){
    //     I* i = args.GetIsolate();
    //     if(!args[0]->IsString()||!args[1]->IsString()){
    //         args.GetReturnValue().Set(Undefined(i));
    //         return;
    //     }
    //     String::Utf8Value s(args[0]);
    //     string name(*s);
    //     String::Utf8Value s2(args[1]);
    //     string data(*s2);
    //     ControlData cdata;
    //     cdata.data = init::s2v(data);
    //     module_load(name,cdata);
    //     args.GetReturnValue().Set(String::NewFromUtf8(i,init::v2s(cdata.result).c_str()));
    // }

    // Thread launch
    void _print(string h){
        cout << h << endl;
    }
    void _thread (int i){
        lib_open(mods[i],bus,i+1);
    }
    void Hello (const FunctionCallbackInfo<Value>& args) {
        args.GetReturnValue().Set(String::NewFromUtf8(args.GetIsolate(),"Hello from C++"));
    }

    void shutdown(int s){
        printf("Recieved signal [%d]\n",s);
        bus.shutdown = true;
        for(int i=0;i < 10000000000000000; i++){}
    }

    void thread_done(uv_work_t* r,int done){
        cout << "Done" << endl;
    }
    void thread_helper(uv_work_t* req){
        int i = mods.size();
        int j = 0;
        thread ths[i];
        // while(j < i){
        //     thread th(_thread,j);
        //     th.join();
        //     cout << "Firmware >> Loading " << mods[j] << endl;
        //     j++;
        // }
        for(int k = 0; k < i; k++){
            ths[k] = thread(_thread,k);
        }
        cout << "End Main" << endl ;
        struct sigaction sigIntHandler;

        sigIntHandler.sa_handler = shutdown;
        sigemptyset(&sigIntHandler.sa_mask);
        sigIntHandler.sa_flags = 0;

        sigaction(SIGINT, &sigIntHandler, NULL);
        for(j = 0 ; j < i; j++){
            ths[j].join();
        }
        pause();
    }

    void new_thread (const V8Args& args){
        // int i(args[0]->NumberValue());
        INITWork* w = new INITWork();
        // w->mods = mods;
        w->request.data = w;
        uv_queue_work(uv_default_loop(),&w->request,thread_helper,thread_done);
    }

    void t(const FunctionCallbackInfo<Value>& args){
        thread f = thread(new_thread,args);
        f.join();
    }

    // Module initialization logic
    void init(Local<Object> exports){
        IVBUS::Init(exports->GetIsolate());
        // new_thread();
        NODE_SET_METHOD(exports,"Bus",IVBUS::NewInstance);
        // NODE_SET_METHOD(exports,"Ureno",UrenoNAPI::NewInstance);
        NODE_SET_METHOD(exports,"Hello",Hello);
        NODE_SET_METHOD(exports,"new_thread",new_thread);
    }
    NODE_MODULE(NODE_GYP_MODULE_NAME,init);
}

