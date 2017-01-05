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
CELL_NUM = 30;
    %close('all');
    
    max_time_ms = 1000;
    
    five_hundred = 900;
    
    s1 = zeros(1,five_hundred);
    s2 = zeros(1,five_hundred);
    sfg = zeros(1,five_hundred);


    if 1
        
        mp({g_fast},1,[3,3,1],'g_fast');
        mp({g_slow},1,[3,3,2],'g_slow');
        mp({gn100_transient},1,[3,3,3],'gn100_transient');
        mp({gn100_sustained},1,[3,3,6],'gn100_sustained');
        mp({g3},1,[3,3,7],'g3');
    end
return
    
    
    %%%%%%%%% calculate figure and ground responses for stimuli %%%%%%%%%%%
    response_figure = [];
    response_ground = [];
    
    ctr = 0;
    for n = 150:10:401
        ctr = ctr + 1;
        n
        %%%%%%%%%%% shape stimulus patterns %%%%%%%%%%%%%%%
        s1 = 0*s1; s2 = 0*s2; sfg = 0*sfg;
        s1(100:n) = 1;
        s2((n+0):(2*n)) = 1;
        sfg(100:(1*n)) = 1;
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        %%%%%%%%%%% accumulate various response waveforms %%%%%%
        response_figure(ctr,:) = neural_response(s1,s2,sfg,gn100_transient, gn100_sustained, g3, max_time_ms);
        response_ground(ctr,:) = neural_response(s1,s2,0*sfg,gn100_transient, gn100_sustained, g3, max_time_ms);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    temp = size(response_figure);
    num_conditions = temp(1);
    
    for i = 1:num_conditions
        %%%%%%%%%%% graphics %%%%%%%%%
        mp({response_figure(i,:),'r-'},1);
        hold on;
        mp({response_ground(i,:),'b-'},1,[1,1,1],'fig vs. gnd response');
        hold off;
        %%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        pause
    end
end


