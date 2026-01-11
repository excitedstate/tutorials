use pyo3::prelude::*;

/// 递归计算斐波那契数列
fn fibonacci(n: u64) -> u64 {
    if n <= 1 {
        return n;
    }
    fibonacci(n - 1) + fibonacci(n - 2)
}

/// 迭代计算斐波那契数列
fn fibonacci_iter(n: u64) -> u64 {
    if n <= 1 {
        return n;
    }
    let mut a = 0;
    let mut b = 1;
    for _ in 2..=n {
        let temp = a + b;
        a = b;
        b = temp;
    }
    b
}

/// 快速排序算法
fn quick_sort(arr: &mut [f64]) {
    if arr.len() <= 1 {
        return;
    }
    let pivot = arr[arr.len() - 1];
    let mut i = 0;
    
    for j in 0..arr.len() - 1 {
        if arr[j] <= pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, arr.len() - 1);
    
    quick_sort(&mut arr[0..i]);
    quick_sort(&mut arr[i + 1..]);
}

/// Python模块定义
#[pymodule]
fn fib_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    /// 递归计算斐波那契数列
    #[pyfn(m)]
    fn fibonacci_py(_py: Python, n: u64) -> PyResult<u64> {
        Ok(fibonacci(n))
    }
    
    /// 迭代计算斐波那契数列
    #[pyfn(m)]
    fn fibonacci_iter_py(_py: Python, n: u64) -> PyResult<u64> {
        Ok(fibonacci_iter(n))
    }
    
    /// 快速排序算法
    #[pyfn(m)]
    fn quick_sort_py(_py: Python, mut arr: Vec<f64>) -> PyResult<Vec<f64>> {
        quick_sort(&mut arr);
        Ok(arr)
    }
    
    Ok(())
}