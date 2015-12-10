#include <string>
#include <vector>
using namespace std;

#include "pdbcircleplotpdb.hh"
#include "ahmet/core/vec.h"


/*
this function returns an array of Secondary Structure States, encoded
 using alpha=0, beta=1, and coils=2. The secondary structures are calculated using the
 algorithm described in "Initial structural alignment" section of the following paper:
http://zhanglab.ccmb.med.umich.edu/TM-align/TMalign.pdf

You can examine the Fortran code available at:
https://sacan.biomed.drexel.edu/svn/extern/frtmalign/main.f
Particularly, see the subroutines: assignssp, make_sec, smooth, and diszy
In that code, they make excessive use of extra variables. E.g., when they can use a for
 loop dis1_k, they repeat the code for dis13, dis14, dis15. Please prefer for loops in
 your code.
*/
//ca is an nx3 float matrix. len is the number of ca atoms.
vector<int> tmalign_getsse(fltnx3_ ca,uint32 n){
	double delta[2]={2.1,1.42};
	double lambda[2][5]={{0,0,5.45,5.18,6.37},{0,0,6.1,10.4,13}};
  float dist;
	int ab;
	bool satisfied;
  vector<int> ret(n,2); //everything is a coil (2) by default.
	for(int i = 2; i < n-4; i++){
		for(ab=0; ab<2; ab++){
			satisfied=true;
			for(int j = i-2; satisfied && j < i+1; j++){
				for(int k = 2; k < 5; k++){
					dist=flt3_dist(ca[j],ca[j+k]);
					if(abs(flt3_dist(ca[j],ca[j+k]) - lambda[ab][k]) >= delta[ab]){
						satisfied=false;
						break;
					}
				}
			}
			if(satisfied){
				ret[i]=ab; break;
			}
		}
	}
	return ret;
}

void tmalign_printsse(vector<int> sse){
	//print abcs..
}

int main(){
	mem__reset(); //required. call it at the beginning of main()
	ptndb__::DATADIR=".,../data,../../data,d:/data/ptn/pdb";

	pdbcircleplotpdb_ p("1crn.pdb");
	//p.print();
	vector<int> sse=tmalign_getsse(p.p.p->ca,p.n);
	tmalign_printsse(sse);

	system("PAUSE");	
	return 0;   
}
