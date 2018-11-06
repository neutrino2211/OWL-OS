#include <Python.h>

static PyObject* hello_world(PyObject* self, PyObject* args){
    printf("Hello world\n");
    return Py_None;
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

static PyObject* cpu_id(PyObject* self, PyObject* args){
    unsigned eax, ebx, ecx, edx;

    eax = 1; /* processor info and feature bits */
    native_cpuid(&eax, &ebx, &ecx, &edx);
    int model = (eax >> 4) & 0xF;
    int family = (eax >> 8) & 0xF;
    int stepping = eax & 0xF;
    int processor_type = (eax >> 12) & 0x3;
    int extended_model = (eax >> 16) & 0xF;
    int extended_family = (eax >> 20) & 0xFF;
    // printf("stepping %d\n", eax & 0xF);
    // printf("model %d\n", (eax >> 4) & 0xF);
    // printf("family %d\n", (eax >> 8) & 0xF);
    // printf("processor type %d\n", (eax >> 12) & 0x3);
    // printf("extended model %d\n", (eax >> 16) & 0xF);
    // printf("extended family %d\n", (eax >> 20) & 0xFF);

    /* EDIT */
    // eax = 3; /* processor serial number */
    // native_cpuid(&eax, &ebx, &ecx, &edx);

    /** see the CPUID Wikipedia article on which models return the serial 
         number in which registers. The example here is for 
        Pentium III */
    // printf("serial number 0x%08x%08x\n", edx, ecx);
    return Py_BuildValue("{s:i,s:i,s:i,s:i,s:i,s:i}",
        "stepping",stepping,
        "model", model,
        "family", family,
        "proc_type", processor_type,
        "ext_model", extended_model,
        "ext_family", extended_family
        );
}


// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition 
static PyMethodDef OWL_API_Methods[] = {
    { "helloworld", hello_world, METH_NOARGS, "Prints Hello World" },
    {"get_cpu_info", cpu_id, METH_NOARGS, "Gets cpu information"},
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef OWL_API_Module = {
    PyModuleDef_HEAD_INIT,
    "owlapi",
    "OWL-OS C++ API",
    -1,
    OWL_API_Methods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_owlapi(void)
{
    return PyModule_Create(&OWL_API_Module);
}