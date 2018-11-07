#ifndef _OWL_HW_H
#define _OWL_HW_H

#include <chrono>
#include <thread>
#include <sys/types.h>
#include <sys/sysinfo.h>

auto start_time = std::chrono::high_resolution_clock::now();
typedef std::chrono::duration<double, std::ratio<1,1>> seconds_t;


uint64_t get_cycles()
{
    unsigned int lo,hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

double age() 
{
    return seconds_t(std::chrono::high_resolution_clock::now() - start_time).count();
}

static inline void native_cpuid(unsigned int *eax, unsigned int *ebx,
                                unsigned int *ecx, unsigned int *edx)
{
        /* ecx is often an input as well as an output. */
        asm volatile("cpuid"
            : "=a" (*eax),
              "=b" (*ebx),
              "=c" (*ecx),
              "=d" (*edx)
            : "0" (*eax), "2" (*ecx));
}

static long cpu_clock_speed(){
    using namespace std::chrono_literals;
    int sleeptime = 100;
    uint64_t cycles_start = get_cycles();
    double time_start = age();
    std::this_thread::sleep_for(sleeptime * 1ms);
    uint64_t elapsed_cycles = get_cycles() - cycles_start;
    double elapsed_time = age() - time_start;
    return elapsed_cycles / elapsed_time;
}

static long long int total_ram(){
    struct sysinfo sysinf;
    sysinfo(&sysinf);
    long long r = sysinf.totalram;
    r *= sysinf.mem_unit;
    return r;
}
#endif