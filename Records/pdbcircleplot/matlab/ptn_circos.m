function ptn_circos(p,varargin)
% Function to implement web tool for PDBCirclePlot [1].
%
% INPUT:  'p'- string - PDB identifier
%    optional:   'dographprepare'- boolean
%                'show'- boolean
%                'resseq'- boolean
%                'resname'- boolean
%                'threshold'- numerical - [4,8]
%                'info'- boolean
%                'sse'- boolean
%                'emphasize'- boolean
%                'marker'- string - {'black', 'order', 'charge',
%                                    'hydro', 'size', 'proxy'}
%                'method'- string - {'dssp', 'lg'}
% OUTPUT: string - image file location
%
% Copyright (C) 2012 by Ahmet Sacan
%
%
% References:
% 1. PDBCirclePlot paper to be published

% Initialization and set up
% To be replaced with varget('p',p)
%var_get('p','1crn');
o = opt_set( ...
  'dographprepare',false ...
  ,'show',~nargout ...
  ,'resseq',true ...
  ,'resname',true ...
  ,'threshold',6 ...
  ,'info',true...
  ,'sse',true...
  ,'emphasize',false...
  ,'marker','proxy'...
  ,'method','lg'...
  ,varargin{:});
mat = ptn_get(p,'!distsqrmat');
R = size(mat,1);
rows = cell(R,0);
rows(:,end+1) = str_ucwords(lower(ptn_get(p,'!resname')));
if o.resseq; rows(:,end+1) = str_numtocell(ptn_get(p,'!resseq')); end
if o.info; info = ptn_get(p,'!info'); end
if isempty(rows); rows(:,end+1) = str_numtocell(1:size(rows,1)); end
for i = 1:size(rows,1)
  rows{i,1} = str_implode(rows(i,:),'');
end
rows = rows(:,1);

% Remove links between consecutive residues.
mat(1:R+1:end) = 0;
for i = 2:3
  mat(i:R+1:end) = 0;
  mat(i+(i-1)*R:R+1:end) = 0;
end

% Initialize mat so only distance less than threshold are used.
% Use negatives to generate blue/green image.
mat(mat>o.threshold^2) = 0;
% Inverse mat so red is closer.
mat = -mat;

% Check if SSE is shown. If so, assign by specified method
sse = [];
if o.sse
  if strcmp(o.method, 'dssp'); sse = ptn_get(p,'!sse');
  elseif strcmp(o.method, 'lg'); sse = backboneSSE(mat); end
else
  o.emphasize = false;
end

% Call circos1.m to generate image.
d=struct('mat',mat,'rows',{rows},'info',info,'sse',sse);
circos(d,o);
