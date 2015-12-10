function circos(d,varargin)
% D must be a square data (matrix), where non-zero entries are connections.
% Copyright (C) 2011 by Rehman Qureshi, Ahmet Sacan
var_get('d',rand(4,4));

o = opt_set( ...
  'dir',[] ... %tempdir for temporary files. If we create them, we delete them.
  ,'imgfile',[] ...
  ,'deletetemps',[] ...
  ,'dbg',true ...
  ,'show',~nargout ...
  ,'colormap','jet' ...
  ,'dographprepare',true ...
  ,varargin{:});
if isempty(o.deletetemps); o.deletetemps = ~o.dbg&&isempty(o.dir); end
if isempty(o.dir); o.dir = io_newtempdir('circos_'); io_mkdirif(o.dir); end
if isempty(o.imgfile); o.imgfile = io_tempfile('circos.png'); end
if o.dographprepare; d = graph_prepare(d,o); end

% Call helper functions to write/load files for execution.
[C,S] = circos_writecolors(io_name(o.dir,'colors.txt'),str2func(o.colormap),d,o);
circos_writedata(io_name(o.dir,'nodes.txt'),io_name(o.dir,'edges.txt'),io_name(o.dir,'bands.txt'),io_name(o.dir,'sstrack1.txt'),d,C,S,o);
circos_writeconf(o,d);

if o.dbg; fprintf('chdir: %s\n',o.dir); end
sys_chdir(o.dir);
if io_isfile(o.imgfile); io_unlink(o.imgfile,true); end

% Execute "Circos" from command line
s = exec_run([exec_installapp('activeperl') '/bin/perl.exe'] ...
	,{ [exec_installapp('circos') '/bin/circos'] ...
	,  '-conf', io_name(o.dir,'circosf.conf')});
sys_chdir('-');
if io_isempty(o.imgfile); dbg_stop(s);
elseif o.show; system(['start ' o.imgfile]); end
if o.deletetemps; io_unlink(o.dir); end
fclose('all');
