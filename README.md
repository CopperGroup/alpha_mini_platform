# Lab work 1: Creating library for working with strings using C++
Authors (team): 
- Dziuba Oksana - [GitHub](https://github.com/Dandaizyer)
- Yelizaveta Piletska - [GitHub](https://github.com/lizapiletska)
- Solchanyk Vasyl - [GitHub](https://github.com/PapaJonas)


Variant: Common (There are no more options)
## Prerequisites

To build and run the project, you need:
- **GCC** (g++ 9.0+ recommended) or another C++17 compatible compiler
- **CMake** (version 3.10 or higher)
- **Make** (or another build system supported by CMake)
- **Bash** (for running `run_tests.sh`)

### Structure of progect

```
├── demo
│   └── main.cpp
├── include
│   └── mystring.hpp
├── src
│   └── mystring.cpp
├── tests
│   ├── run_tests.sh
│   └── testing
│       ├── mystring.cpp
│       └── mystring.hpp
└── README.md
```

### Compilation

To compile and run tests, use:

1. Create and enter the build directory
```bash
mkdir build
cd build
```
2. Generate build files via Make
```bash
cmake ..
```
3. Build the project
```bash
make
```

### Installation

No additional installation required.


### Usage

Run demo program:
```bash
./demo/demo_prog
```
Run tests:
```bash
./tests/run_tests.sh
```
### Important!

All scripts are written for Linux / macOS (Bash).

On Windows use WSL or MinGW.

Known issues: limited set of string operations compared to std::string.

### Realization
- Class my_str_t:
  - header of this class is mysrting.hpp
  - There are key methods of string that have released:
```cpp
#ifndef MY_STRING_HPP 
#define MY_STRING_HPP 
#include <cstddef> 
#include <stdexcept> 
#include <string> 
#include <iostream> 
 
class my_str_t { 
private: 
    char* data_m; 
    size_t capacity_m; 
    size_t size_m; 
public: 
    my_str_t(); 
    my_str_t(size_t size, char initial); 
    my_str_t(const char* cstr); 
    my_str_t(const std::string& str); 
    my_str_t(const my_str_t& other); 
    my_str_t(my_str_t&& other) noexcept; 
    my_str_t& operator=(const my_str_t& other); 
    my_str_t& operator=(my_str_t&& other) noexcept; 
    ~my_str_t(); 
    char& operator[](size_t idx); 
    const char& operator[](size_t idx) const; 
    char& at(size_t idx); 
    const char& at(size_t idx) const; 
    size_t size() const noexcept; 
    size_t capacity() const noexcept; 
    void reserve(size_t new_capacity); 
    void shrink_to_fit(); 
    void clear(); 
    void resize(size_t new_size, char new_char = ' '); 
    void append(const my_str_t& str); 
    void append(char c); 
    void append(const char* cstr); 
    void insert(size_t idx, const my_str_t& str); 
    void insert(size_t idx, char c); 
    void insert(size_t idx, const char* cstr); 
    void erase(size_t begin, size_t count); 
    void swap(my_str_t& other) noexcept; 
    const char* c_str() const; 
    static constexpr size_t not_found = static_cast<size_t>(-1); 
    size_t find(char c, size_t idx = 0); 
    size_t find(const char* cstr, size_t idx = 0); 
    size_t find(const std::string& str, size_t idx = 0); 
    my_str_t substr(size_t begin, size_t count); 
    bool operator==(const my_str_t& rhs) const; 
    bool operator!=(const my_str_t& rhs) const; 
    bool operator<(const my_str_t& rhs) const; 
    bool operator<=(const my_str_t& rhs) const; 
    bool operator>(const my_str_t& rhs) const; 
    bool operator>=(const my_str_t& rhs) const; 
    my_str_t operator+(const my_str_t& rhs) const; 
    my_str_t operator+(const char* rhs) const; 
    my_str_t& operator+=(const my_str_t& rhs); 
    my_str_t& operator+=(const char* rhs); 
    my_str_t& operator+=(char rhs); 
    my_str_t operator*(size_t times) const; 
    my_str_t& operator*=(size_t times); 
}; 
#endif // MY_STRING_HPP 
```

### Results

- Implemented custom string class my_str_t with constructors, assignment, concatenation, and basic operations.

- Learned how to:

    - Work with dynamic memory in C++.

    - Organize code into a library with headers and source files.

    - Use CMake and Bash for project automation.

- Interesting finding: even simple string handling requires careful memory management.

# Additional tasks
- 2.8.1:
  - конструктор переміщення та присвоєння із переміщенням,
  - оператори + та +=, які здійснюють конкатенацію,
  - оператори * та *=, які створюють кілька копій стрічки, аналогічно до відповідних операторів Python.
- 2.8.3:
    - Порівняти продуктивність цієї бібліотеки із стандартними стрі-
      чками C++

