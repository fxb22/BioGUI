#ifndef _PDBDRAWCIRCLE_
#define _PDBDRAWCIRCLE_

#include <stdlib.h>
#include <cairo.h>
//#include <gtk/gtk.h>
#pragma comment(lib, "cairo.lib")
#include <math.h>
#include <fstream>
using namespace std;

class pdbdrawcircle {
public:
	// define variables
	int height;
	int width;
	int lineWidth;
	const char* pdbFile;
	string outputPNG;

	pdbdrawcircle(const char* pdbFile, string outputFile);
	void setWidth(int newWidth);
	void setHeight(int newHeight);
	void setLineWidth(int newLineWidth);
	void run_png();
	void draw_dot(const char *txt, int lineWidth, int x, int y);
	void draw_line(int fromX, int fromY, int toX, int toY);
	void points(pdbcircleplotpdb_ &p, int n, int &lineWidth);
};

#endif