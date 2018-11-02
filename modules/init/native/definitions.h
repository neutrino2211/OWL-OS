#ifndef URENO_DEFINITIONS
#define URENO_DEFINITIONS

namespace Definitions {
    //---------TranferQueries-------
    //Tranferring buffers
    const int BYTE_TRANSER = 0x01;
    //Get status of module
    const int STATUS_QUERY = 0x02;
    //Response of status query
    const int STATUS_RESPONSE = 0x03;

    //---------StatusResponse--------
    const int STATUS_OK = 0x04;
    const int STATUS_BUSY = 0x05;
    const int STATUS_ERROR = 0x06;

    //---------TransferCodes---------
    const int TRANSFER_END = 0x07;
    const int TRANSFER_ERROR = 0x08;
    const int TRANSFER_BEGIN = 0x09;
    const int OPERATION_COMPLETE = 0xa;

    //---------Errors----------------
    const int ERROR_UNKNOWN = 0xb;

}

#endif