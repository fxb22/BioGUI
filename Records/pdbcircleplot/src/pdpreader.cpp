/*
PDB Alpha Carbon Coordinate Reader

Authors: Gavin Rapp 
         Henry Kuns

Version: 1.0

Revisons:
         3/29/11 - Created
*/




#include <stdio.h>
#include <fstream>
#include <assert.h>
#include <vector>
using namespace std;

class pdb {
public:
	string filepath;
	vector<float> cacoords;

	pdb(string filepathin){
		filepath=filepathin;
	}
	void readpdb(){
		//read pdb file , put ca coordinates into cacoords
	}
	void print(){
		//print cacoords.
	}

};

int main(int argc, char *argv[])
{
    
    FILE * pFile;         //File Stream
    char line[82];        //Contains one line of the PDB file
    char token[82];      //Contains the identifier for the PDB line
    char atomtype[82];         //Stores the Atom type
    float x,y,z;          //Stores the X Y and Z coordinates
    
	assert(argc>1);
    // =========User file input/error check======
    if(!(pFile = fopen (argv[1],"r")))
		perror("Error opening file");
    
    //======= Main Loop =======
    
    while(!feof(pFile)){        
     if(!fgets(line,82,pFile)) break;
	 token[0]=0;
	 if(!sscanf(line,"%s",&token)) continue;
	 if(!strcmp(token,"ATOM")){
		 if(!sscanf(&line[12],"%s",&atomtype)) continue;
		 if(!strcmp(atomtype,"CA")){
			 if(sscanf(&line[30],"%f %f %f",&x,&y,&z)!=3) continue;
			 printf("%f %f %f\n",x,y,z);
		 }
	 }
	}
    fclose(pFile);
    system("PAUSE");
    return 0;
}
