function [C,S] = circos_writecolors(file,colmap,d,o)
% C can be an nx3 matrix or a single number n.
% Copyright (C) 2011 by Rehman Qureshi, Ahmet Sacan

f = io_fopen(file,'w');
if ~o.emphasize
  mat = data_get(d,'mat');
  C = max(data_get(d,'R'),numel(unique(mat)));
  C = color_map(colmap,C);
  if is_double(C); C = floor(C*255); end
else
  C = [0,0,220;220,0,0];
  if strcmp(o.marker,'proxy')
    mat = data_get(d,'mat');
    nC = max(data_get(d,'R'),numel(unique(mat)));
    nC = color_map(colmap,nC);
    if is_double(nC); nC = floor(nC*255); end
  end  
end

S = [];
if o.sse; S = [220,0,0;86,255,16;255,255,86;0,0,220;160,160,160]; end

if strcmp(o.marker,'black'); M = [80,80,80];
elseif strcmp(o.marker,'order')
  M = color_map(colmap,data_get(d,'R'));
  is_double(M); M = floor(M*255);
elseif strcmp(o.marker,'charge')
  R = data_get(d,'R');
  M = zeros(R,1);
  for i = 1:R
    switch d.rows{i}(1:3)
        case {'Asp','Glu'}; M(i,:) = .1;
        case {'Arg','His','Lys'}; M(i,:) = .9;
        case {'Ser','Thr','Asn','Gln'}; M(i,:) = .3;
        case {'Cys','Gly','Pro'}; M(i,:) = .7;
        case {'Ala','Val','Ile','Leu','Met','Phe','Tyr','trp'}
            M(i,:) = .5;
        otherwise; M(i,:) = .01;
    end
  end
  G = color_map(colmap,size(M,1));
  G = floor(G*255);
elseif strcmp(o.marker,'hydro')
  R = data_get(d,'R');
  M = zeros(R,1);
  for i = 1:R
    switch d.rows{i}(1:3)
        case 'Ile'; M(i) = 4.5; case 'Val'; M(i) = 4.2;
        case 'Leu'; M(i) = 3.8; case 'Phe'; M(i) = 2.8;
        case 'Cys'; M(i) = 2.5; case 'Met'; M(i) = 1.9;
        case 'Ala'; M(i) = 1.8; case 'Gly'; M(i) = -0.4;
        case 'Thr'; M(i) = -0.7; case 'Ser'; M(i) = -0.8;
        case 'Trp'; M(i) = -0.9; case 'Tyr'; M(i) = -1.3;
        case 'Pro'; M(i) = -1.3; case 'His'; M(i) = -3.2;
        case {'Gln','Glu','Asn','Asp'}; M(i) = -3.5;
        case 'Lys'; M(i) = -3.9; case 'Arg'; M(i) = -4.5;
        otherwise; M(i) = 0.5;
    end
  end
  M = (M+4.5)/9.2;
  G = color_map(colmap,size(M,1));
  G = floor(G*255);
elseif strcmp(o.marker, 'size')
  R = data_get(d,'R');
  M = zeros(R,1);
  for i = 1:R
    switch d.rows{i}(1:3)
        case 'Ile'; M(i) = 131.18; case 'Val'; M(i) = 117.15;
        case 'Leu'; M(i) = 131.18; case 'Phe'; M(i) = 165.19;
        case 'Cys'; M(i) = 121.16; case 'Met'; M(i) = 149.21;
        case 'Ala'; M(i) = 89.10; case 'Gly'; M(i) = 75.07;
        case 'Thr'; M(i) = 119.12; case 'Ser'; M(i) = 105.09;
        case 'Trp'; M(i) = 204.23; case 'Tyr'; M(i) = 181.19;
        case 'Pro'; M(i) = 115.13; case 'His'; M(i) = 155.16;
        case 'Gln'; M(i) = 146.15; case 'Glu'; M(i) = 147.13;
        case 'Asn'; M(i) = 132.12; case 'Asp'; M(i) = 133.11;
        case 'Lys'; M(i) = 146.19; case 'Arg'; M(i) = 174.20;
        otherwise; M(i) = 210.00;
    end
  end
  M = (M-75.07)/(135);
  G = color_map(colmap,size(M,1));
  G = floor(G*255);
elseif strcmp(o.marker, 'proxy'); M = [];
end

if ~and(o.emphasize,strcmp(o.marker,'proxy'))
  for i=1:size(C,1);
    fprintf(f,'c%i = %i,%i,%i\n',i,C(i,:));
  end
else
  nC(1:2,:) = [0,0,220;220,0,0];
  for i=1:size(nC,1);
    fprintf(f,'c%i = %i,%i,%i\n',i,nC(i,:));
  end
  C = nC;
end
for i=1:size(S,1);
  fprintf(f,'c%i = %i,%i,%i\n',i+size(C,1),S(i,:));
end
for i=1:size(M,1);
  if strfind('chargehydrosize',o.marker)
    fprintf(f,'c%i = %i,%i,%i\n',i+size(C,1)+size(S,1),G(ceil(size(G,1)*M(i)+.1),:));
  %elseif strcmp('order',o.marker)
   % fprintf(f,'c%i = %i,%i,%i\n',i);
  else
    fprintf(f,'c%i = %i,%i,%i\n',i+size(C,1)+size(S,1),M(i,:));
  end
end
io_fclose(f,file);

C = size(C,1);
S = size(S,1);