function circos_writedata(nodefile,edgefile,bandfile,secstrucfile,d,nC,S,o,varargin)
% Copyright (C) 2011 by Rehman Qureshi, Ahmet Sacan

o.transparentedges = false;

mat=data_get(d,'mat');
matI=mat;%~=0;
R=data_get(d,'R');
[mat, nodecolors, edgecolors]=graph_balancecolor(mat);
if strcmp(o.marker,'proxy')
  nodecolors=floor(mat_normalize(nodecolors,'range',0,[1 nC]));
else
  nodecolors=floor(mat_normalize(nodecolors,'range',0,[1 nC]));
end
edgecolors=floor(mat_normalize(edgecolors,'range',0,[1 nC]));

nodewidths=mat_normalize(nodecolors,'max',0,45000);
edgewidths=mat_normalize(abs(mat),'sum',2,nodewidths);
edgestarts=edgewidths;
center=ceil(R/2);
for r=1:R
  redgewidths=edgewidths(r,:);
  shift=center-r;
  I=circshift(1:R,[shift shift]);
  I(1:center-1)=fliplr(I(1:center-1));
  I(center+1:end)=fliplr(I(center+1:end));
  redgewidths=redgewidths(I);
  redgestarts=mat_normalize(cumsum([0 redgewidths(1:end-1)]),'range',1,[0 50000-redgewidths(end)]);
  [~,I]=sort(I);
  edgestarts(r,:)=redgestarts(I);
end
edgestarts=floor(edgestarts);
edgewidths=floor(edgewidths);

%% write nodes, bands to respective files and open sse file

%open files (f-nodes,b-bands,s-sse)
n=io_fopen(nodefile,'w');
b=io_fopen(bandfile,'w');
s=io_fopen(secstrucfile,'w');
data_get(d,'rows');
% obtain labels,ranges, and sse
labels=regexprep(data_get(d,'rows'),'\s*','_');
sc='';
info=data_get(d,'info');
chain_seq_num=data_get(info,'ranges');
prev_seq_num=0;

% iterate through chains and write to node file
for j=1:numel(chain_seq_num(:,4))
	fprintf(n,'chr - hs%d chain_%s 0 %i white chr%i\n',j,chain_seq_num{1,j},50000*chain_seq_num{j,4},j);
	
	%iterate through residues of chains 
	%write to nodes and bands files
    for i = 1:chain_seq_num{j,4}
      if strcmp(o.marker,'proxy')
        sc = sprintf('c%d ',nodecolors(i));
      elseif strcmp(o.marker,'black')
        sc = sprintf('c%d',nC+S+1);
      else
        sc = sprintf('c%d ',nC+S+i);
      end
	  labell=labels{i+prev_seq_num};
	  fprintf(n,'band hs%d %s %s %i %i %s\n',j,labell,labell,(i-1)*50000,i*50000-5000,sc);
      fprintf(b,'hs%d %i %i %s\n',j,(i-1)*50000,i*50000-5000,labell);
    end
	prev_seq_num=prev_seq_num+chain_seq_num{j,4};
end

%close files
io_fclose(n,nodefile);
io_fclose(b,bandfile);

%% work with secondary structures if needed

