#include <Python.h>

static PyObject* hello_world(PyObject* self, PyObject* args){
    printf("Hello world\n");
    return Py_None;
}


// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition 
static PyMethodDef OWL_API_Methods[] = {
    { "helloworld", hello_world, METH_NOARGS, "Prints Hello World" },
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