% % ln -s ../../../../../../../../../subjects/HVO/2015/2/26/runs/r5 r5
% Vermeer: 2/12, 14, 16, 20
clc

experiments = [];
N = 0;


%%%%%%%%%%%%% surface_attention_13June2015 %%%%%%%%%%%%%
N = N + 1;
experiments(N).folder = 'surface_attention_13June2015';
experiments(N).subfolder = 'attend_opposite_x';
experiments(N).runs = {...
    {'HVO' [2015 6 15] [3 4 5 6 7 8 9 10]},...
    };

if true
N = N + 1;
experiments(N).folder = 'surface_attention_13June2015';
experiments(N).subfolder = 'attend_x';
experiments(N).runs = {...
    {'HVO' [2015 6 14] [2 3 4 5 6 7 8 9 10]},...
    };
% % run 2 has only 170 TRs. Here I set the TRs 171:184 to the average of the others, so I can use the rest of the data.    
% z_6to20mean = z_scored_20150614_093445mbboldmb620mmAPPSNs006a001.z_img+z_scored_20150614_093445mbboldmb620mmAPPSNs008a001.z_img+z_scored_20150614_093445mbboldmb620mmAPPSNs010a001.z_img;
% z_6to20mean = z_6to20mean + z_scored_20150614_093445mbboldmb620mmAPPSNs012a001.z_img+z_scored_20150614_093445mbboldmb620mmAPPSNs014a001.z_img+z_scored_20150614_093445mbboldmb620mmAPPSNs016a001.z_img;
% z_6to20mean = z_6to20mean + z_scored_20150614_093445mbboldmb620mmAPPSNs018a001.z_img+z_scored_20150614_093445mbboldmb620mmAPPSNs020a001.z_img;
% z_6to20mean = z_6to20mean / 8.0;
% z_6to20mean(:,:,:,1:170)=z_scored_20150614_093445mbboldmb620mmAPPSNs004a001.z_img(:,:,:,1:170);


%%%%%%%%%%%%% vermeer_TMS %%%%%%%%%%%%%%%%
N = N + 1;
experiments(N).folder = 'vermeer_TMS';
experiments(N).subfolder = 'low_high_TMS';
experiments(N).runs = {...
    {'S5_2015' [2015 6 3] [2 3 4 5 6 7 8 9]}};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%% vermeer_TMS %%%%%%%%%%%%%%%%
N = N + 1;
experiments(N).folder = 'vermeer_TMS';
experiments(N).subfolder = 'no_TMS';
experiments(N).runs = {...
    {'S5_2015' [2015 4 9] [7 10]}};
N = N + 1;
experiments(N).folder = 'vermeer_TMS';
experiments(N).subfolder = 'high_TMS';
experiments(N).runs = {...
    {'S5_2015' [2015 4 9] [4 6 9]}};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% HVO BELOW %%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%
N = N + 1;
experiments(N).folder = '_van_der_Weyden_short_presentations';
experiments(N).subfolder = 'vanDerWeyden1_25Feb2015';
experiments(N).runs = {...
    {'HVO' [2015 2 26] [2 3 4 5]},...
    {'HVO' [2015 2 27] [2 3 4 5]}};


