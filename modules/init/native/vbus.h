#ifndef URENO_VIRTUALBUS
#define URENO_VIRTUALBUS

#include <iostream>
#include <stdio.h>
#include <vector>
#include <array>
#include <thread>
#include <future>
#include <cstdlib>
#include "istream"
#include "definitions.h"


using namespace std;
typedef struct ram_space {public: int x[4];} ram_space;
typedef struct message_space {public: int x[2];} message_space;
typedef struct map_space_cell {public: int x[3];} map_space_cell;
class VBUS {
    public:

    VBUS(vector<string> mods){
        map_space[0] = "JS_Bridge";
        IM_IStream s(0);
        channels[0] = s;
        for(uint i = 0; i < mods.size(); i++){
            map_space[i+1] = mods[i];
            IM_IStream s(i+1);
            channels[i+1] = s;
        }
        // for(int i = 0; i < max_space; i++){
        //     message_channel.push_back(vector<int>());
        // }
    }

    bool shutdown = false;

    class value {
        public:
            value(){
                s[0] = 0;
                s[1] = 0;
                id = rand();
                printf("Plain initialization complete with s[0]=%i , s[1]=%i , id=%i\n",s[0],s[1],id);
            }
            value(int i,int j){
                s[0] = i;
                s[1] = j;
                id = rand();
            }

            int* v(){
                return s;
            }

            int data(){
                return s[1];
            }

            int callerID(){
                return s[0];
            }

            int dataID(){
                return id;
            }

            void printInfo(){
                printf("data=%i , stored_by=%i , id=%i\n", s[1],s[0],id);
            }
            int s[2];
        private:
            int id;
    };

    class IM_IStream {
        public:
        int data;
        int _id;
        bool read_lock = false;
        bool write_changed = false;
        vector<value> space = vector<value>();
        IM_IStream(int id){
            _id = id;
        }
        IM_IStream(uint id){
            _id = (int) id;
        }
        IM_IStream(){
            _id = 0;
        }
        // ~IM_IStream(){ delete[] &data; }
        

        IM_IStream& operator>>(value& j){
            is_reading = true;
            printf("Reading [%i] r=[%i]\n",j.data(),read_lock);
            int id = space[j.callerID()].dataID();
            // printf("Caller=%i, data\n",j.callerID());
            j.printInfo();
            // if(j.callerID() == -1){
            //     j.s[0] = 0;
            // }
            int _s = (int) space.size();
            if(j.callerID() >= _s){
                pad_vector(space,j.callerID()-_s);
            }
            bool message_exists = false;
            try{
                for(;;){
                    try{
                        id != space.at(j.callerID()).dataID();
                        message_exists = true;
                    }catch(std::exception& ex){
                        message_exists = false;
                    }
                    if((message_exists || already_written) && !data_read){
                        printf("Read called by (%i)\n",j.callerID());
                        value s = space.at(j.callerID());
                        // j.printInfo();
                        // s.printInfo();
                        j = s;
                        // j.printInfo();
                        already_written = false;
                        data_read = true;
                    }
                }
            } catch(exception& ex){
                printf("Error : (%s) with caller_id=%i\n",ex.what(),j.callerID());
            }
            printf("Read [%i]\n",j.data());
            is_reading = false;
            return *this;
        }

        IM_IStream& operator<<(value& i){
            printf("Writing [%i] r=[%i]\n",i.data(),read_lock);
            int _s = (int) space.size();
            if(i.callerID() >= _s){
                pad_vector(space,i.callerID()-_s);
            }
            space.assign(i.callerID(),i);
            i.printInfo();
            already_written = true;
            data_read = false;
            printf("Wrote [%i]\n",i.data());
            return *this;
        }

        private:
            bool is_reading = false;
            bool data_read = false;
            bool already_written = false;
            void pad_vector(vector<value>& v,int padding){
                printf("Pre-padding=%i\n",v.size());
                int i = 0;
                while(i <= padding){
                    value _v = value(-1,-1);
                    v.push_back(_v);
                    i++;
                }
                printf("Post-padding=%i\n",v.size());
            }
    };

