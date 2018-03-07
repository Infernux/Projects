#include <cstdlib>
#include <iostream>
#include <vector>

#include <algorithm> //for_each

class traction_type
{
  public:
    virtual std::string print_traction() { return "base traction"; }
    virtual int how_many_wheels_are_used() = 0;
};

class fwd : public traction_type
{
  std::string print_traction() { return "FWD !"; }
  virtual int how_many_wheels_are_used() { return 2; };
};

class awd : public traction_type
{
  std::string print_traction() { return "AWD !"; }
  virtual int how_many_wheels_are_used() { return 4; };
};

void pointer_print_and_clear(traction_type *tt)
{
  std::cout << tt->print_traction() << std::endl;
  delete(tt);
}

int main()
{
  std::vector<traction_type*> cars = std::vector<traction_type*>();
  cars.push_back(new fwd());
  cars.push_back(new awd());
  for(auto it = cars.begin(); it < cars.end(); ++it){
    std::cout << (*it)->print_traction() << std::endl;
    std::cout << (*it)->how_many_wheels_are_used() << std::endl;
  }
  for_each(cars.begin(), cars.end(), pointer_print_and_clear);
}