if o.sse
  sse=data_get(d,'sse');
  sse=double(sse);
  sse(sse==3)=0;

  % transform sse so that helices are negatively numbered and sheets are
  % positively numbered
  shel = [];
  if sse(1) == 1; shel = 1; end
  shel = [shel,find((arrayfun(@(x) and(sse(x)==1,sse(x-1)~=1),2:numel(sse))==1)==1)];
  if strcmp(o.method,'lg')
    sse(shel) = 0;
    shel = shel+1;
  end
  ehel = find((arrayfun(@(x) and(sse(x)==1,sse(x+1)~=1),1:numel(sse)-1)==1)==1);
  if sse(end) == 1; ehel(end+1) = numel(sse); end
  for i = 1:numel(shel); sse(shel(i):ehel(i))=(0-i); end

  sshe = [];
  if sse(1) == 2; sshe = 1; end
  sshe = [sshe,find((arrayfun(@(x) and(sse(x)==2,sse(x-1)~=2),2:numel(sse))==1)==1)];
  eshe = find((arrayfun(@(x) and(sse(x)==2,sse(x+1)~=2),1:numel(sse)-1)==1)==1);
  if sse(end) == 2; eshe(end+1) = numel(sse); end
  for i = 1:numel(sshe); sse(sshe(i):eshe(i))=i; end
  
  % iterate through chains and write to node file
  prev_seq_num=0;
  for j=1:numel(chain_seq_num(:,4))

    %iterate through helices and write to sse file
    k = 1;
	while k <= numel(shel)
      if shel(k) < chain_seq_num{j,4} + prev_seq_num
        fprintf(s,'hs%i %i %i 12 color=c%i\n',j,(shel(k) - prev_seq_num - 1) * 50000,(ehel(k) - prev_seq_num)*50000 - 5000,nC + 1);
      else
          k = numel(shel);
      end
      k = k + 1;
	end
	
	%iterate through sheets start residues and write to sse file
    k = 1;
    ssecolors = zeros(max(sse),1);
    while k <= max(sse)
      if ssecolors(k) == 0
        ssecolors(k) = -.5;
      end
      for l = 1:max(sse)
        d2 = matI(sshe(k):eshe(k),sshe(l):eshe(l));
        a = eshe(k) - sshe(k) + 1;
        b = eshe(l) - sshe(l) + 1;
        if b == max(a,b)
          temp = b;
          b = a;
          a = temp;
          d2 = d2';
        end
        d2 = logical(d2);
        m = 1;
        gadget = true;
        minshe = min(3,b-1);
        while and(gadget, m <= a)
          if ssecolors(l) == 0
            if sum(d2(m:a+1:end)) >= minshe
              ssecolors(l) = ssecolors(k);
              gadget = false;
            elseif sum(d2(a+1-m:a-1:end-a+1)) >= minshe
              ssecolors(l) = -ssecolors(k);
              gadget = false;
            end
          else
            if sum(d2(m:a+1:end)) >= minshe
              ssecolors(k) = ssecolors(l);
              gadget = false;
            elseif sum(d2(a+1-m:a-1:end-a+1)) >= minshe
              ssecolors(k) = -ssecolors(l);
              gadget = false;
            end
          end
          m = m + 1;
        end
      end           
      k = k + 1;
    end
	prev_seq_num=prev_seq_num+chain_seq_num{j,4};
  end
  prev_seq_num = 0;
  for j=1:numel(chain_seq_num(:,4))
     k = 1;
     while k <= max(sse)
      fprintf(s,'hs%i %i %i 12 color=c%i\n',j,(sshe(k) - prev_seq_num - 1) * 50000,...
          (eshe(k) - prev_seq_num)*50000 - 5000,nC + 2.5 + ssecolors(k));
      k = k+1;
     end
     prev_seq_num=prev_seq_num+chain_seq_num{j,4};
  end
end

io_fclose(s,secstrucfile);

%% write edges

f = io_fopen(edgefile,'w');
numlinks = 0;
if ~o.emphasize
  for r = 1:R
    for c = 1:R
      if ~matI(r,c); continue; end
      if c > r; continue; end %r->c is already drawn. let's not draw c->r.
      sc = '';
      numlinks = numlinks + 1;
      sc = sprintf(' color=c%d',floor(edgecolors(r,c)));
      if o.transparentedges; sc=[sc '_a4']; end
      rr = 1;
      rrr = 0;
      cc = 1;
      ccc = 0;
      for i = 1:numel(chain_seq_num(:,4))
        if r > chain_seq_num{i,4}
            rr = i;
            rrr = rrr+chain_seq_num{i,4};
        end
        if c > chain_seq_num{i,4}
            cc = i;
            ccc = ccc+chain_seq_num{i,4};
        end
      end
      if and(abs(((r-rrr)*50000+edgestarts(r,c))-((c-ccc)*50000+(edgestarts(c,r)+edgewidths(c,r)-1)))<(R*25000+100000),...
              abs(((r-rrr)*50000+edgestarts(r,c))-((c-ccc)*50000+edgestarts(c,r)))>(R*25000+100000))
        fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
            (r-rrr-1)*50000+edgestarts(r,c),(r-rrr-1)*50000+(edgestarts(r,c)+400));
        fprintf(f,'link%d hs%d %d %d%s\n',numlinks,cc,...
            (c-ccc-1)*50000+(edgestarts(c,r)+400),(c-ccc-1)*50000+edgestarts(c,r),sc);
      else
        fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
            (r-rrr-1)*50000+edgestarts(r,c),(r-rrr-1)*50000+(edgestarts(r,c)+edgewidths(r,c)-1));
        fprintf(f,'link%d hs%d %d %d%s\n',numlinks,cc,...
            (c-ccc-1)*50000+(edgestarts(c,r)+edgewidths(c,r)-1),(c-ccc-1)*50000+edgestarts(c,r),sc);
      end
    end
  end
