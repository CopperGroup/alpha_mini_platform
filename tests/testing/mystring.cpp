#include "mystring.hpp"
#include <iostream>
#include <cstring>
#include <string>
// Constructors

// Example usage:
// my_str_t s; // creates empty string
// (Author: Elyzaveta Piletska)
my_str_t::my_str_t() : data_m(nullptr), capacity_m(0), size_m(0) {}


// Example usage:
// my_str_t s(5, 'A'); // s = "AAAAA"
// (Author: Elyzaveta Piletska)
my_str_t::my_str_t(size_t size, char initial)
    : data_m(new char[size+1]), capacity_m(size), size_m(size)
{
    /*
     We set the data_m to store the size + 1 bytes, so, that we can hold the null terminator e.g. '\0'.
     It is used, so that we know where the string ends.
    */
    for (size_t i = 0; i < size_m; i++) {
        data_m[i] = initial;
    }
    data_m[size_m] = '\0';
}

// Example usage:
// my_str_t s("Hello"); // s = "Hello"
// (Author: Elyzaveta Piletska)
my_str_t::my_str_t(const char* cstr)
    : data_m(nullptr), capacity_m(0), size_m(0)
{
    /*
     C-string constructor. Notice, that if you pass the "Hello" string,
     it will be actualy "Hello\0", but `strlen()` doesn't count the '\0',
     so you will still get the length of "Hello" (5). The '\0' won't be memcpy-ied
     so you still have to assign the string end '\0'

     */
    if (!cstr) {
        // If the nullptr was passed, we drop out of the constructor to avoid errors
        return;
    }

    size_m = std::strlen(cstr);
    capacity_m = size_m;
    data_m = new char[capacity_m+1];
    std::memcpy(data_m, cstr, size_m);
    data_m[size_m] = '\0';
}

// Example usage:
// std::string stds = "World";
// my_str_t s(stds); // s = "World"
// (Author: Elyzaveta Piletska)
my_str_t::my_str_t(const std::string& str)
    : data_m(nullptr), capacity_m(0), size_m(0)
{
    size_m = str.size();
    capacity_m = size_m;
    data_m = new char[capacity_m + 1]; // +1 for '\0'

    std::memcpy(data_m, str.data(), size_m);
    data_m[size_m] = '\0';
}

// Example usage:
// my_str_t s1("Hi");
// my_str_t s2(s1); // copy of s1
// (Author: Elyzaveta Piletska)
my_str_t::my_str_t(const my_str_t& other)
    : data_m(new char[other.capacity_m + 1]), capacity_m(other.capacity_m), size_m(other.size_m)
{
    std::memcpy(data_m, other.data_m, size_m);
    data_m[size_m] = '\0';
}

// Example usage:
// my_str_t s1("Hello");
// my_str_t s2(std::move(s1)); // move from s1, s1 becomes empty
// (Author: Elyzaveta Piletska)
my_str_t::my_str_t(my_str_t&& other) noexcept
    : data_m(other.data_m), size_m(other.size_m), capacity_m(other.capacity_m)
{
    // Leave prev object in a safe empty state
    other.data_m = nullptr;
    other.size_m = 0;
    other.capacity_m = 0;
}

// Example usage:
// my_str_t s1("abc");
// my_str_t s2;
// s2 = std::move(s1); // move assignment
// (Author: Elyzaveta Piletska)

my_str_t& my_str_t::operator=(my_str_t&& other) noexcept
{
    if (this != &other) {
        delete[] data_m; // free current resources

        // Steal the data
        data_m = other.data_m;
        size_m = other.size_m;
        capacity_m = other.capacity_m;

        other.data_m = nullptr;
        other.size_m = 0;
        other.capacity_m = 0;
    }
    return *this;
}


// Assignment


// Example usage:
// my_str_t s1("foo");
// my_str_t s2;
// s2 = s1; // copy assignment
// (Author: Elyzaveta Piletska)

my_str_t& my_str_t::operator=(const my_str_t& other) {
    if (this == &other) return *this; // Check for self-assignment;
    char* new_data = new char[other.capacity_m + 1]; // assign new memory
    std::memcpy(new_data, other.data_m, other.size_m);
    new_data[other.size_m] = '\0';

    delete[] data_m; // delete ald array (clear old memory)

    data_m = new_data;
    size_m = other.size_m;
    capacity_m = other.capacity_m;

    return *this;
}

// Destructor

// Example usage:
// {
//   my_str_t s("temp");
// } // destructor called automatically
// (Author: Elyzaveta Piletska)

