#ifndef TESTLIB_H
#define TESTLIB_H
#include "../../native/library.h"
#include "../../native/lib_data.h"
#include "../../native/vbus.h"

class LaunchTest : public Library
{
 public:
    void init(VBUS&,int);
    void Tick(VBUS&,int);
};

#endif