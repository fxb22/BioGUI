#include <gtk/gtk.h>

#pragma comment(lib,"glib-2.0.lib")
#pragma comment(lib,"gobject-2.0.lib")
#pragma comment(lib,"gtk-win32-2.0.lib")
#pragma comment(lib,"gdk_pixbuf-2.0.lib")
#pragma comment(lib,"atk-1.0.lib")
#pragma comment(lib,"gdk-win32-2.0.lib")
#include <stdlib.h>
#include <cairo.h>
#pragma comment(lib, "cairo.lib")
#include <math.h>
#include "pdbcircleplotpdb.hh"
#include "pdbdrawcircle.hh"

#ifndef M_PI
#define M_PI 3.1415926535897932384626433832795
#endif

static GtkWidget * image;

void fileo(GtkWidget *widget, GtkWidget * load)
 {
   gtk_widget_show(load);
 }

void makePdb(GtkWidget *widget, GtkFileSelection *fs)
{

//open pdb and run drawcircle
//save png to circle.png
//change the image
char str[255];
strcpy(str,(const char*) gtk_file_selection_get_filename(GTK_FILE_SELECTION(fs)));

pdbdrawcircle pc((const char*) gtk_file_selection_get_filename(GTK_FILE_SELECTION(fs)), "circle.png");
pc.run_png();
gtk_image_set_from_file(GTK_IMAGE(image),"circle.png");
gtk_widget_hide(GTK_WIDGET(fs));

}

int main(int argc, char** argv) {
  GtkWidget *menubar;
  GtkWidget *filemenu;
  GtkWidget *file;
  GtkWidget *load;
  GtkWidget *save;
  GtkWidget *quit;
  GtkWidget *window;
 
  GtkWidget *vbox;
  GtkWidget *settings;
  GtkWidget *loader;
  
  gtk_init(&argc, &argv);

  //set up main window
  window = gtk_window_new(GTK_WINDOW_TOPLEVEL);

  gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
  gtk_window_set_default_size(GTK_WINDOW(window), 750, 600);
  gtk_window_set_title(GTK_WINDOW(window), "pdbCirclePlot");
  image = gtk_image_new_from_file("circle.png");
  

  //set up vbox
  vbox = gtk_vbox_new(FALSE,0);
  gtk_container_add(GTK_CONTAINER(window),vbox);
  

  menubar = gtk_menu_bar_new();
  filemenu = gtk_menu_new();

  file = gtk_menu_item_new_with_label("File");
  load = gtk_menu_item_new_with_label("Load");
  save = gtk_menu_item_new_with_label("Save");
  settings = gtk_menu_item_new_with_label("Settings");
  quit = gtk_menu_item_new_with_label("Quit");
  loader = gtk_file_selection_new("File selection");
  
  
  
  

  gtk_menu_item_set_submenu(GTK_MENU_ITEM(file),filemenu); 
  gtk_menu_shell_append(GTK_MENU_SHELL(filemenu),load);
  gtk_menu_shell_append(GTK_MENU_SHELL(filemenu),save);
  gtk_menu_shell_append(GTK_MENU_SHELL(filemenu),settings);
  gtk_menu_shell_append(GTK_MENU_SHELL(filemenu),quit);
  gtk_menu_shell_append(GTK_MENU_SHELL(menubar),file);
  gtk_box_pack_start(GTK_BOX(vbox),menubar,FALSE,FALSE,3);
  gtk_box_pack_start(GTK_BOX(vbox),image,FALSE,TRUE,0);
  

   g_signal_connect(window, "destroy",
      G_CALLBACK (gtk_main_quit), NULL);

	g_signal_connect(G_OBJECT(quit),"activate",
		G_CALLBACK(gtk_main_quit),NULL);

	g_signal_connect(G_OBJECT(load),"activate",
		G_CALLBACK(fileo),loader);
	
	
    /* Connect the ok_button to file_ok_sel function */
    gtk_signal_connect (GTK_OBJECT (GTK_FILE_SELECTION (loader)->ok_button),
                        "clicked", (GtkSignalFunc) makePdb, loader );
    
    /* Connect the cancel_button to destroy the widget */
    gtk_signal_connect_object (GTK_OBJECT (GTK_FILE_SELECTION
                                            (loader)->cancel_button),
                               "clicked", (GtkSignalFunc) gtk_widget_destroy,
                               GTK_OBJECT (loader),image);

  
  gtk_widget_show_all(window);

  gtk_main();

  return 0;
}