my_str_t::~my_str_t() {
    delete[] data_m; // clear symbols array
    data_m = nullptr; // making sure we don't leave dangling pointer behind
    size_m = 0;
    capacity_m = 0;
}

// Element access

/*
 Important note, what is "operator".
 "operator[]" in this case will allow us to speak to our class like we speak to array,
 e.g. mystr[2], will return you the character at the postion 2:
 "Hello" -> (l)

*/

// Example usage:
// my_str_t s("Hello");
// char c = s[1]; // 'e'
// s[0] = 'h'; // modifies string
char& my_str_t::operator[](size_t idx){
    /*
     Add the index out of bounds check if lab requires so,
     I am not sure about it, though.

     Please notice, that we return the referance "&, (char& my_str_t...)", so that
     we will be able to modify the actual value inside our string,
     not the copy of the char
	 (Author: Oksana Dziuba)
     */
    return data_m[idx];
}

// Example usage:
// const my_str_t s("Hello");
// char c = s[1]; // 'e'
const char& my_str_t::operator[](size_t idx) const {
    /*
     Add the index out of bounds check if lab requires so,
     I am not sure about it, though.

     Please notice, that we return the referance "&, (char& my_str_t...)", so that
     we will be able to read (this function works with const objects) the actual value inside our string,
     not the copy of the char.
	 (Author: Oksana Dziuba)
    */
    return data_m[idx];
}

// Example usage:
// my_str_t s("Hello");
// char c = s.at(4); // 'o'
// s.at(10); // throws std::out_of_range
// (Author: Oksana Dziuba)

char& my_str_t::at(size_t idx) {
    if (idx >= size_m) {
        throw std::out_of_range("Index out of range");
    }

    return data_m[idx];
}


const char& my_str_t::at(size_t idx) const {
    if (idx >= size_m) {
        throw std::out_of_range("Index out of range");
    }

    return data_m[idx];
}

// Capacity management

/*
 By adding `noexcept` we guarantee, that this method won't
 throw exeptions


*/

// Example usage:
// my_str_t s("Hello");
// size_t n = s.size(); // 5
// size_t cap = s.capacity();
// (Author: Oksana Dziuba)
size_t my_str_t::size() const noexcept { return size_m; }
size_t my_str_t::capacity() const noexcept { return capacity_m; }

// Example usage:
// my_str_t s("Hi");
// s.reserve(20); // ensures capacity >= 20
// (Author: Oksana Dziuba)
void my_str_t::reserve(size_t new_capacity) {
    if (new_capacity <= capacity_m) {
        // If new size smaller or equal to existing one, we do nothing
        return;
    }

    char* new_data = new char[new_capacity + 1]; // Remember about '\0'

    if (data_m) {
        std::memcpy(new_data, data_m, size_m);
        delete[] data_m; // Clear old memory
    }

    data_m = new_data;
    capacity_m = new_capacity;
    data_m[size_m] = '\0';

}
// Example usage:
// my_str_t s("Hello");
// s.shrink_to_fit(); // reduce capacity = size
// (Author: Oksana Dziuba)
void my_str_t::shrink_to_fit() {
    if (capacity_m <= size_m) {
        // If capacity is already minimum, we do nothing;
        return;
    }

    char* new_data = new char[size_m + 1]; // Remember about '\0'

    if (data_m) {
        std::memcpy(new_data, data_m, size_m);
        delete[] data_m;
    }

    data_m = new_data;
    capacity_m = size_m;
    data_m[size_m] = '\0';

}

// Example usage:
// my_str_t s("Hello");
// s.clear(); // s becomes ""
// (Author: Oksana Dziuba)
void my_str_t::clear() {
    /*
     Here we only assign the size to 0, and
     put the string end '\0'. Notice that we are
     not clearing the memory in case we will need to add symbols again,
     we won't have to re-assign the memory, and avoid unnecessary `new/delete` calls,
     this is good optimization practise

    */
    size_m = 0;
    if (data_m) {
        data_m[0] = '\0';
    }
}

// Example usage:
// my_str_t s("Hi");
// s.resize(5, '!'); // s = "Hi!!!"
// s.resize(1); // s = "H"
void my_str_t::resize(size_t new_size, char new_char) {
    if (new_size <= size_m) {
        /*
         Here we don't clear the actual symbols, because
         we have index out of range checks, so it won't return the symbol that is out of string size
		 (Author: Oksana Dziuba)
        */
        size_m = new_size;
    } else if (new_size > size_m) {
        // If new size bigger than our capacity, reserver more memory
        if (new_size > capacity_m) {
            reserve(new_size);
        }

        for (size_t i = size_m; i < new_size; ++i) {
            data_m[i] = new_char;
        }

        size_m = new_size;
    }

    data_m[size_m] = '\0';
}

