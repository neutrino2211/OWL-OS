#include "iostream"
#include "../../native/library.h"
#include "./test.h"
#include <chrono>
#include <thread>
#include "../../native/vbus.h"
#include "../../native/definitions.h"
#include "strings.h"

using namespace std;
void print(string message,int mid, int id, VBUS& bus, map_space_cell c){
    int stat = bus.ModuleStatus(mid);
    while(stat != Definitions::STATUS_OK){
        cout << "Not ready" << endl;
        // this_thread::sleep_for(chrono::milliseconds(500));
        stat = bus.ModuleStatus(mid);
    }
    cout <<  "Writing message" << endl ;
    // int r = bus.ReadWait(id);
    c.x[0] = mid;
    c.x[1] = Definitions::BYTE_TRANSER;
    bus.WriteMessage(c,mid);
    c.x[1] = Definitions::TRANSFER_BEGIN;
    this_thread::sleep_for(chrono::milliseconds(2000));
    // cout << "Test id " << mid << endl;
    // int _i = bus.ReadWait(mid);
    bus.Write(c,mid);
    c.x[1] = 0x1;
    bus.WriteMessage(c,mid);
    vector<int> m = vector<int>();
    // char message[] = "Hello this is the message";
    for(int i=0; i < (int) message.size(); i++ ){
        m.push_back(static_cast<int>(message[i]));
    }
    c.x[0] = bus.Set(m,id,false);
    c.x[1] = 0x1;
    cout << "Writing" << endl;
    bus.WriteMessage(c,mid);
    c.x[1] = Definitions::OPERATION_COMPLETE;
    cout << "Wait OP_COMPLETE " << endl;
    int _m;
    try{
        _m = bus.ReadWait(mid);
    } catch (std::error_code err){
        cout << err << endl;
    }
    cout << "Wait complete for " << mid <<  endl;
    this_thread::sleep_for(chrono::milliseconds(1000));
    cout << "Writing message to LT for " << mid << endl;
    // c.x[0] = mid;
    bus.Write(c,id);
    cout << mid << endl;
}
void Test::init(VBUS& bus,int id){
    int mid = bus.moduleBusID("launch_test");
    int stat = bus.ModuleStatus(mid);
    bus.SetModuleStatus(id,Definitions::STATUS_OK);
    // while(stat != Definitions::STATUS_OK){
    //     cout << "Not ready" << endl;
    //     this_thread::sleep_for(chrono::milliseconds(500));
    //     stat = bus.ModuleStatus(mid);
    // }
    // cout << stat << "s" << endl;
    map_space_cell c;
    // if(stat == Definitions::STATUS_OK){
        
    // }
    // print("This is the message",mid,id,bus,c);
    // while(stat != Definitions::STATUS_OK){
    //     cout << "Not ready" << endl;
    //     this_thread::sleep_for(chrono::milliseconds(500));
    //     stat = bus.ModuleStatus(mid);
    // }
    // print("This is the second message",mid,id,bus,c);
    VBUS::IM_IStream* os = bus.connect(mid); // Output stream to "Launch Test"
    VBUS::IM_IStream* is = bus.connect(id);  // Input stream for this Module
    vector<int> m = vector<int>();
    char message[] = "Hello this is the message";
    int sm = (sizeof message / sizeof *message);
    for(int i=0; i < sm ; i++ ){
        int in = static_cast<int>(message[i]);
        m.push_back(in);
    }
    int ptr = bus.Set(m,id,false);
    int isPtr = 1,rptr,risptr,rid;
    // this_thread::sleep_for(chrono::milliseconds(400));
    bus.waitFor(mid);
    *os << id;
    *os << ptr;
    *os << isPtr;
    bus.waitFor(mid);
    *is >> rid;
    *is >> rptr;
    *is >> risptr;
    if(rid == mid){
        vector<int> r = bus.Get(rptr,id);
        int int_stream = 0;
        for(int i = 0; i < r.size(); i++){
            int_stream += r.at(i);
        }
        printf("Result of operation = (%i) index=%i \n", int_stream,0);
    }
    for (int i = 101; i < 200; i++) {
        bus.SetModuleStatus(id,Definitions::STATUS_BUSY);
        cout << "Test : " << i << " " << mid << endl;
        // this_thread::sleep_for(chrono::milliseconds(1000));
        *is << id;
        *is << ptr;
        *is << isPtr;
        cout << "Exiting" << endl;
        bus.SetModuleStatus(id,Definitions::STATUS_OK);
    }
}
extern "C" Library* create_object(){
    return new Test();
}

extern "C" void destroy_object(Library* object){
    delete object;
}