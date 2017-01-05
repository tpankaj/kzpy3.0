a1 = load('/Users/davidzipser/Dropbox/pimaginggrant/fmridata/prf.mat'); %load('/stone/ext3/knk/karlzipser/prf.mat');
% scp droponly@stone.psychology.wustl.edu:"/stone/ext3/knk/karlzipser/prf.mat" ~/Desktop/
a2 = load('/Users/davidzipser/Dropbox/pimaginggrant/fmridata/epilinear.mat'); %load('/stone/ext3/knk/karlzipser/epilinear.mat');
a3 = load('/Users/davidzipser/Desktop/preprocessFMAP/preprocessFMAP/GLMdenoisefiguresFMAP.mat'); %load('/stone/ext3/knk/karlzipser/12March2015_data_Karl_Zipser/12March2015_data_Karl_Zipser/nii/preprocessFMAP/GLMdenoisefiguresFMAP.mat');
a4 = load('/Users/davidzipser/Google_Drive/Data/stimuli/2015/2/11Feb2015_Vermeer_reading_videos/vermeer1to10.frames.736031.7177.mat'); %load('/stone/ext3/knk/karlzipser/12March2015_data_Karl_Zipser/12March2015_data_Karl_Zipser/stimuli/vermeer1to10.frames.736031.7177.mat');

origimA = permute(a4.frames(6*20 + linspacefixeddiff(1,6*20,6),:,:,:),[2 3 4 1]);
origim = [];
for p=1:size(origimA,4)
  origim(:,:,:,p) = imresize(origimA(:,:,:,p),[256 256]);
end

res = 256;

ix = find(a1.R2 > 10 & a1.gain > 0);
xx = []; yy = [];
ims = zeros(256*256,length(ix));
for p=1:length(ix), p
  ang0 = a1.ang(ix(p));
  ecc0 = a1.ecc(ix(p));
  rfsize0 = a1.rfsize(ix(p));
  
  [x0,y0] = pol2cart(ang0/180*pi,ecc0);
  
  [im0,xx,yy] = makecircleimage(res,2*rfsize0,xx,yy,[],0,[(1+res)/2-y0 (1+res)/2+x0]);
  
  ims(:,p) = im0(:);%/sum(im0(:));
end
assert(all(isfinite(ims(:))));
  
ixinvol = subscript(find(a2.vol),ix);

beta0 = subscript(squish(a3.betas,3),{ixinvol ':'});

beta0 = unitlength(beta0,2);

ims = bsxfun(@rdivide,ims,sum(ims,2));

for wh=1:6
  pimageA = reshapesquare(ims*beta0(:,wh));
  pimageB = reshapesquare(ims*beta0(:,wh+6));
  mx = max([abs(pimageA(:)); abs(pimageB(:))]);
  figure;
  subplot(1,3,1); hold on;
  imagesc(uint8(origim(:,:,:,wh))); axis image tight;
  set(gca,'YDir','reverse');
  subplot(1,3,2); hold on;
  imagesc(pimageA,[0 mx]); colormap(jet); axis image tight;
  set(gca,'YDir','reverse');
  subplot(1,3,3); hold on;
  imagesc(pimageB,[0 mx]); colormap(jet); axis image tight;
  set(gca,'YDir','reverse');
end

for wh=1:6
  edge0 = detectedges(rgb2gray(double(origim(:,:,:,wh))/255),1);
  whereedge = edge0 > prctile(edge0(:),95);

  pimageA = reshapesquare(ims*beta0(:,wh));
  pimageB = reshapesquare(ims*beta0(:,wh+6));
  mx = max([abs(pimageA(:)); abs(pimageB(:))]);
  figure;
  subplot(1,2,1); hold on;
  temp0 = cmaplookup(pimageA,0,mx,[],jet(256));
  temp0(repmat(whereedge,[1 1 3])) = 0;
  imagesc(temp0); axis image tight;
  set(gca,'YDir','reverse');
  subplot(1,2,2); hold on;
  temp0 = cmaplookup(pimageB,0,mx,[],jet(256));
  temp0(repmat(whereedge,[1 1 3])) = 0;
  imagesc(temp0); axis image tight;
  set(gca,'YDir','reverse');
end