// Modifiers

// my_str_t + my_str_t

// Example usage:
// my_str_t s("Hello");
// s.append(" World"); // s = "Hello World"
// (Author: Oksana Dziuba)
//
void my_str_t::append(const my_str_t& str) {
    if (str.size_m == 0) return;

    size_t new_size = size_m + str.size_m;

    if (new_size > capacity_m) {
        // If new size bigger than our capacity, reserver more memory
        reserve(new_size);
    }

    std::memcpy(data_m + size_m, str.data_m, str.size_m);
    size_m = new_size;

    data_m[size_m] = '\0';
}

// add one char

// Example usage:
// my_str_t s("Hi");
// s.append('!'); // s = "Hi!"
// (Author: Oksana Dziuba)

void my_str_t::append(char c) {
    if (size_m + 1 > capacity_m) {
        // If new size bigger than our capacity, reserver more memory
        reserve(size_m + 1);
    }

    data_m[size_m] = c;
    size_m++;
    data_m[size_m] = '\0';
}

// my_str_t + c-string

// Example usage:
// my_str_t s("Hi");
// my_str_t t(" there");
// s.append(t); // s = "Hi there"
// (Author: Oksana Dziuba)

void my_str_t::append(const char* cstr) {
    if (!cstr) return; // if nullptr - skip;

    size_t cstr_len = std::strlen(cstr);
    size_t new_size = size_m + cstr_len;

    if (new_size > capacity_m) {
        // If new size bigger than our capacity, reserver more memory
        reserve(new_size);
    }

    std::memcpy(data_m + size_m, cstr, cstr_len);

    size_m = new_size;
    data_m[size_m] = '\0';
}

// Example usage:
// my_str_t s("Hello");
// my_str_t t("World");
// s.insert(5, t); // s = "HelloWorld"
// (Author: Oksana Dziuba)

void my_str_t::insert(size_t idx, const my_str_t& str) {
    if (idx > size_m) {
        throw std::out_of_range("Index out of range");
    }

    if (str.size_m == 0) return;

    size_t new_size = size_m + str.size_m;

    if (new_size > capacity_m) {
        // If new size bigger than our capacity, reserver more memory
        reserve(new_size);
    }

    std::memmove(
        data_m + idx + str.size_m, // Destination for existing characters, that will be occupied by new string forward
        data_m + idx, // Start moving mro insertion index
        size_m - idx); // Number of character to move

    std::memcpy(data_m + idx, str.data_m, str.size_m);

    size_m = new_size;
    data_m[size_m] = '\0';
}

// insert one char

// Example usage:
// my_str_t s("Helo");
// s.insert(2, 'l'); // s = "Hello"
// (Author: Oksana Dziuba)

void my_str_t::insert(size_t idx, char c) {
    if (idx > size_m) {
        throw std::out_of_range("Index out of range");
    }

    if (size_m + 1 > capacity_m) {
        // If new size bigger than our capacity, reserver more memory
        reserve(size_m + 1);
    }

    std::memmove(
        data_m + idx + 1,
        data_m + idx,
        size_m - idx
        );

    data_m[idx] = c;
    size_m += 1;
    data_m[size_m] = '\0';
}

// insert c-string

// Example usage:
// my_str_t s("Hello!");
// s.insert(5, " World"); // s = "Hello World!"
// (Author: Oksana Dziuba)

void my_str_t::insert(size_t idx, const char* cstr) {
    if (idx > size_m) {
        throw std::out_of_range("Index out of range");
    }

    if (!cstr) return;

    size_t insert_len = std::strlen(cstr);

    if (size_m + insert_len > capacity_m) {
        // If new size bigger than our capacity, reserver more memory
        reserve(size_m + insert_len);
    }

    std::memmove(
        data_m + idx + insert_len,
        data_m + idx,
        size_m - idx
        );

    std::memcpy(data_m + idx, cstr, insert_len);

    size_m += insert_len;
    data_m[size_m] = '\0';
}

// Example usage:
// my_str_t s("Hello World");
// s.erase(5, 6); // s = "Hello"
// (Author: Oksana Dziuba)

