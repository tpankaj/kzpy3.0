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

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;
    n = 40000;
    hdr = zeros(n,1,'single');
    for i = 1:n
        hdr(i) = model_HRF(i/1000);
    end
    mp({hdr},3);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    %close('all');
    
    max_time_ms = 2000;
    s1 = zeros(1,max_time_ms);
    s2 = zeros(1,max_time_ms);
    sfg = zeros(1,max_time_ms);
    [gn100_transient,gn100_sustained,g3] = temporal_components();

    %%%%%%%%% calculate figure and ground responses for stimuli %%%%%%%%%%%
    experiments(1).conditions = [1 2 3];
    experiments(2).conditions = [1 2 3];
    
    for experiment = 1:2
        response_figure = [];
        response_ground = [];
        ctr = 0;
        for condtion = experiments(experiment).conditions%1:3%150:10:401
            ctr = ctr + 1;
            condtion
            %%%%%%%%%%% shape stimulus patterns %%%%%%%%%%%%%%%
             s1 = 0*s1; s2 = 0*s2; sfg = 0*sfg;

            if experiment == 1 % alternating blank
                if condtion == 2
                    for i = 0:2
                        s1((i*400+100):(i*400+300))=1;
                    end
                    sfg = s1;
                elseif condtion == 3
                    for i = 0:5
                        s1((i*200+50):(i*200+150))=1;
                    end
                    sfg = s1;
                elseif condtion == 1
                    s1(100:1100) = 1;
                    sfg = s1;      
                else
                    error('');
                end
            end
            
            if experiment == 2 % laminar measures
                if or(condtion == 1, condtion == 3)
                    s1(100:1100) = 1;
                    sfg = s1;
                elseif condtion == 2
                    s1(100:1100) = 1;
                    sfg = s1/5;    
                else
                    error('');
                end
            end

            if experiment == 0 % alternating mask
                soa = 75*condtion;
                for i = 0:1:(floor(max_time_ms/(condtion*100)))
                    if iseven(i)
                        s1((1+i*soa):((i+1)*soa))=1;
                        sfg((1+i*soa):((i+1)*soa))=1;
                    else
                        s2((i*soa):((i+1)*soa))=1;
                    end
                end      
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            %%%%%%%%%%% accumulate various response waveforms %%%%%%
            stimulus1(ctr,:) = s1;
            response_figure(ctr,:) = neural_response(s1,s2,sfg,gn100_transient, 1*gn100_sustained, g3, max_time_ms);
            response_ground(ctr,:) = neural_response(s1,s2,0*sfg,gn100_transient, 1*gn100_sustained, g3, max_time_ms);
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        temp = size(response_figure);
        num_conditions = temp(1);

        for i = 1:num_conditions
            %%%%%%%%%%% graphics %%%%%%%%%
            mp({stimulus1(i,:),'k-'},experiment,[3,3,i],'STIMULUS','time (ms)','stimulus contrast');
            axis([0,1500,0,1.5]); set(gca, 'YTick', []);

            mp({response_figure(i,:),'r-'},experiment,[3,3,i+3],'fig vs. gnd NEURAL response','time (ms)','neural response');
            hold on;
            mp({response_ground(i,:),'b-'},experiment,[3,3,i+3]);
            hold off;
            axis([0,1500,0,0.1]); set(gca, 'YTick', []);


            c1=conv(hdr,response_figure(i,:));
            c2=conv(hdr,response_ground(i,:));
            t_seconds = (1:10000)/1000;
            mp({t_seconds, c1(1:length(t_seconds)),'r-'},experiment,[3,3,i+6],'fig vs. gnd BOLD response','time (s)','hemodynamic response');

            hold on;
            mp({t_seconds, c2(1:length(t_seconds)),'b-'},experiment,[3,3,i+6]);
            hold off;
            axis([0,10,0,100]); set(gca, 'YTick', []);
            %%%%%%%%%%%%%%%%%%%%%%%%%%%
        end
    end
end


