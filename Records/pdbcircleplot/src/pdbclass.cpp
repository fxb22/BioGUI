#include "pdbclass.hh"
#include <string>
#include <stdio.h>
#include <fstream>
#include <cmath>
using namespace std;

/*
	pdb(string filepathin):filepath(filepathin){
	}

pdb::pdb (string filepathin){
	filepath = filepathin;
	return;
}

/*
vector<pair<int,int>> pdb::getNeighbors(float thresholdsqr){
	vector<pair<int,int>> ret;
	float distancesqr;

	for (int i = 1;i < residue.size();i++){
		for (int j = 1;j < residue.size();j++){
			distancesqr = pow((cacoordsX[i] - cacoordsX[j]),2) + pow((cacoordsY[i] - cacoordsY[j]),2) + pow((cacoordsZ[i] - cacoordsZ[j]),2);

			// check the threshold
			if (distancesqr < thresholdsqr && j != i && j != (i+1) && j != (i-1))
				ret.push_back(make_pair (i,j));
		}
	}
	
	// return a vector with the points
	return ret;
}


void pdb::readpdb(){
	FILE * pFile;         //File Stream
	char line[82];        //Contains one line of the PDB file
	char token[82];      //Contains the identifier for the PDB line
    char atomtype[82];         //Stores the Atom type
    char residuetemp[82];
    float x,y,z;          //Stores the X Y and Z coordinates
    
    // =========User file input/error check======
    if(!(pFile = fopen (filepath.c_str(),"r")))
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
				cacoordsX.push_back(x);
				cacoordsY.push_back(y);
				cacoordsZ.push_back(z);
				sscanf(&line[17],"%s",&residuetemp);
				residue.push_back(residuetemp); 
			}
		}
	}

    fclose(pFile);
}

void pdb::print(){
	for(int i = 0;i < cacoordsX.size();i++)
		printf("%s %f %f %f\n",residue[i].c_str(),cacoordsX[i],cacoordsY[i],cacoordsZ[i]);
}
*/