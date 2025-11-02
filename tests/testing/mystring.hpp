#ifndef MY_STRING_HPP
#define MY_STRING_HPP
#include <cstddef>  // for size_t
#include <stdexcept> // for exceptions
#include <string>    // for std::string
#include <iostream>  // for I/O operators

class my_str_t {
private:
    char* data_m;        // Pointer to allocated memory
    size_t capacity_m;   // Size of allocated block
    size_t size_m;       // Actual string size

public:
    // Constructors (Author: Elyzaveta Piletska)
    my_str_t();                         // Default
    my_str_t(size_t size, char initial); // Fill with copies of a char
    my_str_t(const char* cstr);          // From C-string
    my_str_t(const std::string& str); // From std:string
    my_str_t(const my_str_t& other);     // Copy constructor
    my_str_t(my_str_t&& other) noexcept; // Move constructor

    // Assignment (Author: Elyzaveta Piletska)
    my_str_t& operator=(const my_str_t& other);
    my_str_t& operator=(my_str_t&& other) noexcept; // Move assignment

    // Destructor (Author: Elyzaveta Piletska)
    ~my_str_t();

    // Element access (Author: Elyzaveta Piletska)
    char& operator[](size_t idx);
    const char& operator[](size_t idx) const;

    char& at(size_t idx);
    const char& at(size_t idx) const;

    // Capacity management (Author: Elyzaveta Piletska)
    size_t size() const noexcept;
    size_t capacity() const noexcept;
    void reserve(size_t new_capacity);
    void shrink_to_fit();
    void clear();
    void resize(size_t new_size, char new_char = ' ');

    // Modifiers (Author: Elyzaveta Piletska)
    void append(const my_str_t& str);
    void append(char c);
    void append(const char* cstr);

    void insert(size_t idx, const my_str_t& str);
    void insert(size_t idx, char c);
    void insert(size_t idx, const char* cstr);

    void erase(size_t begin, size_t count);

    void swap(my_str_t& other) noexcept;

    // Utilities (Author: Elyzaveta Piletska)
    const char* c_str() const;

    static constexpr size_t not_found = static_cast<size_t>(-1);
    size_t find(char c, size_t idx = 0);
    size_t find(const char* cstr, size_t idx = 0);
    size_t find(const std::string& str, size_t idx = 0);

    my_str_t substr(size_t begin, size_t count);

    // Methods for I/O
    //void read_from_stream(std::istream& is);
    //void read_line_from_stream(std::istream& is);
    //void write_to_stream(std::ostream& os) const;

    // Comparison operators (Author: Elyzaveta Piletska)
    bool operator==(const my_str_t& rhs) const;
    bool operator!=(const my_str_t& rhs) const;
    bool operator<(const my_str_t& rhs) const;
    bool operator<=(const my_str_t& rhs) const;
    bool operator>(const my_str_t& rhs) const;
    bool operator>=(const my_str_t& rhs) const;

    bool operator==(const char* rhs) const;
    bool operator!=(const char* rhs) const;
    bool operator<(const char* rhs) const;
    bool operator<=(const char* rhs) const;
    bool operator>(const char* rhs) const;
    bool operator>=(const char* rhs) const;

    // Concatenation operators (Author: Elyzaveta Piletska)
    my_str_t operator+(const my_str_t& rhs) const;
    my_str_t operator+(const char* rhs) const;
    my_str_t& operator+=(const my_str_t& rhs);
    my_str_t& operator+=(const char* rhs);
    my_str_t& operator+=(char rhs);

    // Repetition operators ("a"*3 == "aaa") (Author: Elyzaveta Piletska)
    my_str_t operator*(size_t times) const;
    my_str_t& operator*=(size_t times);

    // those can't be defined inside the class without using `friend`, as they will always get the `*this` at the left argument
    // bool operator==(const char* lhs, const my_str_t& rhs);
    // bool operator!=(const char* lhs, const my_str_t& rhs);
    // bool operator<(const char* lhs, const my_str_t& rhs);
    // bool operator<=(const char* lhs, const my_str_t& rhs);
    // bool operator>(const char* lhs, const my_str_t& rhs);
    // bool operator>=(const char* lhs, const my_str_t& rhs);

    // I/O
    // std::ostream& operator<<(std::ostream& os, const my_str_t& str);
    // std::istream& operator>>(std::istream& is, my_str_t& str);
};
// I/O (Author: Elyzaveta Piletska)
std::ostream& operator<<(std::ostream& os, const my_str_t& str);
std::istream& operator>>(std::istream& is, my_str_t& str);
std::istream& readline(std::istream& stream, my_str_t& str);

// Comparison (Author: Elyzaveta Piletska)
bool operator==(const char* lhs, const my_str_t& rhs);
bool operator!=(const char* lhs, const my_str_t& rhs);
bool operator<(const char* lhs, const my_str_t& rhs);
bool operator<=(const char* lhs, const my_str_t& rhs);
bool operator>(const char* lhs, const my_str_t& rhs);
bool operator>=(const char* lhs, const my_str_t& rhs);
#endif // MY_STRING_HPP