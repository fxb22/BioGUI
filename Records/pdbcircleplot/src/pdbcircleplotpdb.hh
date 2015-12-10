#include "ahmet/bio/ptndb2.hh"
#include "ahmet/bio/ptndb.h"
#pragma comment(lib, "libcore.lib")
#pragma comment(lib, "libbio.lib")

class pdbcircleplotpdb_ {
public:
	pdb_ p;
	ptn_len_ n; //number of residues
	uint32 chaincount;
	vector<ptn_len_> chainlens;
	vector<string> residuenames;
	vector<pair<ptn_len_,ptn_len_>> pairs;
	vector<double> pairsdistsqr;

	pdbcircleplotpdb_(string file=""){ if(!file.empty()) loadpdb(file); }
	void loadpdb(string file,double distsqrthreshold=49,ptn_len_ skipconsecutive=2){
		p.loadpdb(file);
		n=p.residuecount();
		chaincount=p.chaincount();
		chainlens=p.chainlens();
		residuenames=p.residuenames();
		pairs=p.getcontactpairs(distsqrthreshold,skipconsecutive,&pairsdistsqr);
	}
	void print(){
		int i;
		bailout(!p.loaded&&"you need to call loadfile(filepath) first");
		printf("total number of residues: %d\n",n);
		printf("number of chains: %d\n",chainlens.size());
		forto(i,chaincount)
			printf(" length of chain %d: %d\n",i,chainlens[i]);

		printf("Residue names: ");
		forto(i,n)
			printf("%s ",residuenames[i].c_str());
		printf("\n");

		printf("Contact pairs: \n");
		forto(i,pairs.size())
			printf("%d %d %lf\n",pairs[i].first,pairs[i].second,pairsdistsqr[i]);
	}
};
