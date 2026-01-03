from setuptools import setup, Extension
from setuptools_rust import RustExtension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os

# 定义编译输出目录
LIBRARY_DIR = "lib"

# 确保输出目录存在
os.makedirs(LIBRARY_DIR, exist_ok=True)

# 定义C扩展模块
c_extension = Extension(
    'fib_c',  # 模块名
    sources=['c_extension/fib_c.c'],  # 源文件路径
    library_dirs=[LIBRARY_DIR],
)

# 定义C++扩展模块 - 暂时注释，待解决编译问题
# cpp_extension = Pybind11Extension(
#     'matrix_cpp',
#     sources=['cpp_extension/matrix_cpp.cpp'],
#     extra_compile_args=['-O3'],
#     library_dirs=[LIBRARY_DIR],
# )

# 定义Rust扩展模块
rust_extension = RustExtension(
    'fib_rust',  # Rust扩展模块名
    path='rust_extension/Cargo.toml',  # Cargo.toml路径
    # 移除重复的extension-module特性，因为已在Cargo.toml中配置
    features=['pyo3/extension-module'],  # 只需要pyo3的extension-module特性
    # 不使用rustc_flags，通过Cargo.toml配置release模式
)

# 所有扩展模块列表 - 只包含C扩展
extensions = [
    c_extension,
    # cpp_extension,  # 暂时注释
]

setup(
    name='python_concurrency_tutorial',
    version='0.1.0',
    description='Python concurrency tutorial with C/Rust extensions',
    author='Tutorial Author',
    author_email='author@example.com',
    url='https://github.com/example/python_concurrency_tutorial',
    packages=['src'],
    ext_modules=extensions,
    rust_extensions=[rust_extension],  # Rust扩展单独配置
    cmdclass={
        'build_ext': build_ext,
    },
    install_requires=[
        'pybind11>=2.10.0',
        'setuptools-rust>=1.5.0',
    ],
    setup_requires=[
        'setuptools>=40.8.0',
        'wheel>=0.36.0',
        'setuptools-rust>=1.5.0',
    ],
    python_requires='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Rust',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    # 设置扩展输出目录
    script_args=['build_ext', '--inplace'],
)
