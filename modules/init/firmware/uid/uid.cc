#include "iostream"
#include "../../native/library.h"
#include "./uid.h"
#include <chrono>
#include <thread>
#include "../../native/vbus.h"
#include "../../native/definitions.h"

//Module essentials
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <array>
#include <fstream>

using namespace std;
vector<int> s2v(string message){
    vector<int> m = vector<int>();
    int sm = message.length();
    for(int i=0; i < sm ; i++ ){
        int in = static_cast<int>(message[i]);
        m.push_back(in);
    }
    return m;
}

string v2s(vector<char> v){
    string m = "";
    int vm = (int) v.size();
    for(int i=0; i < vm ; i++){
        char ch = static_cast<char>(v.at(i));
        m += ch;
    }
    return m;
}

string exec(const char* cmd){
    array<char, 128> buffer;
    string res;
    shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if(!pipe) return "\0";
    while(!feof(pipe.get())){
        if(fgets(buffer.data(),128,pipe.get()) != nullptr){
            res += buffer.data();
        }
    }
    return res;
}

void UID::init(VBUS& bus,int id){
    bus.SetModuleStatus(id,Definitions::STATUS_OK);
    VBUS::IM_IStream* is = bus.connect(id);
    ofstream file;
    ifstream ifile;
    // int ptr = bus.Set(s2v(exec("id")),id,false);
    for (;!bus.shutdown;) {
        // printf("UID\n");
        file.open("./runtime/uid/uid", ios::out | ofstream::binary);
        string v = exec("id");
        // for(int i = 0; i < (int) v.size(); i++){
        //     file << v.at(i) << "|";
        // }
        // printf("String = %s\n",v.c_str());
        file.write(v.c_str(), sizeof(v));
        file.close();
        ifile.open("./runtime/uid/uid", ios::in | ifstream::binary);
        char ch;
        if(!ifile.is_open()) printf("Error opening file\n");
        while(!ifile.eof()){
            ifile.get(ch);
        }
        ifile.close();
        this_thread::sleep_for(chrono::milliseconds(1000));

        // printf("Exiting\n");
    }
}
extern "C" Library* create_object(){
    return new UID();
}

extern "C" void destroy_object(Library* object){
    delete object;
}