void my_str_t::erase(size_t begin, size_t count) {
    if (begin > size_m) {
        throw std::out_of_range("Index out of range");
    }

    // if count is way too big, restrain it to the size of our string
    if (begin + count > size_m) {
        count = size_m - begin;
    }

    std::memmove(
        data_m + begin,
        data_m + begin + count,
        size_m - (begin + count)
        );

    // Uncomment if lab says to clear old symbols
    // std::memset(data_m + size_m - count, 0, count);
    size_m -= count;

    data_m[size_m] = '\0';
}

// Example usage:
// my_str_t s1("foo");
// my_str_t s2("bar");
// s1.swap(s2); // s1="bar", s2="foo"
// (Author: Oksana Dziuba)

void my_str_t::swap(my_str_t& other) noexcept {

    // Double-check if swap is allowed
    std::swap(data_m, other.data_m);
    std::swap(size_m, other.size_m);
    std::swap(capacity_m, other.capacity_m);
}



// Utilities

// Example usage:
// my_str_t s("Hello");
// const char* cstr = s.c_str(); // "Hello"
const char* my_str_t::c_str() const {
    return data_m ? data_m : "";
}

// here idx, is the search starting point

// Example usage:
// my_str_t s("Hello");
// size_t pos = s.find('o'); // 4
// (Author: Vasyl Solchanyk)

size_t my_str_t::find(char c, size_t idx) {
    if (idx > size_m) {
        throw std::out_of_range("Index out of range");
    }
    for (size_t i = idx; i < size_m; ++i) {
        if (data_m[i] == c) return i;
    }
    return not_found;
}

// Example usage:
// my_str_t s("Hello world");
// size_t pos = s.find("world"); // 6
// (Author: Vasyl Solchanyk)

size_t my_str_t::find(const char* cstr, size_t idx) {
    if (!cstr) return not_found;
    if (idx > size_m) {
        throw std::out_of_range("Index out of range");
    }

    size_t cstr_len = std::strlen(cstr);
    if (cstr_len == 0) return not_found;

    if (cstr_len > size_m - idx) {
        return not_found;
    }

    for (size_t i = idx; i <= size_m - cstr_len; ++i) {
        bool match = true;
        for (size_t j = 0; j < cstr_len; ++j) {
            if (data_m[i + j] != cstr[j]) {
                match = false;
                break;
            }
        }
        if (match) return i; // Return index of first match
    }
    return not_found;
}

size_t my_str_t::find(const std::string& str, size_t idx) {
    return find(str.c_str(), idx);
}


// Example usage:
// my_str_t s("Hello world");
// my_str_t sub = s.substr(6, 5); // "world"
// (Author: Vasyl Solchanyk)


my_str_t my_str_t::substr(size_t begin, size_t count) {
    if (begin > size_m) {
        throw std::out_of_range("Index out of range");
    }

    if (begin + count > size_m) {
        count = size_m - begin;
    }

    my_str_t result(count, ' '); // create string of needed size

    for (size_t i = 0; i < count; ++i) {
        result.data_m[i] = data_m[begin + i]; // Copy symbols
    }

    result.data_m[count] = '\0';

    return result;
}

// Comparison operators

// Example usage:
// my_str_t a("abc"), b("abc");
// bool eq = (a == b); // true
// (Author: Vasyl Solchanyk)


bool my_str_t::operator==(const my_str_t& rhs) const {
    if (size() != rhs.size()) return false;

    for (size_t i =0; i < size(); ++i) {
        if (data_m[i] != rhs[i]) {
            return false;
        }
    }

    return true;
}

bool my_str_t::operator!=(const my_str_t& rhs) const {
    // Using previous operator
    return !(*this == rhs);
}

// Example usage:
// my_str_t s("apple");
// bool less = (s < "banana"); // true
// (Author: Vasyl Solchanyk)

bool my_str_t::operator<(const my_str_t& rhs) const {
    size_t min_size = size() < rhs.size() ? size() : rhs.size();

    for (size_t  i =0; i < min_size; ++i) {
        if (data_m[i] < rhs[i]) return true;
        if (data_m[i] > rhs[i]) return false;
    }

    return size() < rhs.size();
}

bool my_str_t::operator<=(const my_str_t& rhs) const {
    return (*this < rhs) || (*this == rhs);
}
bool my_str_t::operator>(const my_str_t& rhs) const {
    return !(*this <= rhs);
}

bool my_str_t::operator>=(const my_str_t& rhs) const {
    return !(*this < rhs);
}

// my_str_t == const char*
bool my_str_t::operator==(const char* rhs) const {
    if (!rhs) return size() == 0; // nullptr treated as empty string
    size_t rhs_len = std::strlen(rhs);
    if (size() != rhs_len) return false;

    for (size_t i = 0; i < size(); ++i) {
        if (data_m[i] != rhs[i]) return false;
    }
    return true;
}