    int Set (vector<int> value, int module_id, bool isPointer){
        if(stack.size() >= (uint) max_space){
            clearStack(stack);
        }

        int a = (int) stack.size();
        vector<int> r = {a};
        if(isPointer){
            // r = {a,value.,module_id,1};
            r.insert(r.end(),value.begin(),value.end());
            r.push_back(module_id);
            r.push_back(1);
            r.push_back((int) r.size());
        } else {
            // r = {a,value,module_id,0};
            r.insert(r.end(),value.begin(),value.end());
            r.push_back(module_id);
            r.push_back(1);
            r.push_back((int) r.size());
        }
        stack.push_back(r);
        printStack(stack);
        return a;
    }

    bool is_set(int address){
        // int len = (sizeof stack/ sizeof &stack);
        if(address < (int) stack.size()){
            return true;
        } else {
            return false;
        }
    }

    vector<int> Get (int address, int mid){
        printStack(stack);
        vector<int> i = stack.at(address);
        int pos = i.size() - 3;
        printf("SMID=%i , RMID=%i\n",stack.at(address).at(pos),mid);
        if(stack.at(address).at(pos) == mid){
            return stack.at(address);
        } else {
            vector<int> r = {0,0,0,2,0};
            return r;
        }
    }

    IM_IStream* connect(int mid){
        // waitFor(mid);
        return &channels[mid];
    }

    int moduleBusID(string name){
        printf("Getting id of (%s)\n",name.c_str());
        for(int i = 0; i < 30 /*(sizeof map_space/sizeof *map_space)*/; i++){
            // printf("cmp %s , %s\n",name.c_str(),map_space[i].c_str());
            if(map_space[i] == name){
                return i;
            }
        }

        return -1;
    }

    int OwnerOf(int addr){
        cout << "Get owner of " << addr << endl;
        vector<int> space = stack.at(addr);
        cout << "Got owner of " << addr << endl;
        return space[space.size()-3];
    }

    void Write(map_space_cell cell, int mid){
        map_space_cells.push_back(cell);
        // cout << "Bus (Write) : " << cell.x << " by " << mid << endl;
        last_write[mid] = cell.x[1];
    }

    void WriteMessage(map_space_cell c, int mid){
        cout << "Write " << mid << endl;
        message_channel[mid].x[0] = c.x[0];
        message_channel[mid].x[1] = c.x[1];
        message_channel[mid].x[2] = 0;
    }

    int ModuleStatus(int mid){
        return module_status[mid];
    }

    void SetModuleStatus(int mid, int s){
        module_status[mid] = s;
    }

    void waitFor(int id){
        int stat = ModuleStatus(id);
        for(;;){
            if(stat == Definitions::STATUS_OK){
                break;
            }
            stat = ModuleStatus(id);
        }
    }

    int Read(int mid){
        for(int i = 0; i < (int) map_space_cells.size(); i++){
            if(map_space_cells[i].x[0] == mid){
                return map_space_cells[i].x[1];
            }
        }
    }

    int ReadWait(int mid){
        // cout << "Bus (Read) :  for " << mid << endl;
        int cv = last_write[mid];
        for(;;){
            if(last_write[mid] != cv){
                return last_write[mid];
            }
        }
    }

    message_space ReadMessage(int mid){
        // cout << mid << " " << sizeof message_channel/sizeof *message_channel << endl;
        // message_space cv = message_channel[mid];
        // cout << "Read " << mid << "Which has " << cv.x[0] << endl;
        for(;;){
            if(message_channel[mid].x[2] != 1){
                cout << "Message read" << endl;
                message_channel[mid].x[2] = 1;
                return message_channel[mid];
            }
        }
    }

    vector<int> ReadAll(int mid){
        vector<int> data_arr = vector<int>();
        for(int i = 0; i < (int) map_space_cells.size(); i++){
            if(map_space_cells[i].x[0] == mid){
                data_arr.push_back(map_space_cells[i].x[1]);
            }
        }
        return data_arr;
    }

