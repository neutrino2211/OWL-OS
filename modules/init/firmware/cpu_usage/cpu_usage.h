#ifndef TESTLIB_H
#define TESTLIB_H
#include "../../native/library.h"
#include "../../native/lib_data.h"
#include "../../native/vbus.h"

class CPU_USAGE : public Library
{
 public:
    void init(VBUS&,int);
};

#endif