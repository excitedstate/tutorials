#include <pybind11/pybind11.h>
#include <vector>

namespace py = pybind11;

// C++类：矩阵运算
class MatrixOperations {
public:
    // 矩阵乘法
    std::vector<std::vector<double>> multiply(const std::vector<std::vector<double>>& a, 
                                             const std::vector<std::vector<double>>& b) {
        size_t m = a.size();
        size_t n = b[0].size();
        size_t p = b.size();
        
        // 初始化结果矩阵
        std::vector<std::vector<double>> result(m, std::vector<double>(n, 0.0));
        
        // 矩阵乘法
        for (size_t i = 0; i < m; ++i) {
            for (size_t j = 0; j < n; ++j) {
                for (size_t k = 0; k < p; ++k) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        
        return result;
    }
    
    // 斐波那契数列（迭代）
    long long fibonacci(long long n) {
        if (n <= 1) {
            return n;
        }
        long long a = 0, b = 1, temp;
        for (long long i = 2; i <= n; ++i) {
            temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }
    
    // 快速排序
    void quick_sort(std::vector<double>& arr) {
        quick_sort_impl(arr, 0, arr.size() - 1);
    }
    
private:
    void quick_sort_impl(std::vector<double>& arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quick_sort_impl(arr, low, pi - 1);
            quick_sort_impl(arr, pi + 1, high);
        }
    }
    
    int partition(std::vector<double>& arr, int low, int high) {
        double pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; ++j) {
            if (arr[j] <= pivot) {
                i++;
                std::swap(arr[i], arr[j]);
            }
        }
        std::swap(arr[i + 1], arr[high]);
        return i + 1;
    }
};

// 导出C++函数和类到Python
PYBIND11_MODULE(matrix_cpp, m) {
    m.doc() = "Matrix operations module written in C++";
    
    // 导出类
    py::class_<MatrixOperations>(m, "MatrixOperations")
        .def(py::init<>())
        .def("multiply", &MatrixOperations::multiply, "Multiply two matrices")
        .def("fibonacci", &MatrixOperations::fibonacci, "Calculate fibonacci number iteratively")
        .def("quick_sort", &MatrixOperations::quick_sort, "Sort a list using quick sort");
    
    // 导出独立函数
    m.def("fibonacci", [](long long n) {
        MatrixOperations mo;
        return mo.fibonacci(n);
    }, "Calculate fibonacci number");
}