function circos_writeconf(o,d,varargin)
% Copyright is waived
file = io_name(o.dir,'circosf.conf');
copyfile(io_name(io_dirname(mfilename('fullpath')),'circosf.conf'),file);
s=io_read(io_name(o.dir,'circosf.conf'));

R=data_get(d,'R');
[~, imgname,imgext] = fileparts(o.imgfile);
fontsize=logsig((120-R)/10)*160+30;
if o.resname
  textcolor = 'black';
  linkcolor = 'black';
  if o.resseq
    binner = num2str(fontsize/3575*(2.5+length(num2str(R)))+1+(200-fontsize)/4000);
    bouter = num2str(fontsize/3575*(2.5+length(num2str(R)))+1.1);
  else
    binner = num2str(fontsize/3575*(2.5+length(num2str(R)))+0.98+(200-fontsize)/4000);
    bouter = num2str(fontsize/3575*(2.5+length(num2str(R)))+1.08);
  end      
else
  if o.resseq
    textcolor = 'black';
    linkcolor = 'black';
    binner = num2str(fontsize/3575*(2.5+length(num2str(R)))+0.97+(200-fontsize)/4000);
    bouter = num2str(fontsize/3575*(2.5+length(num2str(R)))+1.07);
  else
    textcolor = 'white';
    linkcolor = 'white';
    binner = '1.05';
    bouter = '1.15';
  end 
end
  
    
s=regexprep(s,'FILENAMEHERE',sprintf(strcat(imgname,imgext)));
%R: [0 200] --> fontsize: [40 200]

s=regexprep(s,'BANDSIZEHERE',sprintf(num2str(floor(fontsize))));
s=regexprep(s,'LINKTHICKNESSHERE',sprintf(strcat(num2str(floor(4*47/R)),'p')));
s=regexprep(s,'RESCOLORHERE',sprintf(textcolor));
s=regexprep(s,'LINKCOLORHERE',sprintf(linkcolor));
s=regexprep(s,'BANDINNERHERE',sprintf(binner));
s=regexprep(s,'BANDOUTERHERE',sprintf(bouter));
io_write(file,s);
