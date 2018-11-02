#include "iostream"
#include "../../native/library.h"
#include "./cpu_usage.h"
#include <chrono>
#include <thread>
#include <strings.h>
#include "../../native/vbus.h"
#include "../../native/definitions.h"

//Module essentials

#include "sys/types.h"
#include "sys/sysinfo.h"
#include "fstream"

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

int getRamUsage(){
    struct sysinfo meminfo;

    sysinfo (&meminfo);

    long long vmem = meminfo.totalram;
    vmem += meminfo.totalswap;
    vmem *= meminfo.mem_unit;

    long long totalvmem = meminfo.totalram;
    totalvmem *= meminfo.mem_unit;

    long long usedvmem = meminfo.totalram - meminfo.freeram;
    usedvmem *= meminfo.mem_unit;

    return (int) usedvmem; 
}

void CPU_USAGE::init(VBUS& bus,int id){
    // int ptr,isPtr=0,rid,rptr,riptr;
    ofstream file;
    // int i =0;
    for (;!bus.shutdown;) {
        // cout << "CPU-USAGE"<< endl;
        // vector<int> space = s2v(getRamUsage());
        this_thread::sleep_for(chrono::milliseconds(1000));
        int ru = getRamUsage();
        file.open("./runtime/cpu/usage",ofstream::binary);
        if(!file){
            // printf("Error opening cpu file\n");
        }
        // printf("%i = Shutdown\n");
        file.write(reinterpret_cast<char*>(&ru), sizeof(int));
        file.close();
        // printf("Exiting\n");
    }
}
extern "C" Library* create_object(){
    return new CPU_USAGE();
}

extern "C" void destroy_object(Library* object){
    delete object;
}