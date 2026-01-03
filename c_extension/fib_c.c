#include <Python.h>

/* 递归计算斐波那契数列 */
long long fibonacci(long long n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2);
}

/* 迭代计算斐波那契数列 */
long long fibonacci_iter(long long n) {
    if (n <= 1) {
        return n;
    }
    long long a = 0, b = 1, temp;
    for (long long i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

/* Python调用的C函数 - 递归斐波那契 */
static PyObject* py_fibonacci(PyObject* self, PyObject* args) {
    long long n;
    if (!PyArg_ParseTuple(args, "L", &n)) {
        return NULL;
    }
    long long result = fibonacci(n);
    return PyLong_FromLongLong(result);
}

/* Python调用的C函数 - 迭代斐波那契 */
static PyObject* py_fibonacci_iter(PyObject* self, PyObject* args) {
    long long n;
    if (!PyArg_ParseTuple(args, "L", &n)) {
        return NULL;
    }
    long long result = fibonacci_iter(n);
    return PyLong_FromLongLong(result);
}

/* 模块方法定义 */
static PyMethodDef FibMethods[] = {
    {"fibonacci", py_fibonacci, METH_VARARGS, "Calculate fibonacci number recursively."},
    {"fibonacci_iter", py_fibonacci_iter, METH_VARARGS, "Calculate fibonacci number iteratively."},
    {NULL, NULL, 0, NULL}
};

/* 模块定义 */
static struct PyModuleDef fibmodule = {
    PyModuleDef_HEAD_INIT,
    "fib_c",
    "Fibonacci calculation module written in C",
    -1,
    FibMethods
};

/* 模块初始化函数 */
PyMODINIT_FUNC PyInit_fib_c(void) {
    return PyModule_Create(&fibmodule);
}