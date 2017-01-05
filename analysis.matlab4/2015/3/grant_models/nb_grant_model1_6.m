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
% Grant models
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;
    if not(exist('hdr'))
        n = 40000;
        hdr = zeros(n,1,'single');
        for i = 1:n
            hdr(i) = model_HRF(i/1000);
        end
        mp({hdr},3);
    end
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    %close('all');
    
    max_time_ms = 2000;
    s1 = zeros(1,max_time_ms);
    s2 = zeros(1,max_time_ms);
    sfg = zeros(1,max_time_ms);
    satt = zeros(1,max_time_ms);
    [gn100_transient, gn100_sustained, g_fig_gnd, g_attention] = temporal_components();

    %%%%%%%%% calculate figure and ground responses for stimuli %%%%%%%%%%%
    FIG_GND = 1;
    ATTENTION = 2;
    FLICKER = 3;
    LAMINAR = 4;
    ORIENTATION = 5;
    
    experiments(LAMINAR).conditions = [1 2 3];
    experiments(FLICKER).conditions = [1 2 3];
    experiments(ATTENTION).conditions = [1];
    experiments(FIG_GND).conditions = [1];
    experiments(ORIENTATION).conditions = [1];
    
    experiments(ATTENTION).modulations = [1 1 1 0;1 1 1 1];
    experiments(FLICKER).modulations = [1 1 0 0;1 1 1 0];
    experiments(LAMINAR).modulations = [1 1 0 0;1 1 1 0];
    experiments(FIG_GND).modulations = [1 1 0 0;1 1 1 0];
    experiments(ORIENTATION).modulations = [0.3 0.3 0 0;1 1 0 0];

    for experiment = 1:length(experiments)
        experiment
        response = [];
        ctr = 0;
        for condtion = experiments(experiment).conditions%1:3%150:10:401
            ctr = ctr + 1;
            condtion
            %%%%%%%%%%% shape stimulus patterns %%%%%%%%%%%%%%%
             s1 = 0*s1; s2 = 0*s2; sfg = 0*sfg; satt = 0 * satt;

            if experiment == FLICKER % alternating blank
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
            if experiment == FIG_GND % fig/gnd
                s1(100:1100) = 1;
                sfg = s1;      
            end
            if experiment == ORIENTATION % fig/gnd
                s1(100:1100) = 1;
     
            end
            if experiment == LAMINAR % laminar measures
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

            if experiment == ATTENTION % attention
                if condtion == 1
                    s1(100:1100) = 1;
                    sfg = s1;
                    satt = s1;
                elseif condtion == 2
                    s1(100:1100) = 1;
                    satt = s1;
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
            m = experiments(experiment).modulations;
            temp = size(m);
            num_c = temp(1);
            
            for c=1:num_c
                response(ctr,c,:) = neural_response(s1,s2,sfg,satt,m(c,1)*gn100_transient, m(c,2)*gn100_sustained, m(c,3)*g_fig_gnd, m(c,4)*g_attention, max_time_ms);
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        temp = size(response);
        num_conditions = temp(1);
        num_conditions2 = temp(2);
        color_str = {'b-','r-','k-'};
        for i = 1:num_conditions
            for j = num_conditions2:-1:1
                %%%%%%%%%%% graphics %%%%%%%%%
                 mp({stimulus1(i,:),'k-','LineWidth',4},experiment,[3,3,i],'STIMULUS','time (ms)','stimulus contrast',[0,1500,0,1.5]);
                set(gca, 'YTick', []);
                mp({squeeze(response(i,j,:)),color_str{j},'LineWidth',4},experiment,[3,3,i+3],'fig vs. gnd NEURAL response','time (ms)','neural response',[0,1500,0,0.1]);
                if j == num_conditions2
                    hold on;
                end
                if j == 1
                    hold off;
                    set(gca, 'YTick', []);
                end

                

                c1=conv(hdr,squeeze(response(i,j,:)));

                t_seconds = (1:10000)/1000;
                mp({t_seconds, c1(1:length(t_seconds)),color_str{j},'LineWidth',4},experiment,[3,3,i+6],'fig vs. gnd BOLD response','time (s)','hemodynamic response',[0,10,0,35]);
                if j == num_conditions2
                    hold on;
                end
                if j == 1
                    hold off;
                    set(gca, 'YTick', []);
                end
                
                %%%%%%%%%%%%%%%%%%%%%%%%%%%
            end
        end
        hFig = figure(experiment);
        fig_width = 900; fig_height = 500;
        set(hFig, 'Position', [fig_width/2*(experiment-1) fig_height fig_width fig_height])
    end
end


