#include "pdbclass.h"
#include <string>
#include <vector>
using namespace std;


int main(){
    
  pdb bob = pdb("../data/1crn.pdb");
  bob.readpdb();
  bob.print();
  system("PAUSE");
  return 0;  
    
    
}