    // istream* channels[0xffff];

    private:
    const static int max_space = 0xffff;
    int curr_address = 0;
    int last_write[max_space];
    string map_space[max_space];
    int module_status[max_space];
    IM_IStream channels[max_space];
    vector<vector<int>> stack = vector<vector<int>>();
    message_space message_channel[max_space];
    vector<map_space_cell> map_space_cells  = vector<map_space_cell>();
    void printStack(vector<vector<int>> stack){
        cout << "Stack " << stack.size() << endl;
        for(uint i = 0; i < stack.size(); i++){
            cout << "--- " << stack[i][0] << " " << stack[i][1] << endl;
        }
    }

    void clearStack(vector<vector<int>>& stack){
        vector<vector<int>>().swap(stack);
        curr_address = 0;
        cout << "Stack limit exceeded and is now cleared" << endl;
    }
};

// class IM_IStream {
//         public:
//         IM_IStream(int id){
//             _id = id;
//         }

//         IM_IStream(){
//             _id = 0;
//         }

//         string identity(){
//             return "ISTREAM: " + (char) _id;
//         }

//         void waitRead(int& j){
//             for(;;){
//                 if(curr_read == 0){
//                     curr_write = j;
//                     curr_write_modified = 1;
//                     curr_read = 1;
//                     break;
//                 }
//             }
//         }

//         void waitWrite(int& _i){
//             for(;;){
//                 // if((++counter%count) == 0) cout << cwm() << endl; 
//                 if(cwm() == 1){
//                     _i = cw();
//                     curr_write_modified = 0;
//                     curr_read = 0;
//                     break;
//                 }
//             }
//         }

//         IM_IStream& operator>>(int& _i){
//             // int  count = 200000000;
//             // int counter = 0;
//             // thread th(waitWrite,_i);
//             // th.join();
//             thread f([&_i,this]{
//                 for(;;){
//                     // if((++counter%count) == 0) cout << cwm() << endl; 
//                     if(curr_write_modified == 1){
//                         _i = curr_write;
//                         printf("Reading [%i] for [%i]\n",curr_write,_id);
//                         curr_write_modified = 0;
//                         curr_read_modified = 0;
//                         break;
//                     }
//                 }
//                 printf("Read [%i]\n",_id);
//             });
//             f.join();
//             // for(;;){
//             //     // if((++counter%count) == 0) cout << cwm() << endl; 
//             //     if(curr_write_modified == 1){
//             //         _i = curr_write;
//             //         printf("Reading [%i] for [%i]\n",curr_write,_id);
//             //         curr_write_modified = 0;
//             //         curr_read_modified = 0;
//             //         break;
//             //     }
//             // }
//             printf("Init read [%i]\n",_id);
//             // Work* w = new Work();
//             // w->request.data = w;
//             // uv_queue_work(uv_default_loop(),&w->request,[]);
//             return *this;
//         }

//         IM_IStream& operator<<(int& j){
//             thread t([&j,this]{
//                 for(;;){
//                     if(curr_read_modified == 0){
//                         curr_write = j;
//                         printf("Writing [%i] for [%i]\n",curr_write,_id);
//                         curr_write_modified = 1;
//                         curr_read_modified = 1;
//                         break;
//                     }
//                 }
//                 printf("Wrote [%i]\n",_id);
//             });
//             t.join();
//             // for(;;){
//             //     if(curr_read_modified == 0){
//             //         curr_write = j;
//             //         printf("Writing [%i] for [%i]\n",curr_write,_id);
//             //         curr_write_modified = 1;
//             //         curr_read_modified = 1;
//             //         break;
//             //     }
//             // }
//             printf("Init write [%i]\n",_id);
//             return *this;
//         }
        

//         private:
//         int _id;
//         int curr_read = 0;
//         int curr_read_modified = 0;

//         int cw(){
//             return curr_write;
//         }

//         int cwm(){
//             return curr_write_modified;
//         }

//         int curr_write = 0;
//         int curr_write_modified = 0;
//     };

#endif