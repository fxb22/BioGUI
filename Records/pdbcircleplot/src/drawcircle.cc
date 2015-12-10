#include <stdlib.h>
#include <cairo.h>
#pragma comment(lib, "cairo.lib")
#include <math.h>
#include <fstream>
#include "pdbcircleplotpdb.hh"
#include "pdbdrawcircle.hh"

#ifndef M_PI
#define M_PI 3.1415926535897932384626433832795
#endif

int main (int argc, char *argv[]) {
	mem__reset();
	ptndb__::DATADIR="d:/data/ptn/pdb,.,../data,../../data";

	if ( argc < 3 ) {
		cout << "Usage is " << argv[0] << " <pdbfile> <pngfile>\n";
		exit(0);
	} else {
		/*
		// check if the PDB file exists
		ifstream fin(argv[2],ios::in);
		if ( fin.fail() ) {
			cout << "Invalid PDB file, please try again." << endl;
			exit(0);
		}
		*/

		char* pdbFile = argv[1];
		char* outputPNG = argv[2];

		pdbdrawcircle pc(pdbFile,outputPNG);
		pc.run_png();
		return 0;
	}
}
