function [et_xy et_times] = et_trace(edf_filename,eye)

if nargin<2
    eye = 2; %right eye
end


% load edf into struct
edf = edfmex(edf_filename);
disp(sprintf('\n'));


%% filter trials
raw_msg={edf.FEVENT.message};
msg_timestamp=[edf.FEVENT.sttime];
raw_events={edf.FEVENT.codestring};

% get trialstart, trialend for the given datafile

start_idx=[];
timestamps=1;

% this just gets you message-based trial windows

for startstop=1:length(raw_msg)
    if strcmp(raw_msg{startstop},'SYNCTIME')
        start_idx = startstop;

        time_idx_start = find(edf.FSAMPLE.time>=msg_timestamp(startstop),1,'first');
        start_timestamp = edf.FSAMPLE.time(time_idx_start);
    end
    
            
end

%% stats for each trial
x_trace = edf.FSAMPLE.gx(eye,time_idx_start:end);
y_trace = edf.FSAMPLE.gy(eye,time_idx_start:end);
et_times = (double(edf.FSAMPLE.time(time_idx_start:end) - start_timestamp))./1000;

et_xy = [x_trace; y_trace];



% filter out timepoints where tracking failed
mask = true(size(et_times));
mask(x_trace > 1024) = false;    %Arbitrary criterion. Could also use sd, or y


%% plot time traces for each trial
figure; hold on;
% ylim([406 618]);

plot(et_xy(1,mask(1:1000/2:end)),et_xy(2,mask(1:1000/2:end)));    %only 2 samples per second
 


