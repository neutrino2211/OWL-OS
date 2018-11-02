#ifndef _URENO_LIBRARY_
#define _URENO_LIBRARY_

#include <dlfcn.h>
#include <iostream>
#include <stdio.h>
#include <strings.h>
#include "vbus.h"



using namespace std;

struct Library {
    public:
        virtual ~Library() = default;

        virtual void init(VBUS&,int)=0;
};

struct ControlData{
    vector<int> data;
    VBUS* bus;
    vector<int> result;
};

struct Module {
    public:
        virtual ~Module() = default;

        virtual void call(ControlData&)=0;
};

void lib_open(string name,VBUS& vbus,int id){
    string path = "/root/Desktop/Ureno/modules/init/firmware/"+name+"/build/"+name+".so";
    void* handle = dlopen(path.c_str(),RTLD_NOW);
    if(!handle){
        printf("Error : %s\n",dlerror());
    }
    Library* (*create)();
    void (*destroy)(Library*);

    create = (Library* (*)())dlsym(handle,"create_object");
    destroy = (void (*)(Library*))dlsym(handle,"destroy_object");

    if(!create){
        printf("Error : %s\n",dlerror());
    }

    if(!destroy){
        printf("Error : %s\n",dlerror());
    }

    Library* l = (Library*)create();
    l->init(vbus,id);
    destroy(l);
    return;
}

void module_load(string name, ControlData& cdata){
    // I* i = args.GetIsolate();
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
    string sub = name.substr(0,name.find_last_of("/"));
    // int len = sub.length();
    // printf("%s:%i\n",sub.c_str(),len);
    // printf("%i\n",name.find("?"));
    if(name.find("/") != -1){
        sub = name.substr(sub.length());
    }
    string path = "/root/Desktop/Ureno/modules/modules/"+name+"/build/"+sub+".so";
    void* handle = dlopen(path.c_str(),RTLD_NOW);
    if(!handle){
        printf("Error : %s\n",dlerror());
    }
    Module* (*create)();
    void (*destroy)(Module*);

    create = (Module* (*)())dlsym(handle,"create_object");
    destroy = (void (*)(Module*))dlsym(handle,"destroy_object");

    if(!create){
        printf("Error : %s\n",dlerror());
    }

    if(!destroy){
        printf("Error : %s\n",dlerror());
    }

    Module* l = (Module*)create();
    try{
        l->call(cdata);
    }catch(exception& ex){
        printf("Error from (%s) : %s\n",name,ex.what());
    }
    // args.GetReturnValue().Set(String::NewFromUtf8(i, v2s(cdata.result).c_str()));
    // destroy(l);
    return ;
}

#endif