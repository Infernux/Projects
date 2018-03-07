#include <cstdlib>
#include <iostream>

class Parent
{
  public:
    virtual std::string toString() { return "Parent"; }
};

class Child1 : public Parent
{
  public:
    std::string toString() { return "Child1"; }
};

class Child2 : public Parent
{
  public:
    std::string toString() { return "Child2"; }
};

int& ref_return(int& num)
{
  num += 2;
  return num;
}

void ref_test_mod(int& num)
{
  std::cout << __func__ << ':' << num << std::endl;
  num ++;
  std::cout << __func__ << ':' << num << std::endl;
}

void ref_test_pointer(int& num)
{
  std::cout << __func__ << ':' << &num << std::endl;
}

void ref_object_test(Parent& p)
{
  std::cout << __func__ << ':' << ((Child2*)&p)->toString() << std::endl;
}

void ref_object_copy_2_in_1(Parent& p1, Parent& p2)
{
  p1 = p2;
}

void ptr_object_copy_2_in_1(Parent** p1, Parent* p2)
{
  *p1 = p2;
}

int main()
{
  int num = 42;
  ref_test_mod(num);
  std::cout << __func__ << ':' << num << std::endl;
  std::cout << __func__ << ':' << &num << std::endl;

  int ret_num = ref_return(ref_return(num));
  std::cout << __func__ << ':' << ret_num << std::endl;
  std::cout << __func__ << ':' << &ret_num << std::endl;
  std::cout << __func__ << ':' << &num << std::endl;

  num = ref_return(num);
  std::cout << __func__ << ':' << num << std::endl;
  std::cout << __func__ << ':' << &num << std::endl;

  ret_num++;
  std::cout << __func__ << ':' << num << std::endl;
  std::cout << __func__ << ':' << ret_num << std::endl;

  ref_test_pointer(num);

  std::cout << "---- object ----" << std::endl;
  Child1 c1 = Child1();
  Child2 c2 = Child2();
  std::cout << c1.toString() << std::endl;

  ref_object_test(c1);
  Parent* p1 = &c1;
  ptr_object_copy_2_in_1(&p1, &c2);
  std::cout << p1->toString() << std::endl;
}
