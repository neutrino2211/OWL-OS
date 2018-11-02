#include "iostream"
#include "../../native/library.h"
#include "./launch_test.h"
#include <chrono>
#include <stdio.h>
#include <thread>
#include "../../native/vbus.h"
#include "../../native/definitions.h"

using namespace std;
void LaunchTest::init(VBUS& b,int id){
    // b.Set(0x05,id,false);
    // map_space_cell cell;
    // cell.x[0] = id;
    // cell.x[1] = 0xa41;
    // this_thread::sleep_for(chrono::milliseconds(100));
    // b.Write(cell,id);
    // for (int i = 1; i < 20; i++) {
    //     cout << "Launch Test : " << i << endl;
    //     this_thread::sleep_for(chrono::milliseconds(300));
    // }
    b.SetModuleStatus(id,Definitions::STATUS_OK);
    for(;;){
        Tick(b,id);
    }
}

void LaunchTest::Tick(VBUS& b,int id){
    cout << "Tick " << endl;
    b.SetModuleStatus(Definitions::STATUS_OK,id);
    VBUS::IM_IStream* is = b.connect(id);
    int mid,ptr,isPtr;
    b.SetModuleStatus(Definitions::STATUS_BUSY,id);
    *is >> mid;
    printf("mid %i ", mid);
    *is >> ptr;
    printf("ptr %i ", ptr);
    *is >> isPtr;
    printf("isPtr %i\n",isPtr);
    printf("LT recieved %i - %i - %i\n",mid,ptr,isPtr);
    printf("Printing message\n");
    vector<int> m = b.Get(ptr,mid);
    for(int i=0; i < (int) m.size(); i++){
        cout << static_cast<char>(m.at(i));
    }

    cout << endl;
    int i = 1;
    VBUS::IM_IStream* os = b.connect(mid);
    *os << id;
    *os << ptr;
    *os << i;
}

extern "C" Library* create_object(){
    return new LaunchTest();
}

extern "C" void destroy_object(Library* object){
    delete object;
}