%%%%%%%%%%%%% vermeer_attention %%%%%%%%%%%%%%%%
N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = 'attend_face_or_read';
experiments(N).runs = {...
    {'HVO' [2015 2 12] [3 4 5]},...
    {'HVO' [2015 2 14] [3 4 5]},...
    {'HVO' [2015 2 16] [10 11 12]},...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = '_saccade_from_vase_or_face';
experiments(N).runs = {...
    {'HVO' [2015 3 24] [2 3 4 5 8 9]},...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = '_fixate_vase_or_face';
experiments(N).runs = {...
    {'HVO' [2015 3 21] [2 4 8 9 10 11]},...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = 'attend_vase_or_read';
experiments(N).runs = {...
    {'HVO' [2015 3 9] [2 3 4 5]}...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = 'attend_vase_or_face';
experiments(N).runs = {...    
    {'HVO' [2015 3 14] [2 3 4 5]}...
    {'HVO' [2015 3 16] [2 4 5]}...
    };


N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = 'attend_object_or_body';
experiments(N).runs = {...    
    {'HVO' [2015 3 18] [2 3 4]}...
    {'HVO' [2015 3 19] [2 3 4]}...
    };



N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = 'attend_gnd_near_vase_or_face';
experiments(N).runs = {...    
    {'HVO' [2015 3 26] [2 3 4 8 9 10]}...
    {'HVO' [2015 3 27] [2 3 4 8 9 10]}...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = '_saccade_continually_vase_or_face';
experiments(N).runs = {...    
    {'HVO' [2015 3 27] [5]}...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = '_fixate_or_move_around_letter_box';
experiments(N).runs = {...    
    {'HVO' [2015 3 27] [11]}...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = 'fixate_or_read';
experiments(N).runs = {...    
    {'HVO' [2015 3 29] [2 3 4 8 9 10]}...
    };

N = N + 1;
experiments(N).folder = 'vermeer_attention';
experiments(N).subfolder = 'attend_scene_or_face';
experiments(N).runs = {...    
    {'HVO' [2015 3 30] [2 8]}...
    {'HVO' [2015 4 2] [3 4]}...
    {'HVO' [2015 4 3] [2 3 8]}...
    };
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%% BarryLyndon %%%%%%%%%%%%%%%%
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'fixate_BarryLyndon_16Jan2015_1';
experiments(N).runs = {...
    {'HVO' [2015 3 20] [2 8]},...
    {'HVO' [2015 3 23] [2]}...
    {'HVO' [2015 3 24] [10]}...
    {'HVO' [2015 3 26] [5]}...
    };
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'fixate_BarryLyndon_16Jan2015_2';
experiments(N).runs = {...
    {'HVO' [2015 3 20] [3 9]},...
    {'HVO' [2015 3 23] [3 5]}...
    {'HVO' [2015 3 29] [5]}...
    };
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'fixate_BarryLyndon_16Jan2015_3';
experiments(N).runs = {...
    {'HVO' [2015 3 20] [4 10]}...
    {'HVO' [2015 3 23] [4]}...
    {'HVO' [2015 3 24] [11]}...
    {'HVO' [2015 3 29] [11]}...
    };

N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'attend_scene_BarryLyndon_16Jan2015_1';
experiments(N).runs = {...
    {'HVO' [2015 3 30] [3 9]},...
    {'HVO' [2015 4 2] [5]}...
    {'HVO' [2015 4 3] [4]}...
    };
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'attend_scene_BarryLyndon_16Jan2015_2';
experiments(N).runs = {...
    {'HVO' [2015 3 30] [4 10]},...
    {'HVO' [2015 4 2] [6]}...
    {'HVO' [2015 4 3] [5 10]}...
    };
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'attend_scene_BarryLyndon_16Jan2015_3';
experiments(N).runs = {...
    {'HVO' [2015 3 30] [5 11]}...
    {'HVO' [2015 4 2] [7]}...
    {'HVO' [2015 4 3] [9]}...
    };
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'attend_person_not_BL_BarryLyndon_16Jan2015_1';
experiments(N).runs = {...
    {'HVO' [2015 4 7] [4 7]}...
    };
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'attend_person_not_BL_BarryLyndon_16Jan2015_2';
experiments(N).runs = {...
    {'HVO' [2015 4 7] [3 8]}...
    };
N = N + 1;
experiments(N).folder = 'BarryLyndon';
experiments(N).subfolder = 'attend_person_not_BL_BarryLyndon_16Jan2015_3';
experiments(N).runs = {...
    {'HVO' [2015 4 7] [2 9]}...
    };


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


N = N + 1;
experiments(N).folder = 'localizer2';
experiments(N).subfolder = 'orientation';
experiments(N).runs = {...
    {'HVO' [2015 2 18] [2 4]},...
    {'HVO' [2015 2 16] [3 5]},...
    {'HVO' [2015 2 9] [3 6]}};
    
N = N + 1;
experiments(N).folder = 'localizer2';
experiments(N).subfolder = 'eccentricity';
experiments(N).runs = {...
    {'HVO' [2015 2 18] [3 5]},...
    {'HVO' [2015 2 16] [4 6]},...
    {'HVO' [2015 2 9] [4 7]}};



end


start_path = pwd;
for i = 1:length(experiments)
    e = experiments(i);
    for j = 1:length(e.runs)
        r = e.runs{j};
        for k = 1:length(r{3})
            subject = r{1};
            year = r{2}(1);
            month = r{2}(2);
            day = r{2}(3);
            run_num = r{3}(k);
            runs_path = d2s({'~/Data/experiments/' e.folder '/' e.subfolder '/subjects/' subject '/' year '/' month '/' day '/runs/'});
            fps(runs_path)
            mkdir(runs_path);

            cd(runs_path)
            sys_str = d2s({'ln -s ../../../../../../../../../subjects/' subject '/' year '/' month '/' day '/runs/' run_num ' ' run_num  });
            system(sys_str);
        end
    end
end
    
cd(start_path);