bool my_str_t::operator!=(const char* rhs) const {
    return !(*this == rhs);
}

bool my_str_t::operator<(const char* rhs) const {
    if (!rhs) return false; // nullptr is treated as empty, never "greater"
    size_t i = 0;
    while (i < size() && rhs[i] != '\0') {
        if (data_m[i] < rhs[i]) return true;
        if (data_m[i] > rhs[i]) return false;
        ++i;
    }
    return size() < std::strlen(rhs);
}

bool my_str_t::operator<=(const char* rhs) const {
    return (*this < rhs) || (*this == rhs);
}

bool my_str_t::operator>(const char* rhs) const {
    return !(*this <= rhs);
}

bool my_str_t::operator>=(const char* rhs) const {
    return !(*this < rhs);
}

// const char* == my_str_t


bool operator==(const char* lhs, const my_str_t& rhs) {
    return rhs == lhs; // call member operator
}

bool operator!=(const char* lhs, const my_str_t& rhs) {
    return !(lhs == rhs);
}

bool operator<(const char* lhs, const my_str_t& rhs) {
    return my_str_t(lhs) < rhs; // convert lhs to my_str_t and reuse operator<
}

bool operator<=(const char* lhs, const my_str_t& rhs) {
    return my_str_t(lhs) <= rhs;
}

bool operator>(const char* lhs, const my_str_t& rhs) {
    return my_str_t(lhs) > rhs;
}

bool operator>=(const char* lhs, const my_str_t& rhs) {
    return my_str_t(lhs) >= rhs;
}

// Concatenation operators
my_str_t my_str_t::operator+(const my_str_t& rhs) const {
    my_str_t result(*this); // copy current string
    result.append(rhs);     // append rhs
    return result;
}

my_str_t my_str_t::operator+(const char* rhs) const {
    my_str_t result(*this);
    result.append(rhs);
    return result;
}

my_str_t& my_str_t::operator+=(const my_str_t& rhs) {
    this->append(rhs);
    return *this;
}

my_str_t& my_str_t::operator+=(const char* rhs) {
    this->append(rhs);
    return *this;
}

my_str_t& my_str_t::operator+=(char rhs) {
    this->append(rhs);
    return *this;
}

// Repetition operators
my_str_t my_str_t::operator*(size_t times) const {
    my_str_t result;
    result.reserve(size() * times);
    for (size_t i = 0; i < times; ++i) {
        result.append(*this);
    }
    return result;
}

my_str_t& my_str_t::operator*=(size_t times) {
    my_str_t result = (*this) * times;
    this->swap(result); // replace current string with repeated version
    return *this;
}


std::ostream& operator<<(std::ostream& os, const my_str_t& str) {
    os << str.c_str();
    return os;
}
std::istream& operator>>(std::istream& is, my_str_t& str) {
    str.clear();
    char c;

    // skip spaces
    while (is.get(c) && std::isspace(static_cast<unsigned char>(c))) { // `static_cast<unsigned char>` safely converts possibly signed char

    }

    if (is) {
        do {
            str.append(c);
        } while (is.get(c) && !std::isspace(static_cast<unsigned char>(c)));

        // if the last char is space, give it back to the stream
        if (is) {
            is.unget();
        }
    }

    return is;
}

// Example usage:
// my_str_t s;
// readline(std::cin, s); // read full line into s
// (Author: Vasyl Solchanyk)

std::istream& readline(std::istream& stream, my_str_t& str) {
    str.clear();

    char c;
    while (stream.get(c)) {
        if (c == '\n') {
            break;  // stop at newline
        }
        str.append(c); // add character to my_str_t, ← null terminator is updated here
    }

    return stream;
}
//
// bool operator==(const char* lhs, const my_str_t& rhs) {
//     return rhs == lhs;
// }
//
// bool operator!=(const char* lhs, const my_str_t& rhs) {
//     return !(lhs == rhs);
// }
//
// bool operator<(const char* lhs, const my_str_t& rhs) {
//     return my_str_t(lhs) < rhs;
// }
//
// bool operator<=(const char* lhs, const my_str_t& rhs) {
//     return my_str_t(lhs) <= rhs;
// }
//
// bool operator>(const char* lhs, const my_str_t& rhs) {
//     return my_str_t(lhs) > rhs;
// }
//
// bool operator>=(const char* lhs, const my_str_t& rhs) {
//     return my_str_t(lhs) >= rhs;
// }

