function sse = backboneSSE(mat)
  % Function for determining secondary structure elements using a method
  % similar to that of Levitt and Greer [1] which only uses backbone
  % alpha-carbon atoms. It is an alternative to DSSP [2] but not as
  % comprehensive. DSSP uses all atoms in its determination.
  %
  % INPUT:  Square matrix of distances between Ca atoms less than
  %         some threshold. Threshold is superflous for this function.
  % OUTPUT: 1 x R matrix of SSE classification where 1 is a helix, 2 is a
  %         beta strand, and 3 is undetermined.
  %
  % Copyright is waived.
  %
  %
  % References: 
  %
  % 1. Levitt, M. and Greer, J. (1977) Automatic identification of 
  %      secondary structure in globular proteins, Journal of Molecular 
  %      Biology, 114, 181-239.
  % 2. Kabsch, W. and Sander, C. (1983) Dictionary of protein secondary
  %      structure: Pattern recognition of hydrogen-bonded and geometrical 
  %      features, Biopolymers, 22, 2577-2637.
  
  % Initialize
  R = size(mat,1);
  sse = zeros(1,R);
  mat = logical(mat);
 
  % Ensure distances between consecutive residues are ignored.
  mat(1:R+1:end) = 0;
  for i = 2:3
    mat(i:R+1:end) = 0;
    mat(1+(i-1)*R:R+1:end) = 0;
  end
  
  % Find locations of distances less than threshold.
  hits = find(mat);
  % Iterate through hits to check all distances less than threshold.
  for i=1:numel(hits)
    % Determine if a sequence of hits forms a negative diagonal
    %          (up and right). This is a beta strand.
    if and(mod(hits(i)-1,R) >= 3, ceil(hits(i)/R) <= R-3)
      if all(mat(hits(i):R-1:hits(i)+3*R))
        sse(mod(hits(i)-1,R):-1:(mod(hits(i)-1,R)-2)) = 2;
        sse(ceil(hits(i)/R):ceil(hits(i)/R)+2) = 2;
      end
    end
    
    % Determine if a sequence of hits forms a positive diagonal
    %          (down and right). This is either a helix or a beta strand.
    %          Because all helices have the same pattern as a beta strand,
    %          strands are considered only after helices are ruled out.
    if and(mod(hits(i)-1,R) <= R-3, ceil(hits(i)/R) <= R-3)
      go = true;
      if and(all(mat(hits(i):R+1:hits(i)+3*R)),...
              mod(hits(i)-1,R)+4 >= ceil(hits(i)/R))
        sse(mod(hits(i)-1,R)+1) = 1;
        sse(ceil(hits(i)/R)) = 1;
        go = false;
      end
      if and(and(mod(hits(i)-1,R) <= R-3, ceil(hits(i)/R) <= R-3),go)
        if all(mat(hits(i):R+1:hits(i)+4*R))
          sse(mod(hits(i)-1,R)+2:(mod(hits(i)-1,R)+4)) = 2;
          sse(ceil(hits(i)/R):ceil(hits(i)/R)+2) = 2;
        end
      end
    end
  end
  sse(sse==0) = 3;