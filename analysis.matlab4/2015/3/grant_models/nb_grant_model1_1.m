%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G'))
    error('NOTE: run local_startup.m manually at the beginning of the Matlab session.');
end
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GRAPHICS = 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Description . . .
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;


    max_time_ms = 1000;
    t = (1:max_time_ms)/max_time_ms;
    plot_time = -100:1:900;
    tn = t.^(1/4);
    tn100 = round(1000*tn(1:5:max_time_ms));
    
    g = gaussian(1:max_time_ms,max_time_ms/2,max_time_ms/10);
    g2 = gaussian(1:length(tn100),60,40);
    g3 = gaussian(1:(2*length(tn100)),150,15);
    gn100 = g(tn100)-g2/10;
    gn100(40:(length(tn100)-1))=gn100(1:(length(tn100)-40));
    gn100(1:40)=0;
    
    s = zeros(1,500);
    s(100:400) = 1;
    sf = zeros(1,500);
    sf(100:400) = 1;
     s(50:100) = 1; s(150:200) = 1; s(250:300) = 1; s(350:400) = 1;
     sf(50:100) = 1; sf(250:300) = 1;
    
    linear_s_gn100 = conv(s,gn100);
    thresh_s_gn100 = linear_s_gn100;
    thresh_s_gn100(find(thresh_s_gn100<0))=0;
    
    linear_s_g3 = conv(sf,g3);
    thresh_s_g3 = linear_s_g3;
    thresh_s_g3(find(thresh_s_g3<0))=0;

    mp({t,'o-'},1,[3,2,1]);    
    mp({tn100,'o-'},1,[3,2,2]);
    mp({g,'o-'},1,[3,2,3]);
    mp({gn100,'o-'},1,[3,2,4]);
    mp({g2,'o-'},1,[3,2,5]);
    mp({g3,'o-'},1,[3,2,6]);
    
    mp({s,'o-'},2,[2,2,1]);    
    mp({linear_s_gn100,'o-'},2,[2,2,2]);
    mp({plot_time(1:500),thresh_s_gn100(1:500),'b-'},2,[2,2,3]);
    hold on; mp({plot_time(1:500),thresh_s_gn100(1:500)+thresh_s_gn100(1:500).*thresh_s_g3(1:500),'r-'},2,[2,2,3]); hold off;
	%mp({,'o-'},2,[2,2,4]);
 
    mp({s,'b-'},3,[2,2,1]);hold on; mp({sf,'r-'},2,[2,2,1]); hold off;
    mp({linear_s_g3,'o-'},3,[2,2,2]);
    mp({thresh_s_g3(1:500),'o-'},3,[2,2,3]);
    
	%mp({,'o-'},32,[2,2,4]);

end


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    tmax = 300;
    t1 = 40;
    k1 = 0.1;
    k2 = 5;
    t = 0:tmax;
    stim_start = 1;
    stim_end = 200;
    
    initial_delay = 40;
    feedback_delay = 70;
    
%     stimulus = 0 * t;
%     delayed_stimulus = 0 * t;
%     stimulus(stim_start:stim_end) = 1;
%     delayed_stimulus((stim_start+initial_delay):(stim_end+initial_delay)) = stimulus(stim_start:stim_end);
%   
%     plot(stimulus);hold on;plot(delayed_stimulus,'k');hold off;
%      feedforward_component = exp( -delayed_stimulus/t1 ) + k1;
     feedforward_component = 0 * t;
     feedback_component = 0 * t;
     
     feedforward_component(initial_delay:tmax) = exp( -(0:(tmax-initial_delay))/t1 ) + k1;
%     
     feedback_component(feedback_delay:tmax) = feedforward_component.*(1-exp( -(0:(tmax-feedback_delay))/t1 ))/k2;
%     
     plot(feedforward_component);hold on;
     plot(feedback_component,'r');
     plot(feedforward_component+feedback_component,'k');hold off;
     axis([0,tmax,0,1.5]);
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    t = 1:500;
    stim_start = 100;
    stim_end = 300;

    ramp_rep = 0 * t + 1;
    ramp_rep(stim_start:stim_end) = (1:(stim_end-stim_start+1)) / (stim_end-stim_start);
    %ramp_rep = ramp_rep 
    stim = 0 * t;
    stim(find(ramp_rep > 0)) = 1;
    feedforward_component = exp(-ramp_rep/0.3);
    fsp(1,[1,3,1]);
    plot(ramp_rep,'o-');
    fsp(1,[1,3,2]);
    plot(stim,'o-');
    fsp(1,[1,3,3]);
    plot(feedforward_component,'o-');

end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%