function mix = gmminitmod(mix, x, options)
%ESta es una version modificada de GMMINIT por Manuel Guillermo Forero Vargas,
%pero incluye la rutina kmeans %de matlab, en lugar de la original
%GMMINIT Initialises Gaussian mixture model from data
%
%	Description
%	MIX = GMMINIT(MIX, X, OPTIONS) uses a dataset X to initialise the
%	parameters of a Gaussian mixture model defined by the data structure
%	MIX.  The k-means algorithm is used to determine the centres. The
%	priors are computed from the proportion of examples belonging to each
%	cluster. The covariance matrices are calculated as the sample
%	covariance of the points associated with (i.e. closest to) the
%	corresponding centres. For a mixture of PPCA model, the PPCA
%	decomposition is calculated for the points closest to a given centre.
%	This initialisation can be used as the starting point for training
%	the model using the EM algorithm.
%
%	See also
%	GMM
%

%	Copyright (c) Ian T Nabney (1996-2001)

[ndata, xdim] = size(x);

% Check that inputs are consistent
errstring = consist(mix, 'gmm', x);
if ~isempty(errstring)
  error(errstring);
end

% Arbitrary width used if variance collapses to zero: make it 'large' so
% that centre is responsible for a reasonable number of points.
GMM_WIDTH = 1.0;

% Use kmeans algorithm to set centres
%options(5) = 1;	
%[mix.centres, options, post] = kmeansnetlab(mix.centres, x, options);
[IDX,mix.centres]=kmeans(x,mix.ncentres,'start','cluster','display','final','replicates',20);
%----------------------------------------------------------------
% Set priors depending on number of points in each cluster
%cluster_sizes = max(sum(post, 1), 1);  % Make sure that no prior is zero
cluster_sizes=zeros(1,mix.ncentres);
for c=1:mix.ncentres
    [i,j]=find(IDX==c);
    cluster_sizes(c)=sum(j);
end;
%---------------------------------------------------------------
mix.priors = cluster_sizes/sum(cluster_sizes); % Normalise priors

switch mix.covar_type
case 'spherical'
   if mix.ncentres > 1
      % Determine widths as distance to nearest centre 
      % (or a constant if this is zero)
      cdist = dist2(mix.centres, mix.centres);
      cdist = cdist + diag(ones(mix.ncentres, 1)*realmax);
      mix.covars = min(cdist);
      mix.covars = mix.covars + GMM_WIDTH*(mix.covars < eps);
   else
      % Just use variance of all data points averaged over all
      % dimensions
      mix.covars = mean(diag(cov(x)));
   end
  case 'diag'
    for j = 1:mix.ncentres
      % Pick out data points belonging to this centre
      %c = x(find(post(:, j)),:);
      [a,b]=find(IDX==j);%Obtiene los indices de los objetos que pertenecen a la clase j
      c=x(a,:);%se obtiene los vectores de descriptores de los objetos de la clase j
      diffs = c - (ones(size(c, 1), 1) * mix.centres(j, :));
      mix.covars(j, :) = sum((diffs.*diffs), 1)/size(c, 1);
      % Replace small entries by GMM_WIDTH value
      mix.covars(j, :) = mix.covars(j, :) + GMM_WIDTH.*(mix.covars(j, :)<eps);
    end
  case 'full'
    for j = 1:mix.ncentres
      % Pick out data points belonging to this centre
      %c = x(find(post(:, j)),:);
      [a,b]=find(IDX==j);%Obtiene los indices de los objetos que pertenecen a la clase j
      c=x(a,:);%se obtiene los vectores de descriptores de los objetos de la clase j
      diffs = c - (ones(size(c, 1), 1) * mix.centres(j, :));
      mix.covars(:,:,j) = (diffs'*diffs)/(size(c, 1));
      % Add GMM_WIDTH*Identity to rank-deficient covariance matrices
      if rank(mix.covars(:,:,j)) < mix.nin
	mix.covars(:,:,j) = mix.covars(:,:,i) + GMM_WIDTH.*eye(mix.nin);
      end
    end
  case 'ppca'
    for j = 1:mix.ncentres
      % Pick out data points belonging to this centre
%      c = x(find(post(:,j)),:);
      [a,b]=find(IDX==j);%Obtiene los indices de los objetos que pertenecen a la clase j
      c=x(a,:);%se obtiene los vectores de descriptores de los objetos de la clase j
      diffs = c - (ones(size(c, 1), 1) * mix.centres(j, :));
      [tempcovars, tempU, templambda] = ...
	ppca((diffs'*diffs)/size(c, 1), mix.ppca_dim);
      if length(templambda) ~= mix.ppca_dim
	error('Unable to extract enough components');
      else 
        mix.covars(j) = tempcovars;
        mix.U(:, :, j) = tempU;
        mix.lambda(j, :) = templambda;
      end
    end
  otherwise
    error(['Unknown covariance type ', mix.covar_type]);
end