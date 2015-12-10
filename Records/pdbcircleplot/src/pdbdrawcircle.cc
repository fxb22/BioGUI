#include <stdlib.h>
#include <cairo.h>
//#include <gtk/gtk.h>
#pragma comment(lib, "cairo.lib")
#include <math.h>
#include <fstream>
#include "pdbcircleplotpdb.hh"
#include "pdbdrawcircle.hh"

#ifndef M_PI
#define M_PI 3.1415926535897932384626433832795
#endif

cairo_surface_t *surface;
cairo_t *cr;

pdbdrawcircle::pdbdrawcircle(const char* pdbFilein, string outputPNGin) {
	height = 700;
	width = 700;
	lineWidth = 5;
	pdbFile = pdbFilein;
	outputPNG = outputPNGin;
}

//pdbcircle::pdbcircle(int heightin=700): height(heightin),width(700),lineWidth(5) {
//	}

void pdbdrawcircle::setWidth(int newWidth) {
	width = newWidth;
}

void pdbdrawcircle::setHeight(int newHeight) {
	height = newHeight;
}

void pdbdrawcircle::setLineWidth(int newLineWidth) {
	lineWidth = newLineWidth;
}

// exports the cairo context to a png
void pdbdrawcircle::run_png() {
	pdbcircleplotpdb_ p;
	p.loadpdb(pdbFile,50,4);

	// initialize cairo context

	// define png size
	surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, 700, 700);
	cr = cairo_create(surface);

	// create the border and circle
	cairo_set_source_rgb(cr, 0.69, 0.19, 0);
	//(width < height ? width : height) / 2
	cairo_arc(cr, width/2, (height/2)+10, 250 , 0, 2 * M_PI);
	cairo_stroke_preserve(cr);

	// make the circle trasparent
	cairo_set_source_rgba(cr, 1, 1, 1, 0); 
	cairo_fill(cr);


	// draw the lines
	points(p, p.n, lineWidth);
	cairo_move_to(cr,350, 350);
	cairo_line_to(cr, 350, 350);
	cairo_stroke(cr);

	// write the circle to a file
	system((string("del ")+outputPNG).c_str());
	cairo_surface_write_to_png(surface,outputPNG.c_str());
	// cairo_paint(cr);
    cairo_surface_destroy(surface);

	//open image using default Windows program
	//system("start circle.png");
	}

// draw the dot and label it
void pdbdrawcircle::draw_dot(const char *txt, int lineWidth, int x, int y) {
	// draw the dot
	cairo_set_source_rgb(cr,0,0,0); // black color
	cairo_set_line_width(cr, lineWidth);
	cairo_set_line_cap(cr, CAIRO_LINE_CAP_ROUND);
	cairo_move_to(cr, x, y+10);
	cairo_line_to(cr, x, y+10);
	cairo_stroke(cr);

	// now draw the text
	cairo_select_font_face(cr,"Helvetica",CAIRO_FONT_SLANT_NORMAL,CAIRO_FONT_WEIGHT_NORMAL);
	cairo_set_font_size(cr,12);
	cairo_move_to(cr,x,y+10);

			if(y==350){
			if(x>350){
		    cairo_move_to(cr,x+20 ,y);
			}
				
			if(x<350){
		
			cairo_move_to(cr,x+10,y);
			}
		}

		if(x==350)
		{
			if(y>350){
				cairo_move_to(cr,x,y+10);
			}
			if(y<350){
				cairo_move_to(cr,x,y-10);
			}}

	if(x>350 && y>350)
		cairo_move_to(cr,x+15,y+20);
	if(x>350&&y<350)
		cairo_move_to(cr,x+15,y-10);
	if(x<350&&y>350)
		cairo_move_to(cr,x-30,y+20);
	if(x<350&&y<350)
		cairo_move_to(cr,x-30,y-10);

	





	//if ( x < 250 ) {
	//	if ( y > 250 ) {
	//		cairo_move_to(cr,x-10,y+15);
	//	} else {
	//		cairo_move_to(cr,x-10,y-5);
	//	}
	//} else if ( x > 250 && y > 250 ) {
	//	cairo_move_to(cr,x+5,y+10);
	//} else {
	//	cairo_move_to(cr,x,y);
	//}
	if(txt) cairo_show_text(cr,txt); // convert char
}

void pdbdrawcircle::draw_line(int fromX, int fromY, int toX, int toY) {
	cairo_set_source_rgb(cr,.5,.5,.5);
	fromY+=10;
	toY+=10;
	// black color
	cairo_move_to(cr, fromX, fromY);
	//cairo_line_to(cr, toX, toY);
	cairo_curve_to(cr,fromX,fromY,350,350,toX,toY);
	cairo_stroke(cr);
}

// draw points on the circle
void pdbdrawcircle::points(pdbcircleplotpdb_ &p, int n, int &lineWidth) {
	for ( int i = 0; i < p.pairs.size(); i++ ) {
		draw_line(
			350+250*cos(p.pairs[i].first*((2*M_PI)/n)), 
			350+250*sin(p.pairs[i].first*((2*M_PI)/n)), 
			350+250*cos(p.pairs[i].second*((2*M_PI)/n)), 
			350+250*sin(p.pairs[i].second*((2*M_PI)/n))
			);
	}

	for ( int i = 0; i < n; i++ )
		draw_dot(p.residuenames[i].c_str(), lineWidth, 350+250*cos(i*((2*M_PI)/n)), 350+250*sin(i*((2*M_PI)/n)));
}