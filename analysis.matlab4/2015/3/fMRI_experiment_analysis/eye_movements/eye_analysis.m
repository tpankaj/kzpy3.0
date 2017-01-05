
% [et_xy et_times] = et_trace('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/20/edf/et_data.20150220_0833.edf');

% edf = edfmex('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/20/edf/et_data.20150220_0833.edf');

% a=edf.FSAMPLE.pa;

% for i = 1:100:300000;plot(squeeze(edf.FSAMPLE.gy(2,(i):(i+10000)))-340);hold on;plot(squeeze(edf.FSAMPLE.gx(2,(i):(i+10000)))-512,'r');hold off;axis([0,10000,-100,100]);pause(0.1);end
raw_msg={edf.FEVENT.message};
msg_timestamp=[edf.FEVENT.sttime];
raw_events={edf.FEVENT.codestring};

ctr = 0
for startstop=1:length(raw_msg)
    if strcmp(raw_msg{startstop},'TR_TRIGGER')
		ctr = ctr + 1;
	end        
end
ctr