else
  numlinks = 1;
  for r=1:R
    for c=1:R
      if ~matI(r,c); continue; end
      if or(sse(r) == 0,sse(c) == 0); continue; end;
      if c < r; continue; end %r->c is already drawn. let's not draw c->r.
      %numlinks = numlinks + 1;
      rr = 1;
      rrr = 0;
      cc = 1;
      ccc = 0;
      for i =1:numel(chain_seq_num(:,4))
        if r > chain_seq_num{i,4}
          rr = i;
          rrr = rrr+chain_seq_num{i,4};
        end
        if c > chain_seq_num{i,4}
          cc = i;
          ccc = ccc+chain_seq_num{i,4};
        end
      end
      if sse(r) < 0
        if and(c == 2 + r,sse(c) == sse(r))
          fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
              (r-rrr-1)*50000+20000,(r-rrr-1)*50000+30000);
          fprintf(f,'link%d hs%d %d %d color=c%d\n',numlinks,cc,...
              (c-ccc-1)*50000+30000,(c-ccc-1)*50000+20000,nC + 1);
          numlinks=numlinks + 1;
        elseif sse(c) ~= sse(r)
          fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
              (r-rrr-1)*50000+24000,(r-rrr-1)*50000+26000);
          fprintf(f,'link%d hs%d %d %d color=c%d\n',numlinks,cc,...
              (c-ccc-1)*50000+24000,(c-ccc-1)*50000+26000,nC + 5);
          numlinks=numlinks + 1;
        end
      else
        if sse(c) > 0
          if sse(c) ~= sse(r)
            if abs(((r-rrr)*50000)-((c-ccc)*50000))==(R*25000+100000)
              fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
                (r-rrr-1)*50000+40000,(r-rrr-1)*50000+45000);
              fprintf(f,'link%d hs%d %d %d color=c%d\n',numlinks,cc,...
                (c-ccc-1)*50000+5000,(c-ccc-1)*50000,nC + 4);
            else
              fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
                (r-rrr-1)*50000+15000,(r-rrr-1)*50000+35000);
              fprintf(f,'link%d hs%d %d %d color=c%d\n',numlinks,cc,...
                (c-ccc-1)*50000+35000,(c-ccc-1)*50000+15000,nC + 4);
            numlinks=numlinks+1;
            end
          end
        elseif abs(((r-rrr)*50000)-((c-ccc)*50000))==(R*25000+100000)
          fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
              (r-rrr-1)*50000+40000,(r-rrr-1)*50000+45000);
          fprintf(f,'link%d hs%d %d %d color=c%d\n',numlinks,cc,...
              (c-ccc-1)*50000+5000,(c-ccc-1)*50000,nC + 4);
        else
          fprintf(f,'link%d hs%d %d %d\n',numlinks,rr,...
              (r-rrr-1)*50000+22500,(r-rrr-1)*50000+27500);
          fprintf(f,'link%d hs%d %d %d color=c%d\n',numlinks,cc,...
              (c-ccc-1)*50000+27500,(c-ccc-1)*50000+22500,nC + 5);
          numlinks=numlinks+1;
        end
      end
    end
  end
end

io_fclose(f,edgefile);
