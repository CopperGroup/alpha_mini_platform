#include <iostream>
#include <string>
#include <chrono>
#include "mystring.hpp"


// Helper function to run and time a test
// Author: Elyzaveta Piletska
template <typename Func>
void run_and_time(const std::string& description, Func func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    std::cout << description << " time: " << duration << " microseconds" << std::endl;
}

int main() {
    // Existing tests as requested
    // 1. Constructor with size and initial character
    my_str_t str1(5, 'A');
    std::cout << "str1: " << str1.c_str() << std::endl;

    // 2. Constructor from C-string
    my_str_t str2("Hello");
    std::cout << "str2: " << str2.c_str() << std::endl;

    // 3. Constructor from std::string
    std::string stdStr = "World";
    my_str_t str3(stdStr);
    std::cout << "str3: " << str3.c_str() << std::endl;

    // 4. Copy constructor
    my_str_t str4(str2);
    std::cout << "str4 (copy of str2): " << str4.c_str() << std::endl;

    // 5. Copy assignment
    str4 = str3;
    std::cout << "str4 (after assignment from str3): " << str4.c_str() << std::endl;

    // 6. Swap
    str2.swap(str3);
    std::cout << "After swap str2: " << str2.c_str() << ", str3: " << str3.c_str() << std::endl;

    // 7. Index operator
    str1[2] = 'B';
    std::cout << "str1 after operator[]: " << str1.c_str() << std::endl;

    // 8. at() operator
    try {
        str1.at(10) = 'C';
    } catch (const std::out_of_range& e) {
        std::cout << "Exception caught: " << e.what() << std::endl;
    }

    // 9. reserve and shrink_to_fit
    str1.reserve(20);
    std::cout << "str1 capacity after reserve: " << str1.capacity() << std::endl;
    str1.shrink_to_fit();
    std::cout << "str1 capacity after shrink_to_fit: " << str1.capacity() << std::endl;

    // 10. resize
    str1.resize(8, 'X');
    std::cout << "str1 after resize: " << str1.c_str() << std::endl;

    // 11. clear
    str1.clear();
    std::cout << "str1 after clear: \"" << str1.c_str() << "\"" << std::endl;

    // 12. insert
    str1.append("Hello");
    str1.insert(2, 'X');
    std::cout << "str1 after insert char: " << str1.c_str() << std::endl;
    str1.insert(3, "YY");
    std::cout << "str1 after insert C-string: " << str1.c_str() << std::endl;
    str1.insert(0, str2);
    std::cout << "str1 after insert my_str_t: " << str1.c_str() << std::endl;

    // 13. append
    str1.append('Z');
    str1.append("!!!");
    str1.append(str3);
    std::cout << "str1 after appends: " << str1.c_str() << std::endl;

    // 14. erase
    str1.erase(2, 5);
    std::cout << "str1 after erase: " << str1.c_str() << std::endl;

    // 15. find
    size_t pos = str1.find('X');
    std::cout << "Position of 'X' in str1: " << pos << std::endl;
    pos = str1.find("Hello");
    std::cout << "Position of \"Hello\" in str1: " << pos << std::endl;

    // 16. substr
    my_str_t str5 = str1.substr(1, 4);
    std::cout << "Substring of str1: " << str5.c_str() << std::endl;

    // 17. size and capacity
    std::cout << "str1 size: " << str1.size() << ", capacity: " << str1.capacity() << std::endl;

    // 18. Comparison operators
    my_str_t a("Apple");
    my_str_t b("Banana");
    my_str_t c("Apple");

    std::cout << std::boolalpha; // print bools as true/false

    std::cout << "a == b: " << (a == b) << std::endl;
    std::cout << "a != b: " << (a != b) << std::endl;
    std::cout << "a < b: " << (a < b) << std::endl;
    std::cout << "a <= b: " << (a <= b) << std::endl;
    std::cout << "a > b: " << (a > b) << std::endl;
    std::cout << "a >= b: " << (a >= b) << std::endl;

    std::cout << "a == c: " << (a == c) << std::endl;
    std::cout << "a != c: " << (a != c) << std::endl;
    std::cout << "a <= c: " << (a <= c) << std::endl;
    std::cout << "a >= c: " << (a >= c) << std::endl;

    // 19. Concatenation tests
    my_str_t concat_rep_str1(5, 'A');         // "AAAAA"
    my_str_t concat_rep_str2("Hello");  // "Hello"

    my_str_t concat_result = concat_rep_str2 + concat_rep_str1;
    std::cout << "concat_rep_str2 + concat_rep_str1: " << concat_result.c_str() << std::endl;

    concat_rep_str2 += concat_rep_str1;
    std::cout << "concat_rep_str2 after += concat_rep_str1: " << concat_rep_str2.c_str() << std::endl;

    concat_rep_str2 += '!';
    std::cout << "concat_rep_str2 after += '!': " << concat_rep_str2.c_str() << std::endl;

    my_str_t concat_with_cstr = concat_rep_str1 + "XYZ";
    std::cout << "concat_rep_str1 + \"XYZ\": " << concat_with_cstr.c_str() << std::endl;

    concat_rep_str1 += "123";
    std::cout << "concat_rep_str1 after += \"123\": " << concat_rep_str1.c_str() << std::endl;

    // 20. Repetition tests
    my_str_t rep_result = concat_rep_str2 * 3;
    std::cout << "concat__rep_str2 * 3: " << rep_result.c_str() << std::endl;

    concat_rep_str2 *= 2;
    std::cout << "concat__rep_str2 after *= 2: " << concat_rep_str2.c_str() << std::endl;

    // 21. Performance comparison with std::string
    const int N = 100000; // кількість повторів
    my_str_t my_perf("A");
    std::string std_perf("A");

    // --- my_str_t concatenation ---
    auto start_my = std::chrono::high_resolution_clock::now();
    my_str_t temp_my = my_perf;
    for (int i = 0; i < N; ++i) {
        temp_my += "B";
    }
    auto end_my = std::chrono::high_resolution_clock::now();
    auto duration_my = std::chrono::duration_cast<std::chrono::milliseconds>(end_my - start_my).count();
    std::cout << "my_str_t concatenation time: " << duration_my << " ms" << std::endl;

    // --- std::string concatenation ---
    auto start_std = std::chrono::high_resolution_clock::now();
    std::string temp_std = std_perf;
    for (int i = 0; i < N; ++i) {
        temp_std += "B";
    }
    auto end_std = std::chrono::high_resolution_clock::now();
    auto duration_std = std::chrono::duration_cast<std::chrono::milliseconds>(end_std - start_std).count();
    std::cout << "std::string concatenation time: " << duration_std << " ms" << std::endl;

    // --- NEW: Time checks for all operators and functions ---
    std::cout << "\n--- Performance Tests for Individual Functions & Operators ---\n";

    // Timing Constructors
    run_and_time("my_str_t(1000, 'C') constructor", []() { my_str_t s(1000, 'C'); });
    run_and_time("std::string(1000, 'C') constructor", []() { std::string s(1000, 'C'); });

    // Timing Copy Constructor
    my_str_t base_my("This is a test string for copy constructor.");
    std::string base_std("This is a test string for copy constructor.");
    run_and_time("my_str_t copy constructor", [&]() { my_str_t s = base_my; });
    run_and_time("std::string copy constructor", [&]() { std::string s = base_std; });

    // Timing Copy Assignment
    my_str_t assigned_my;
    std::string assigned_std;
    run_and_time("my_str_t copy assignment", [&]() { assigned_my = base_my; });
    run_and_time("std::string copy assignment", [&]() { assigned_std = base_std; });

    // Timing Operator[]
    my_str_t access_my("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    std::string access_std("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    run_and_time("my_str_t operator[] (write)", [&]() { for (size_t i = 0; i < access_my.size(); ++i) access_my[i] = 'A'; });
    run_and_time("std::string operator[] (write)", [&]() { for (size_t i = 0; i < access_std.size(); ++i) access_std[i] = 'A'; });

    // Timing at()
    run_and_time("my_str_t at()", [&]() { for (size_t i = 0; i < access_my.size(); ++i) { try { access_my.at(i); } catch(...) {} } });
    run_and_time("std::string at()", [&]() { for (size_t i = 0; i < access_std.size(); ++i) { try { access_std.at(i); } catch(...) {} } });

    // Timing resize
    my_str_t resize_my("12345");
    std::string resize_std("12345");
    run_and_time("my_str_t resize to 1000", [&]() { resize_my.resize(1000, 'Z'); });
    run_and_time("std::string resize to 1000", [&]() { resize_std.resize(1000, 'Z'); });

    // Timing clear
    run_and_time("my_str_t clear", [&]() { resize_my.clear(); });
    run_and_time("std::string clear", [&]() { resize_std.clear(); });

    // Timing insert
    my_str_t insert_my("abcdef");
    std::string insert_std("abcdef");
    run_and_time("my_str_t insert at middle", [&]() { insert_my.insert(3, "XYZ"); });
    run_and_time("std::string insert at middle", [&]() { insert_std.insert(3, "XYZ"); });

    // Timing erase
    my_str_t erase_my("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    std::string erase_std("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    run_and_time("my_str_t erase", [&]() { erase_my.erase(5, 10); });
    run_and_time("std::string erase", [&]() { erase_std.erase(5, 10); });

    // Timing find
    my_str_t find_my("This is a long test string for the find method.");
    std::string find_std("This is a long test string for the find method.");
    run_and_time("my_str_t find", [&]() { find_my.find("test"); });
    run_and_time("std::string find", [&]() { find_std.find("test"); });

    // Timing substr
    run_and_time("my_str_t substr", [&]() { my_str_t sub_my = find_my.substr(10, 5); });
    run_and_time("std::string substr", [&]() { std::string sub_std = find_std.substr(10, 5); });

    // Timing comparison operators
    my_str_t comp_my1("Compare");
    my_str_t comp_my2("Compare");
    std::string comp_std1("Compare");
    std::string comp_std2("Compare");
    run_and_time("my_str_t == operator", [&]() { for(int i=0; i<1000; ++i) { volatile bool result = (comp_my1 == comp_my2); } });
    run_and_time("std::string == operator", [&]() { for(int i=0; i<1000; ++i) { volatile bool result = (comp_std1 == comp_std2); } });

    return 0;
}